import contextlib
import os

from ..util import autolink
from ..util import elffile
from ..util.elffile import PT

from context import Context
from linker import Linker

class Binary:
    """Binary class representing a binary file

    Use pt.binary to get this instance.

    """
    def __init__(self, path):
        self.path = path
        self.fileobj = open(path, 'rb')
        self.elf = elffile.open(fileobj=self.fileobj)
        self.linker = Linker(self)

        self.final_hook = []
        self.asm_hook = []
        self.c_hook = []

        self.verbose = False
        autolink.declare(self.linker)

        start = 0xFFFFFFFFFFFFFFFF
        end = 0
        # find the end of current segments
        # TODO: doesn't handle new mem being mapped or unmapped
        for ph in reversed(self.elf.progs):
            if ph.isload:
                start = min(start, ph.vaddr)
                end = max(ph.vaddr + ph.vsize, end)

        def new_segment(addr):
            """adds a patch segment

            Args:
              addr (int): address to create segment
            
            Returns:
              ph: added program header

            """
            align = 0x1000
            ph = self.elf.programHeaderClass()
            ph.data = bytearray()
            ph.type = PT['PT_LOAD'].code
            ph.vaddr = (addr + align - 1) & ~(align - 1)
            ph.paddr = ph.vaddr
            # TODO: default is RWX?!
            ph.flags = 7
            ph.align = align
            ph.memsz = 0
            ph.filesz = 0
            self.elf.progs.append(ph)
            return ph

        # patch, nxpatch, linkpatch, jitpatch is new segments of different 
        # semantics, adds them to binary first, if we don't need any of them,
        # just remove it when saving
        self.patch = new_segment(end)
        self.nxpatch = new_segment(end + 0x800000)
        self.nxpatch.flags = 6 # RW
        self.linkpatch = new_segment(end + 0x1600000)
        self.jitpatch = new_segment(end + 0x2400000)

        self.entry_hooks = []

    def _seg(self, name):
        """get the segment of such name, default is 'patch'
        """
        return {
            'patch': self.patch,
            'nx': self.nxpatch,
            'link': self.linkpatch,
            'jit': self.jitpatch,
        }.get(name, 'patch')

    @contextlib.contextmanager
    def collect(self):
        """collects a context as a wrapper of binary

        Returns:
          Context: context of binary

        """
        p = Context(self, verbose=self.verbose)
        yield p

    def next_alloc(self, target='patch'):
        """returns the address of next allocation

        This actually returns the end of some segment

        Args:
          target (str): segment name, one of 'patch', 'nx', 'link' or 'jit'

        Returns:
          int: address of the next allocation(end of segment)

        """
        return self._seg(target).vend

    def alloc(self, size, target='patch'):
        """allocates a new chunk of memory of given size

        Args:
          size (int): size to allocate
          target (str): where to put new memory, available choices are 'patch', 'nx', 'link' or 'jit'

        Returns:
          int: allocated memory start address

        """
        # new segment, within target
        ph = self._seg(target)
        # next_alloc is used to get the address
        # of the next allocation, which is what
        # we are doing (thus the name)
        tmp = self.next_alloc(target)

        # set segment info
        ph.data += '\0' * size
        ph.memsz += size
        ph.filesz += size
        return tmp

    def onfinal(self, cb):
        self.final_hook.append(cb)

    def onasm(self, cb):
        self.asm_hook.append(cb)

    def save(self, path):
        """saves a binary


        Args:
          path (str): the path to save binary to

        Returns:
          None

        """
        self.nxpatch.flags &= ~1

        print('[+] Saving binary to: {}'.format(path))
        # hooking the entry point is a special case that generates a more efficient call table
        if self.entry_hooks:
            with self.collect() as pt:
                # call each hook addr then jump to original entry point
                calls = map(pt.arch.call, self.entry_hooks) + [pt.arch.jmp(pt.entry)]
                addr = pt.inject(asm=';'.join(calls), internal=True)
                pt.entry = addr

        for cb in self.final_hook:
            with self.collect() as pt:
                cb(pt)

        for prog in (self.patch, self.nxpatch, self.linkpatch, self.jitpatch):
            # no program header is needed, remove it
            if not prog.filesz and prog in self.elf.progs:
                self.elf.progs.remove(prog)

        self.elf.save(path)
        os.chmod(path, 0755)
