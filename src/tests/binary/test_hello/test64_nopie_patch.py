def patch(pt):
    pt.patch(0x400634, raw='patched\x00')
