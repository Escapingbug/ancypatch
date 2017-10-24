import stdlib
import heap
import crypto

__all__ = ['declare']

def declare(linker):
    stdlib.declare(linker)
    heap.declare(linker)
    crypto.declare(linker)
