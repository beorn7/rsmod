#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Creation of static HTML based on a Phase tuple.

This is pretty messy ad-hoc HTML generation. It should use some form of
template framework... But since all the HTML is supposed to be generated
dynamically for the real online play, this will go away at some point anyway.
"""

import html
import os

import base
import util

COMPANY_CLASS = {
    0: 'red',
    1: 'orange',
    2: 'yellow',
    3: 'green',
    4: 'blue',
    5: 'purple'
}

SYNERGY_CLASS = {
    1: 'red',
    2: 'orange',
    4: 'yellow',
    8: 'blue',
   16: 'purple'
}

PHASE_NAMES = {
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
        fd.write(_CorporationDetails(phase))
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
        '<div class="h1">Rolling Stock &ndash; %s ' % name,
        '<div class="tooltip-parent">',
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
        '<dt>Preselected companies</dt><dd>%s</dd>' %
        _FormatCompanies(phase.params.preselected_companies)
        if phase.params.preselected_companies else "none",
        '</dl>',
        '</div></div></div>',
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
        ]
    return "\n".join(lines + [''])


def _Actions(phase):
    lines = ['<div class="clear-both">',]
    for line in phase.actions + phase.future_actions:
        lines.append('<p>%s</p>' % line)
    lines.append('</div>')
    return "\n".join(lines + [''])


def _Overview(phase):
    lines = [
        '<h3>Overview</h3>',
        '<p>(players in player order, corporations in share price order)</p>',
        ]
    # TODO (link to anchor for corps or tooltips)
    return "\n".join(lines + [''])


def _SharePriceRow(phase):
    lines = [
        '<h3>Share price row</h3>',
        '<table>',
        '<tr>',
        ]
    for price in base.PRICES[1:]:
        lines.append('  <td class="centered-num">%d</td>\n' % price)
    lines += [
        '</tr>',
        '<tr>',
        ]
    # Make a map: share price -> corp name.
    corp_at_price = {
        (base.PRICES[corp.price], name)
        for name, corp in zip(base.CORPORATIONS, phase.corporations)
        if corp.price > 0
        }
    for price in base.PRICES[1:]:
        lines.append('  <td class="sharepricerow">')
        if price in corp_at_price:
            corp = corp_at_price[price]
            lines.append(
                '    <img src="%s-20.png" width="20" alt="%s">' %
                (os.path.join(phase.params.image_dir, corp.lower()), corp))
        lines.append('  </td>')
    lines += [
        '</tr>',
        '</table>',
        ]
    # TODO (link to anchor for corps or tooltips)
    return "\n".join(lines + [''])


def _Deck(phase):
    params = phase.params
    deck = phase.deck
    lines = [
        '<h3>Company deck</h3>',
        '<ul>',
        '<li>Available for auctions: %s</li>' %
        _FormatCompanies(phase.available),
        '<li>Drawn but not available for auctions: %s</li>' %
        _FormatCompanies(phase.unavailable),
        '<li>In the deck: ',
        ]
    if params.open_companies:
        lines.append(_FormatCompanies(deck))
    else:
        lines.extend('<span class="%s">&nbsp;</span>' %
                     COMPANY_CLASS[base.COMPANIES[id].tier]
                     for id in deck)
    lines.append(' <span class="card">%s game end card</span></li>' %
                 ('flipped' if phase.last_turn == phase.turn else ''))
    if not params.open_companies:
        preselected_still_in_deck = params.preselected_companies & set(deck)
        if preselected_still_in_deck:
            lines.append('<li>Preselected companies in deck: %s</li>'%
                         _FormatCompanies(preselected_still_in_deck))
    lines.append('<li>Cost of ownership:')
    cost = base.COST[params.type][util.TierOnTop(phase)]
    for tier in range(cost.max_affected_tier+1):
        lines.append(' <span class="%s">-$%d</span>' %
                     (COMPANY_CLASS[tier], cost.cost))
    if not cost.cost:
        lines.append(' none')
    lines += [
        '</li>',
        '<li>Closed companies:  %s </li>' % _FormatCompanies(phase.closed),
        '</ul>',
        ]
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
""" % (fi.money,
       _FormatDelta(util.TotalIncomeForeignInvestor(phase)),
       _FormatCompanies(phase.foreign_investor.companies,
                        max_tier=base.MAX_TIER[phase.params.type])))


def _CorporationDetails(phase):
    corps = phase.corporations
    if not any(corp.shares for corp in corps):
        return ""
    lines = [
        '<h3>Corporation details (in share price order)</h3>',
        ]
    # TODO (add anchors to jump to corp, only put open corps here)
    # or use tooltips instead of this
    return "\n".join(lines + [''])


def _Footer():
    return "</body>\n</html>\n"


def _FormatBoolean(b):
    return 'yes' if b else 'no'


def _FormatDelta(delta):
  if delta >= 0:
    return '+$%d' % delta
  return '<span class="loss">-$%d</span>' % -delta


def _FormatCompany(company, active=False):
  return '<div class="%s" title="%s" %s>%s[%d]</div>' % (
      COMPANY_CLASS[base.COMPANIES[company].tier],
      base.COMPANIES[company].name,
      'style="border: 3px solid black"' if active else '',
      base.COMPANIES[company].abbreviation, company)


def _FormatCompanyHover(company, corporation=None, max_tier=5):
  return '<div class="%s">%s[%d]<div class="tooltip">%s</div></div>' % (
      COMPANY_CLASS[base.COMPANIES[company].tier] + "-hover",
      base.COMPANIES[company].abbreviation, company,
      _FormatCompanyDetail(company, corporation, max_tier))


def _FormatCompanyDetail(company, corporation=None, max_tier=5):
    return ('<h4>%s</h4>'
            '<div class="%s" title="%s">%s[%d] ($%d&ndash;$%d) %s</div>'
            '<br>%s' % (
            base.COMPANIES[company].name,
            COMPANY_CLASS[base.COMPANIES[company][0]],
            base.COMPANIES[company].name,
            base.COMPANIES[company].abbreviation, company,
            base.MinPrice(company), base.MaxPrice(company),
            _FormatDelta(base.COMPANIES[company].income),
            _FormatSynergies(company, corporation, max_tier)))


def _FormatCompanies(companies, corporation=None, max_tier=5):
    if isinstance(companies, set):
        companies = sorted(companies)
    return (' '.join(_FormatCompanyHover(company, corporation, max_tier)
                     for company in companies)
            if companies else '&ndash;')


def _FormatSynergies(company, corporation=None, max_tier=5):
    parts = []
    for bonus, companies in sorted(base.Synergies(company).items()):
        inner_parts = []
        for i in sorted(companies):
            if base.COMPANIES[i].tier > max_tier:
                continue
            inner_parts.append(_FormatCompany(
                    i, corporation is not None and i in corporation.companies))
        if inner_parts:
            parts.append('<li><div class="%s">%s:</div>'
                         '&nbsp;%s</li>' %
                         (SYNERGY_CLASS[bonus],
                          _FormatDelta(bonus),
                          '&nbsp;'.join(inner_parts)))
    return '<ul class="synergies">%s</ul>' % '\n'.join(parts)

