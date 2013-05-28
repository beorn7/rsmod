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
     'preselected_companies', # set of company id's that _must_ be in the mix.
     'open_companies',        # bool
     'share_redemption',      # bool
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
     'presidencies' # list of bools, if president of the respective company.
     )) 

# TODO corps, don't forget DONE status and available money

# A game is tracked in a serious of Phase objects. Each
# translates into a separate page in the HTML interface.
Phase = collections.namedtuple(
    'Phase',
    ('turn',         # int, >0.
     'phase',        # int, between 1 and 9. Phase 10 from the rules is not
                     # explicitly represented.
     'last_turn',    # int, number of the last turn, 0 if not yet known.
     'available',    # set of id's of companies available for auctions.
     'unavailable',  # set of id's of companies drawn but not yet available.
     'closed',       # set of id's of closed companies.
     'deck',         # list of id's of companies in the deck. If the game is
                     # played with open_companies=False, the deck is
                     # reshuffled before drawing.
     'foreign_investor', # A ForeignInvestor tuple.
     'players',      # A list of Player tuples.
     'corporations', # A lest of Corporation tuples.
     'actions',      # TODO
    ))
