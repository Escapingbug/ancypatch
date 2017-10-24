# ancypatch
----------
A forked verson of origial patchkit, means to be more easy to install and contains more documentation.

Patches an ELF binary using one or more simple Python scripts.

Usage:

    ancypatch <binary> <patchdir|file> [patchdir|file...]


# patchdir
----
Contains one or more Python patch files, which will be executed in alphabetical order against a binary.


# Patch Examples
----

Nopping an address, injecting an assembly function, and hooking the entry point:

    def simple_patch(pt):
        # nop out a jump at the entry point
        pt.patch(pt.entry, hex='90' * 5)

        # inject assembly into the binary and return the address
        addr = pt.inject(asm='mov eax, 1; ret')

        # hook the entry point to make it call addr (ret will run the original entry point)
        pt.hook(pt.entry, addr)

Replacing a C function:

    def replace_free(pt):
        # pretend free() is at this address:
        old_free = 0x804fc4

        # inject a function to replace free()
        new_free = pt.inject(c=r'''
        void free_stub(void *addr) {
            printf("stubbed free(%p)\n", addr);
        }
        ''')

        # patch the beginning of free() with a jump to our new function
        pt.patch(old_free, jmp=new_free)


API
----

see [documentation page](http://anciety.cn/ancypatch/index.html)

# IDA scripts
----
Some scripts live in the ida/ path. Run them like this:

    /Applications/IDA\ Pro\ 6.8/idaq.app/Contents/MacOS/idaq64 -A -Sida/allfuncs.py a.out

When invoked like this, allfuncs.py will generate `a.out.funcs` which is used by hardening scripts.


# Tools
----
These are somewhat CGC and x86-specific right now, but will be ported for general use in the future.

- explore: uses a Python CFG and recursive backtracking emulator to find basic blocks in an executable, used as `ancyexplore`
- bindiff: uses the block boundaries from an explore run, as well as additional analysis to find and output basic block diffs between two binaries, used as `ancybindiff`


# Installation
----
(This is about to change shortly. I'm doing surgery on this for now)

## Simple form
simple installation via pip:
```
pip install ancypatch
```

## Manually


```
# Run `./deps.sh` to automatically install these.
#   - Capstone Engine - https://github.com/aquynh/capstone.git
#   - Keystone Engine - https://github.com/keystone-engine/keystone.git
#   - Unicorn Engine  - https://github.com/unicorn-engine/unicorn.git
./deps.sh

# after installation of the dependencies, we can now install ancypatch
python setup.py install

echo "now we can use ancypatch, ancybindiff, ancyrun and ancyexplore :) Have fun."
```
 

Notice
-------
This project has just been forked, some documentation may be wrong since the code is a little bit tricky to read, truly. And I feel sorry when I make mistakes, you are welcome to raise an issue if that happens. :)
