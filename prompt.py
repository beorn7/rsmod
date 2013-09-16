#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Command prompt interface.

Games can be run and managed by calling functions at a command prompt.
This is the most low-level interface and intended to be used for
experimental features and for fixes and manipulations the more
high-level interfaces won't allow.
"""

import __main__
import code

# Add tab completion if readline is available.
try:
    import readline
except ImportError:
    pass
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

BANNER = """
TODO: A helpful message how to create and load games.
"""


if __name__ == '__main__':
    code.interact(banner=BANNER, local=__main__.__dict__)

