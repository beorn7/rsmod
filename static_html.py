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

MONEY_IN_FLIGHT_EXPLANATION = (
    'From company sales. Becomes available at end of phase. Already added to '
    'book value.')

COMPANIES_IN_FLIGHT_EXPLANATION = (
    'Companies just bought. Become available at end of phase. Already taken '
    'into account for book value and income.')


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

    # First a lot of local helper functions.

    def _Header():
        name = 'Game: %s' %  html.escape(phase.params.name)
        t = phase.turn
        p = phase.phase
        turn_and_phase = 'Turn: %d &ndash; Phase: %d (%s)' % (
            t, p, PHASE_NAMES[p])
        lines = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '<meta http-equiv="content-type" content="text/html; '
            'charset=utf-8">',
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

    def _Actions():
        lines = ['<div class="clear-both">',]
        for line in phase.actions + phase.future_actions:
            lines.append('<p>%s</p>' % line)
        lines.append('</div>')
        return "\n".join(lines + [''])
    
    def _Overview():
        players = phase.players
        corps = phase.corporations
        player_order = util.PlayerOrder(players)
        corps_order = util.SharePriceOrder(corps)
        lines = [
            '<h3>Overview</h3>',
            '<p class="small">Players in player order. Corporations in '
            'share price order. '
            'Mouse over corporation symbols and company boxes for details.</p>',
            '<table>',
            '<tr>',
            '<th>name</th>',
            '<th>cash</th>',
            '<th>value</th>',
            '<th>companies</th>',
           ]
        for i in corps_order:
            name = base.CORPORATIONS[i]
            active = phase.corporations[i].price > 0
            lines.append('<th%s>%s<img src="%s-%s30.png" width="30" alt="%s">'
                         '</th>'
                         % (' class="corp"' if active else '',
                            _CorporationDetails(i) if active else '',
                            os.path.join(phase.params.image_dir, name.lower()),
                            '' if active else 'gray-',
                            name))
        lines.append('</tr>')
        for p in player_order:
            name = html.escape(phase.params.players[p])
            player = phase.players[p]
            lines += [
                '<tr>',
                '<td>%s</td>' % name,
                '<td class="num">$%d</td>' % player.money,
                '<td class="num">$%d</td>' % util.BookValuePlayer(p, phase),
                '<td>%s</td>' % _FormatCompanies(player.companies),
                ]
            for c in corps_order:
                lines.append(
                    '<td class="num">%s%s</td>' %
                    ('*' if player.presidencies[c] else '',
                     player.shares[c] or '&ndash;'))
            lines.append('</tr>')
        lines += [
            '<tr>',
            '<td class="top-border" colspan=3></td>',
            '<td class="solid-border">Shares owned by bank</td>',
            ]
        for c in corps_order:
            lines.append('<td class="solid-border">%s</td>' %
                         (util.BankShares(c, phase) or '&ndash;'))
        lines += [
            '</tr>',
            '<tr>',
            '<td class="no-border" colspan=3></td>',
            '<td class="solid-border">Shares issued in total</td>',
            ]
        for c in corps_order:
            lines.append('<td class="solid-border">%s</td>' %
                         (phase.corporations[c].shares or '&ndash;'))
        lines += [
            '</tr>',
            '<tr>',
            '<td class="no-border" colspan=3></td>',
            '<td class="solid-border">Share price</td>',
            ]
        for c in corps_order:
            lines.append('<td class="solid-border">%s</td>' %
                         ('$'+str(util.SharePrice(c, phase))
                          if phase.corporations[c].price > 0
                          else '&ndash;'))
        lines += [
            '</tr>',
            '<tr>',
            '<td class="no-border" colspan=3></td>',
            '<td class="solid-border">Cash</td>',
            ]
        for c in corps_order:
            corp = phase.corporations[c]
            lines.append('<td class="solid-border">%s</td>' %
                         ('$'+str(corp.money)
                          if corp.price > 0
                          else '&ndash;'))
        if phase.phase == 6:
            lines += [
                '</tr>',
                '<tr title="%s">' % MONEY_IN_FLIGHT_EXPLANATION,
                '<td class="no-border" colspan=3></td>',
                '<td class="solid-border">Cash “in flight”</td>',
                ]
            for c in corps_order:
                corp = phase.corporations[c]
                lines.append('<td class="solid-border">%s</td>' %
                             ('$'+str(corp.money_in_flight)
                              if corp.price > 0
                              else '&ndash;'))
        lines += [
            '</tr>',
            '<tr>',
            '<td class="no-border" colspan=3></td>',
            '<td class="solid-border">Income</td>',
            ]
        for c in corps_order:
            corp = phase.corporations[c]
            lines.append('<td class="solid-border">%s</td>' %
                         (_FormatDelta(util.TotalIncomeCorporation(c, phase))
                          if corp.price > 0
                          else '&ndash;'))
        lines += [
            '</tr>',
            '<tr>',
            '<td class="no-border" colspan=3></td>',
            '<td class="solid-border">Book value</td>',
            ]
        for c in corps_order:
            corp = phase.corporations[c]
            lines.append('<td class="solid-border">%s</td>' %
                         ('$'+str(util.BookValueCorporation(c, phase))
                          if corp.price > 0
                          else '&ndash;'))
        lines += [
            '</tr>',
            '<tr>',
            '<td class="no-border" colspan=3></td>',
            '<td class="solid-border">Market capitalization</td>',
            ]
        for c in corps_order:
            corp = phase.corporations[c]
            lines.append('<td class="solid-border">%s</td>' %
                         ('$'+str(util.MarketCap(c, phase))
                          if corp.price > 0
                          else '&ndash;'))
        lines += [
            '</tr>',
            '</table>',
            ]   
        return "\n".join(lines + [''])
    
    def _SharePriceRow():
        lines = [
            '<h3>Share price row</h3>',
            '<table>',
            '<tr>',
            ]
        for price in base.PRICES[1:]:
            lines.append('  <td class="centered-num">%d</td>' % price)
        lines += [
            '</tr>',
            '<tr>',
            ]
        # Make a map: share price -> corp name.
        corp_at_price = {
            base.PRICES[corp.price]: name
            for name, corp in zip(base.CORPORATIONS, phase.corporations)
            if corp.price > 0
            }
        for price in base.PRICES[1:]:
            if price in corp_at_price:
                corp = corp_at_price[price]
                lines.append(
                    '  <td class="sharepricerow">'
                    '<img src="%s-20.png" width="20" alt="%s"></td>' %
                    (os.path.join(phase.params.image_dir, corp.lower()), corp))
            else:
                lines.append('  <td class="sharepricerow"></td>')
        lines.append('</tr>')
        for tier, (start, end) in enumerate(base.PRICE_RANGES):
            if tier > base.MAX_TIER[phase.params.type]:
                break
            lines += [
                '<tr>',
                '<td colspan="%d" class="solid-border"></td>' % (start-1),
                '<td colspan="%d" class="%s-cell"></td>' %
                (end-start+1, COMPANY_CLASS[tier]),
                '<td colspan="%d" class="solid-border"></td>' % (31-end),
                '</tr>',
                ]
        lines.append('</table>')
        return "\n".join(lines + [''])
    
    def _Deck():
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
    
    def _ForeignInvestor():
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
           _FormatCompanies(phase.foreign_investor.companies)))
    
    def _CorporationDetails(i):
        corp = phase.corporations[i]
        cash = '$%s' % corp.money
        president = util.President(i, phase.players)
        all_companies = corp.companies | corp.companies_in_flight
        if corp.money_in_flight:
            cash += ' <span title="%s">(+$%d)</span>' % (
                MONEY_IN_FLIGHT_EXPLANATION, corp.money_in_flight)
        lines = [
            '<div class="tooltip-corp">',
            '<table class="tooltip-corp">',
            '<tr><th>President</th><th>Cash</th><th>Shares</th></tr>',
            '<tr><td>%s</td>' % (html.escape(phase.params.players[president])
                                 if president > -1 else 'NONE'),
            '<td>%s</td>' % cash,
            '<td>%d</td></tr></table>' % corp.shares,
            '<table class="tooltip-corp">',
            '<tr><th colspan="4">Income</th></tr>',
            '<tr><th>Base</th><th>Synergy</th><th>Cost</th>'
            '<th class="emph">Total</th></tr>',
            '<tr><td>%s</td>' %  _FormatDelta(base.BaseIncome(all_companies)),
            '<td>%s</td>' % _FormatDelta(base.SynergyIncome(all_companies)),
            '<td>%s</td>' % _FormatDelta(-base.CostOfOwnership(
                    all_companies, util.TierOnTop(phase), phase.params.type)),
            '<td class="emph">%s</td>' %
            _FormatDelta(util.TotalIncomeCorporation(i, phase)),
            '</tr></table>',
            '<table class="tooltip-corp">',
            '<tr><th>Companies</th></tr>',
            '<tr><td>%s</td></tr>' % _FormatCompanies(corp.companies, corp),
            '</table>',
            ]
        if corp.companies_in_flight:
            lines += [
                '<table class="tooltip-corp">',
                '<tr><th title="%s">Companies “in flight”</th></tr>' %
                COMPANIES_IN_FLIGHT_EXPLANATION,
                '<tr><td>%s</td></tr>' %
                _FormatCompanies(corp.companies_in_flight, corp),
                '</table>',
            ]
        lines += [
            '</div>',
            ]
        # TODO share price, max payout, book value
        # market cap(?), what's needed to jump to where
        return "\n".join(lines + [''])
     
    def _Footer():
        # Leave space for tooltips.
        return '<div style="height:100px"></div></body>\n</html>\n'
     
    def _FormatCompanyHover(company, corporation=None):
      return '<div class="%s">%s[%d]<div class="tooltip">%s</div></div>' % (
          COMPANY_CLASS[base.COMPANIES[company].tier] + "-hover",
          base.COMPANIES[company].abbreviation, company,
          _FormatCompanyDetail(company, corporation))
    
    def _FormatCompanyDetail(company, corporation=None):
        return ('<h4>%s</h4>'
                '<div class="%s" title="%s">%s[%d] ($%d&ndash;$%d) %s</div>'
                '<br>%s' % (
                base.COMPANIES[company].name,
                COMPANY_CLASS[base.COMPANIES[company][0]],
                base.COMPANIES[company].name,
                base.COMPANIES[company].abbreviation, company,
                base.MinPrice(company), base.MaxPrice(company),
                _FormatDelta(base.COMPANIES[company].income),
                _FormatSynergies(company, corporation)))
     
    def _FormatCompanies(companies, corporation=None):
        if isinstance(companies, set):
            companies = sorted(companies)
        return (' '.join(_FormatCompanyHover(company, corporation)
                         for company in companies)
                if companies else '&ndash;')
     
    def _FormatSynergies(company, corporation=None):
        parts = []
        for bonus, companies in sorted(base.Synergies(company).items()):
            inner_parts = []
            for i in sorted(companies):
                if base.COMPANIES[i].tier > base.MAX_TIER[phase.params.type]:
                    continue
                inner_parts.append(_FormatCompany(
                        i, corporation is not None
                        and i in corporation.companies))
            if inner_parts:
                parts.append('<li><div class="%s">%s:</div>'
                             '&nbsp;%s</li>' %
                             (SYNERGY_CLASS[bonus],
                              _FormatDelta(bonus),
                              '&nbsp;'.join(inner_parts)))
        return '<ul class="synergies">%s</ul>' % '\n'.join(parts)


    if os.path.isdir(phase.params.file_root):
        os.chmod(phase.params.file_root, 0o755)
    else:
        os.mkdir(phase.params.file_root, 0o755)

    filename = os.path.join(phase.params.file_root,
                            't%dp%d.html' % (phase.turn, phase.phase))
    mode = 'w' if overwrite_existing else 'x'
    with open(filename, mode) as fd:
        fd.write(_Header())
        fd.write(_Actions())
        fd.write(_Overview())
        fd.write(_SharePriceRow())
        fd.write(_Deck())
        fd.write(_ForeignInvestor())
        fd.write(_Footer())
    os.chmod(filename, 0o644)
    index_filename = os.path.join(phase.params.file_root, 'index.html')
    if create_index_link:
        if os.path.islink(index_filename):
            os.remove(index_filename)
        os.symlink(filename, index_filename)


# The following helper functions don't need the closure of WriteHtml(),
# so we keep things a bit cleaner and have them top-level.

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
    
    
