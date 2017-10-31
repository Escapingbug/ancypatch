def hook(pt):
    # FIXME This shows that the FLAGS register is modified after hook
    addr = pt.inject(asm=r'''
        cmp [rbp-0x4], 0x1;
        ret;
    ''')
    pt.hook(0x674, addr)
