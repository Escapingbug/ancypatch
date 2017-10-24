#!/usr/bin/env python

import os
import sys

from ancypatch.core import Patcher
from optparse import OptionParser

def main():
    parser = OptionParser(usage='Usage: run [options] <binary> <patchdir> [patchdir...]')
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true", help="verbose output")

    options, args = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    args = map(os.path.abspath, args)
    patchdirs = args[1:]

    patch = Patcher(args[0], verbose=options.verbose, silent=not options.verbose)
    for d in patchdirs:
        patch.add(d)
    patch.patch()

if __name__ == '__main__':
    main()
