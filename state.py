#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Dumb data classes to track the state of the game.

This module also provides means to pickle and un-pickle said
classes into and from a human-readable and -editable format.
"""

import collections

# Things that are set at game start and never change.
GameParams = collections.namedtuple(
    'GameParams',
    ('name',                  # Name of the game.
     'players',               # Sequence of player names.
     'type',                  # One of 'training', 'short', 'full'.
     'preselected_companies', # Set of company id's that _must_ be in the mix.
     'open_companies',        # bool
     'ascending_companies',   # bool (whether companies in the deck are sorted).
     'share_redemption',      # bool
     'file_root',             # Directory for game state and HTML files.
     'css_file',              # As used in HTML. May be relative to file_root.
     'image_dir',             # As used in HTML. May be relative to file_root.
     'seed',                  # For random number generator. int or None.
    ))

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
     'actions',      # For now just a list of strings describing the actions
                     # performed in this phase. (This phase tuple contains the
                     # state after these actions have been applied.) Later,
                     # this list will contain action objects that can be
                     # replayed. The phase tuple will then contain the state at
                     # the beginning of a phase.
    ))
