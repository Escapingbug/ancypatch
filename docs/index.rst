.. ancypatch documentation master file, created by
   sphinx-quickstart on Thu Oct 19 19:21:49 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ancypatch's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. module:: core.context

.. autoclass:: Context

   .. automethod:: asm(asm, addr, att_syntax=False)
   .. automethod:: dis(addr, size=64)
   .. automethod:: disiter(addr)
   .. automethod:: irdis(addr, size=64)
   .. automethod:: irstream(addr)
   .. automethod:: ir(asm, \*\*kwargs)
   .. automethod:: make_writable(addr)
   .. automethod:: search(data)
   .. automethod:: hook(src, dst, first=False, noentry=False)
   .. automethod:: inject([internal, is_asm, mark_func, size, target, desc])
   .. automethod:: patch(desc[, is_asm])
   .. automethod:: resolve(sym)
   .. automethod:: declare(symbols=None, headers='', source='')
   .. automethod:: final(cb)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
