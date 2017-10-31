def patch(pt):
    pt.patch(0x6f4, raw='patched\x00')
