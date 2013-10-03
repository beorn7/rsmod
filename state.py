#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Factory functions for dumb data classes to track the state of the game.

This module also provides means to pickle and un-pickle said
classes into and from a human-readable and -editable format.
"""

import base

import collections
import os
import types

from action import *


def _CondSet(o, attr, value):
    if not hasattr(o, attr): setattr(o, attr, value)


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
    _CondSet(o, 'preselected_companies', set())
    _CondSet(o, 'open_companies', False)
    _CondSet(o, 'ascending_companies', False)
    _CondSet(o, 'share_redemption', False)
    _CondSet(o, 'file_root',
             os.path.expanduser(os.path.join(
                '~', 'public_html', 'rollingstock', 'games', o.name)))
    _CondSet(o, 'css_file', '../css/rsmod.css')
    _CondSet(o, 'image_dir', '../img')
    _CondSet(o, 'seed', None)
    return o


def ForeignInvestor(**kwargs):
    """The foreign investor.

    Factory function to create a types.SimpleNamespace object with the
    attributes described below.

    Attributes:
      money (int, default 0): Money in treasury.
      companies (set, default set()): IDs of owned companies.
    """
    o = types.SimpleNamespace(**kwargs)
    _CondSet(o, 'money', 0)
    _CondSet(o, 'companies', set())
    return o


def Player(**kwargs):
    """A player.

    Factory function to create a types.SimpleNamespace object with the
    attributes described below plus all the attributes of the ForeignInvestor.

    Attributes:
      order (int, mandatory): Position in player order (1-based).
      shares (list of int, default base.N_CORPORATIONS*[0]): Number of
        shares for each corporation.
      presidencies (list of bool, default base.N_CORPORATIONS*[False]:
        Whether the player is the president of the respective corporation.
    """
    o = ForeignInvestor(**kwargs)
    assert hasattr(o, 'order')
    _CondSet(o, 'shares', base.N_CORPORATIONS*[0])
    _CondSet(o, 'presidencies', base.N_CORPORATIONS*[False])
    return o


def Corporation(**kwargs):
    """A corporation.

    Factory function to create a types.SimpleNamespace object with the
    attributes described below plus all the attributes of the ForeignInvestor.

    Attributes:
      money_in_flight (int, default 0): Money that will be received at end of
        phase 6.
      companies_in_flight (set, default set()): Set of id's of companies that
        will be received at the end of phase 6.
      done (bool, default False): Whether corporatios has had its turn in phase
        1 or 9.
      price (int, default -1): Share price card held by the corporation (as an
        index in the PRICES tuple, -1 means no card).
      shares (int, defailt 0): Number of shares issued.
    """
    o = ForeignInvestor(**kwargs)
    _CondSet(o, 'money_in_flight', 0)
    _CondSet(o, 'companies_in_flight', set())
    _CondSet(o, 'done', False)
    _CondSet(o, 'price', -1)
    _CondSet(o, 'shares', 0)
    return o


def Phase(**kwargs):
    """A phase of the game.

    A game is tracked in a series of Phase objects. Each translates into a
    separate page in the HTML interface.

    Factory function to create a types.SimpleNamespace object with the
    attributes described below.

    Attributes:
      params (GameParams, mandatory): Paramater for this game.
      turn (int, default 1): Game turn.
      phase (int, default 1): Phase within the turn, {1..9}. Note that phase 10
        as known from the rules is not explicitly represented in the program.
      last_turn (int, default 0): Number of the last turn, 0 if not yet known.
      available (set, default set()): IDs of companies available for auctions.
      unavailable (set, default set()): IDs of companies drawn but not yet
        available for auctions.
      closed (set, default set()): IDs of closed companies.
      deck (list, default []): IDs of companies in the deck.
      foreign_investor (ForeignInvestor, mandatory): The foreign investor.
      players (list of Player, mandatory): The players.
      corporations (list of Corporation, default
        base.N_CORPORATIONS*[Corporation()]): The corporations.
      actions (list of Actions, default []): Action objects that can be
        replayed. A phase tuple is supposed to be persisted when it contains
        the state at the beginning of a phase. By replaying these actions, it
        can be forwarded into any later state during the phase.
      next_action (Action, default None): The next action to execute.
    """
    o = types.SimpleNamespace(**kwargs)
    assert hasattr(o, 'params')
    _CondSet(o, 'turn', 1)
    _CondSet(o, 'phase', 1)
    _CondSet(o, 'last_turn', 0)
    _CondSet(o, 'available', set())
    _CondSet(o, 'unavailable', set())
    _CondSet(o, 'closed', set())
    _CondSet(o, 'deck', [])
    assert hasattr(o, 'foreign_investor')
    assert hasattr(o, 'players')
    _CondSet(o, 'corporations', [Corporation()
                                 for _ in range(base.N_CORPORATIONS)])
    _CondSet(o, 'actions', [])
    _CondSet(o, 'next_action', None)
    return o


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
    
