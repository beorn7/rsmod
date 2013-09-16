#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Factory function to set-up new games."""

import random

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
      deck=[],  # Will be populated below.
      closed=set(),
      foreign_investor=state.ForeignInvestor(money=4, companies=set()),
      players=[],  # Will be populated below.
      corporations=[],  # Will be populated below.
      actions=[])

  random.seed(params.seed)
  number_of_players = len(params.players)
  
  for tier in range(len(base.TIERS)):
      preselected_in_tier = {id for id in params.preselected_companies
                             if base.COMPANIES[id].tier == tier}
      number_in_tier = base.NumberOfCompanies(number_of_players, tier,
                                              params.type)
      still_to_draw = number_in_tier - len(preselected_in_tier)
      if still_to_draw < 0:
          raise ValueError('Too many preselected companies for tier %d. '
                           'Max allowed: %d. Preselected: %d.' %
                           (tier, number_in_tier, len(preselected_in_tier)))
      remaining_in_tier = {id for id, c in base.COMPANIES.items()
                           if c.tier == tier and id not in preselected_in_tier}
      selected_in_tier = list(preselected_in_tier) + random.sample(
          remaining_in_tier, still_to_draw)
      if params.ascending_companies:
          selected_in_tier.sort()
      else:
          random.shuffle(selected_in_tier)
      phase.deck += selected_in_tier
  # Draw initial companies from deck.
  for _ in range(number_of_players):
      phase.available.add(phase.deck.pop(0))
      
  # TODO; populate players, corporations
  return phase  

