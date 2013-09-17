#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""HTML creation based on a Phase tuple."""

import html
import os

def Write(phase, create_index_link=True):
    """Writes the game state as HTML.

    The file name is derived from phase.params:
    <file_root>/t<turn>p<phase>.html
    The CSS used and the directory for embedded images is determined by
    GameParams, too.
    The function creates <file_root>, if it doesn't exist (but not its
    parent directories). It sets its permissions to 0755.
    The HTML file gets permissions set to 0644, and a link index.html
    to the newly writte file is created. To prevent the latter, set
    create_index_link to False.

    Raises:
      OSError: If file operations go wrong.
    """

    filename = os.path.join(phase.params.file_root,
                            't%dp%d.html' % (phase.turn, phase.phase))
    try:
        os.chmod
