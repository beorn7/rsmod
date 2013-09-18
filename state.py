#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Factory functions for dumb data classes to track the state of the game.

This module also provides means to pickle and un-pickle said
classes into and from a human-readable and -editable format.
"""

import collections
import os
import types


def GameParams(**kwargs):
    """ Things that are set at game start and never change.

    Factory function to create a types.SimpleNamespace object with the
    attributes described below.

    Attributes:
      name (string, mandatory): name of the game.
      players (sequence of strings, mandatory): player names.
      type (string, mandatory): one of 'training', 'short', 'full'.
      preselected_companies (set, default set()): company id's that must be in
        the mix.
      open_companies (bool, default false): whether company deck is open.
      ascending_companies (bool, default false): whether companies in deck are
        sorted (rather than random).
      share_redemption (bool, default false): whether share redemption is
        allowed.
      file_root (string, default "~/public_html/rollingstock/games/<name>"):
        directory for game state and HTML files.
      css_file (string, default "../css/rsmod.css"): CSS file to use in HTML.
        May be relative to file_root.
      image_dir (string, default "../img": image directory to use in HTML.
        May be relative to file_root.
      seed (int, default None): seed for the random number generator.
    """
    o = types.SimpleNamespace(**kwargs)
    assert hasattr(o, 'name')
    assert hasattr(o, 'players')
    assert hasattr(o, 'type')
    assert o.type in ('training', 'short', 'full')
    if not hasattr(o, 'preselected_companies'):
        o.preselected_companies = set()
    if not hasattr(o, 'open_companies'):
        o.open_companies = False
    if not hasattr(o, 'ascending_companies'):
        o.ascending_companies = False
    if not hasattr(o, 'share_redemption'):
        o.share_redemption = False
    if not hasattr(o, 'file_root'):
        o.file_root = os.path.exanduser(os.path.join(
                '~', 'public_html', 'rollingstock', 'games', o.name))
    if not hasattr(o, 'css_file'):
        o.css_file = '../css/rsmod.css'
    if not hasattr(o, 'image_dir'):
        o.image_dir = '../img'
    if not hasattr(o, 'seed'):
        o.seed = None
    return o


ForeignInvestor = collections.namedtuple(
    'ForeignInvestor',
    ('money',     # int
     'companies', # set of id's
    ))

Player = collections.namedtuple(
    'Player',
    ForeignInvestor._fields +
    ('order',       # Player order, as int, 1-based.
     'shares',      # list of ints, number of shares for each company.
     'presidencies' # list of bools, whether president of the respective company.
     )) 

Corporation = collections.namedtuple(
    'Corporation',
    ForeignInvestor._fields +
    ('money_in_flight',       # Money that will be received at end of phase 6.
     'companies_in_flight',   # Set of id's of companies that will be received
                              # at the end of phase 6.
     'done',                  # Bool. Company has had its turn in phase 1 or 9.
     'price',                 # Share price card (as index in the PRICES tuple).
     'shares',                # Number of shares issued.
     ))

# A game is tracked in a series of Phase objects. Each
# translates into a separate page in the HTML interface.
Phase = collections.namedtuple(
    'Phase',
    ('params',       # A GameParams tuple.
     'turn',         # int, >0.
     'phase',        # int, between 1 and 9. Phase 10 from the rules is not
                     # explicitly represented.
     'last_turn',    # int, number of the last turn, 0 if not yet known.
     'available',    # set of id's of companies available for auctions.
     'unavailable',  # set of id's of companies drawn but not yet available.
     'closed',       # set of id's of closed companies.
     'deck',         # list of id's of companies in the deck.
     'foreign_investor', # A ForeignInvestor tuple.
     'players',      # A list of Player tuples.
     'corporations', # A list of Corporation tuples.
     'actions',      # For now just a list of HTML strings describing the actions
                     # performed in this phase. (This phase tuple contains the
                     # state after these actions have been applied.) Later,
                     # this list will contain action objects that can be
                     # replayed. The phase tuple will then contain the state at
                     # the beginning of a phase.
     'future_actions', # In phases with predictable order, this may be filled
                     # with HTML hints for the players (so that they see who is up).
    ))

def SavePhase(phase, overwrite_existing=False):
    """Saves the Phase tuple to a file.

    The file is created in file_root with the pattern t<x>p<y>.py for its name,
    where x is the turn number and p the phase number.

    Existing files will only be overwritten if overwrite_existing is set to
    True. (Otherwise, OSError is raised.)

    Raises:
      OSError: If any file operation fails.
    """
    filename = os.path.join(phase.params.file_root,
                            't%dp%d.py' % (phase.turn, phase.phase))
    mode = 'w' if overwrite_existing else 'x'
    with open(filename, mode) as fd:
        fd.write(str(phase))
        fd.write('\n')

def RestorePhase(filename):
    """Restores a Phase tuple from the named file.

    Returns:
      The restored Phase tuple.
    Raises:
      OSError: If any file operation fails.
    """
    with open(filename, 'r') as fd:
        code = fd.read()
    namespace = types.SimpleNamespace
    phase = eval(code)
    return phase
    
