import re
from capstone import *
from keystone import *

class Arch:
    """Arch class represents the current architecture
    
    One can use Context object to get Arch, like pt.arch
    This one is just base class

    """
    def __init__(self):
        # capstone object
        self.cs = Cs(*self._cs)
        self.cs.detail = True
        # keystone object
        self.ks = Ks(*self._ks)

    def asm(self, asm, addr=0, att_syntax=False):
        """assembling of this architecture

        This is the internal implementation of pt.asm, using
        keystone to do disassemble job.


        """
        if not asm:
            return ''
        # asm start label for use with relative offsets
        asm = '_PKST_:;' + asm

        saved = self.ks.syntax
        if att_syntax:
            self.ks.syntax = KS_OPT_SYNTAX_ATT
        # FIXME debug print
        print("assembling {}".format(asm))
        tmp, _ = self.ks.asm(asm, addr=addr)
        self.ks.syntax = saved
        return ''.join(map(chr, tmp))

    def dis(self, raw, addr=0):
        """disassembling of this architecture

        This is the internal implementation of pt.dis, using
        capstone to do disassemble job.

        """
        return list(self.cs.disasm(str(raw), addr))

    def jmp(self, dst):
        raise NotImplementedError

    def call(self, dst):
        raise NotImplementedError

    def ret(self):
        raise NotImplementedError

    def nop(self):
        raise NotImplementedError


class x86(Arch):
    """x86 implementation of Arch class

    Use pt.arch to get the instance.

    """
    _cs = CS_ARCH_X86, CS_MODE_32
    _ks = KS_ARCH_X86, KS_MODE_32

    def call(self, dst): 
        return 'call {};'.format(dst)

    def jmp(self, dst):
        return 'jmp {};'.format(dst)

    def ret(self): return 'ret;'
    def nop(self): return 'nop;'

    # memcpy should be pc-relative
    # dst and src are offsets from the _PKST_ label
    def memcpy(self, dst, src, size):
        """memcpy implementation under x86 arch
        """
        return '''
        push edi
        push esi
        push ecx

        call ref
        ref: pop edi
        sub edi, ref - _PKST_
        mov esi, edi

        add edi, {}
        add esi, {}
        mov ecx, {}

        rep movsb

        pop ecx
        pop esi
        pop edi
        '''.format(dst, src, size)

class x86_64(x86):
    """x86_64 implementation of Arch
    """
    _cs = CS_ARCH_X86, CS_MODE_64
    _ks = KS_ARCH_X86, KS_MODE_64

    def memcpy(self, dst, src, size):
        """memcpy implementation under x86_64 arch
        """
        return '''
        push rdi
        push rsi
        push rcx

        lea rdi, [rip - _PKST_ + {}]
        lea rsi, [rip - _PKST_ + {}]
        mov rcx, {}

        rep movsb

        pop rcx
        pop rsi
        pop rdi
        '''.format(dst, src, size)

class arm(Arch):
    """arm arch is currently not implemented
    """
    # TODO implement arm
    _cs = CS_ARCH_ARM, CS_MODE_ARM
    _ks = KS_ARCH_ARM, KS_MODE_ARM
