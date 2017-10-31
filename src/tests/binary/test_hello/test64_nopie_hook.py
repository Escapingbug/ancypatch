def patch(pt):
    addr = pt.inject(asm=r'''
        add rdi, 7;
        ret;
    ''')
    pt.hook(0x400595, addr)
