def patch(pt):
    addr = pt.inject(asm=r'''
    mov eax, [rbp-4];
    movsxd rdx, eax;
    mov rax, [rbp-18];
    add rdx, rax;
    mov [rdx], 0;
    ret;
    ''')

    pt.hook(0xc8b, addr)
