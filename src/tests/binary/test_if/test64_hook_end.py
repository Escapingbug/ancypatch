def patch(pt):
    addr = pt.inject(asm=r'''
        ret
    ''')
    pt.hook(0x65d, addr)
