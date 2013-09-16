#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Factory function to set-up new games."""

import base
import state

def MakePhase(params):
  """Creates and returns an initial Phase tuple from a GameParams tuple.

  Returns: The Phase tuple for turn 1, phase 1 of the new game.

  Raises:
    ValueError: If invalid input values are encountered.
  """
  phase = state.Phase(
      params=params,
      turn=1,
      phase=1,
      last_turn=0,
      available=set(),  # Will be populated below.
      unavailable=set(),
      deck=set(),  # Will be populated below.
      closed=set(),
      foreign_investor=state.ForeignInvestor(money=4, companies=set()),
      players=[],  # Will be populated below.
      corporations=[],  # Will be populated below.
      actions=[])
  # TODO; populate available, deck, players, corporations
  return phase  

