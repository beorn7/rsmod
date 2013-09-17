#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Creation of static HTML based on a Phase tuple."""

import html
import os

import util

PHASE_NAMES = {  # TODO: i18n.
    1: 'issue shares',
    2: 'form corporations',
    3: 'share trading and auctions',
    4: 'determine new player order',
    5: 'foreign investor buys companies',
    6: 'corporations buy companies',
    7: 'close companies',
    8: 'income',
    9: 'pay dividends and adjust share prices',
}

def WriteHtml(phase, create_index_link=True, overwrite_existing=False):
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

    Existing files will only be overwritten if overwrite_existing is set to
    True. (Otherwise, OSError is raised.)

    Raises:
      OSError: If file operations go wrong.
    """

    if os.path.isdir(phase.params.file_root):
        os.chmod(phase.params.file_root, 0o755)
    else:
        os.mkdir(phase.params.file_root, 0o755)

    filename = os.path.join(phase.params.file_root,
                            't%dp%d.html' % (phase.turn, phase.phase))
    mode = 'w' if overwrite_existing else 'x'
    with open(filename, mode) as fd:
        fd.write(_Header(phase))
        fd.write(_Actions(phase))
        fd.write(_Overview(phase))
        fd.write(_SharePriceRow(phase))
        fd.write(_Deck(phase))
        fd.write(_ForeignInvestor(phase))
        fd.write(_Footer())
    os.chmod(filename, 0o644)
    index_filename = os.path.join(phase.params.file_root, 'index.html')
    if create_index_link:
        if os.path.islink(index_filename):
            os.remove(index_filename)
        os.symlink(filename, index_filename)


def _Header(phase):
    name = 'Game: %s' %  html.escape(phase.params.name)
    t = phase.turn
    p = phase.phase
    turn_and_phase = 'Turn: %d &ndash; Phase: %d (%s)' % (
        t, p, PHASE_NAMES[p])
    lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta http-equiv="content-type" content="text/html; charset=utf-8">',
        '<title>Rolling Stock &ndash; %s &ndash; %s</title>' %
        (name, turn_and_phase),
        '<link rel="stylesheet" type="text/css" href="%s">' %
        html.escape(phase.params.css_file),
        '<link rel="icon" type="image/png" href="%s/rabe.png">' %
        html.escape(phase.params.image_dir),
        '</head>',
        '<body>',
        '<h1>Rolling Stock &ndash; %s ' % name,
        '<span class="tooltip-parent">',
        '<img src="%s/info.png" alt="info">' %
        html.escape(phase.params.image_dir),
        '<div class="tooltip"><h4>Game variants used</h4>',
        '<dl>',
        '<dt>Type</dt><dd>%s</dd>' % phase.params.type,
        '<dt>Open company deck</dt><dd>%s</dd>' %
        _FormatBoolean(phase.params.open_companies),
        '<dt>Companies in ascending order</dt><dd>%s</dd>' %
        _FormatBoolean(phase.params.ascending_companies),
        '<dt>Share redemption allowed</dt><dd>%s</dd>' %
        _FormatBoolean(phase.params.share_redemption),
        '</dl>',
        '</div></span>',
        '</h1>',
        '<h2>%s</h2>' % turn_and_phase,
        '<div class="left">',
        '  <a class="nav" href="t1p1.html">&#8676;start</a>',
        '  <a class="nav" href="t%dp%d.html">&#8606;previous turn</a>' %
        (t-1 if t > 1 else 1, p),
        '  <a class="nav" href="t%dp%d.html">&#8592;previous phase</a>' %
        (t if p > 1 else (t-1 if t > 1 else 1),
         p-1 if p > 1 else (9 if t > 1 else 1)),
        '</div>',
        '<div class="right">',
        '  <a class="nav" href="t%dp%d.html">next phase&#8594;</a>' %
        (t if p < 9 else t+1, p+1 if p < 9 else 1),
        '  <a class="nav" href="t%dp%d.html">next turn&#8608;</a>' %
        (t+1, p),
        '  <a class="nav" href="index.html">latest move&#8677;</a>',
        '</div>',
        '<div class="clear-both">',
        ]
    for line in phase.actions + phase.future_actions:
        lines.append('<p>%s</p>' % line)
    lines.append('</div>')
    return "\n".join(lines + [''])


def _Actions(phase):
    lines = []
    
    return "\n".join(lines + [''])


def _Overview(phase):
    lines = [
        '<h3>Overview</h3>',
        '<p>(players in player order)</p>',
        ]
    
    return "\n".join(lines + [''])


def _SharePriceRow(phase):
    lines = []
    
    return "\n".join(lines + [''])


def _Deck(phase):
    lines = []
    # TODO (include preselected companies)
    return "\n".join(lines + [''])


def _ForeignInvestor(phase):
    fi = phase.foreign_investor
    return ("""\
<h3>Foreign investor</h3>
<ul>
  <li>Treasury: $%d</li>
  <li>Income: %s</li>
  <li>Companies: %s</li>
</ul>
""" % (fi.money, util.TotalIncomeForeignInvestor(phase), "TODO"))

def _Footer():
    return "</body>\n</html>\n"


def _FormatBoolean(b):
    return 'yes' if b else 'no'
