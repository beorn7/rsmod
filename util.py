#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""General utility functions.

These functions make combined use of the state and the base module.
They are still pure, i.e. not object-oriented.
"""

import base


# TODO: test these functions!

def TierOnTop(phase):
    """Returns the tier of the card on top of the deck.

    Returns:
      The tier number {0..5} of the card on top of the deck.
      If this is the last turn of the game, 7 is returned.
      If the deck is empty, 6 is returned.
    """
    if phase.turn == phase.last_turn:
        return 7
    elif len(phase.deck):
        return base.COMPANIES[phase.deck[0]].tier
    else:  # Empty deck, but not last turn yet.
        return 6
    

def CostOfOwnership(ids, phase):
    """Calculates cost of ownership for a set of company IDs."""
    result = base.CostOfOwnership(ids, TierOnTop(phase), phase.params.type)
    assert(result >= 0)
    return result


def TotalIncomePlayer(i, phase):
    """Calculates total income for a player.

    Args:
      i: 0-based position of the player in the Phase tuple.
      phase: the Phase named-tuple.
    Returns:
      The total income.
    """
    player = phase.players[i]
    ids = player.companies
    return base.BaseIncome(ids) - CostOfOwnership(ids, phase)


def TotalIncomeCorporation(i, phase):
    """Calculates total income for a corporation.

    Args:
      i: 0-based position of the corporation in the Phase tuple.
      phase: the Phase named-tuple.
    Returns:
      The total income.
    """
    corp = phase.corporations[i]
    ids = corp.companies
    return (base.BaseIncome(ids) - CostOfOwnership(ids, phase)
            + base.SynergyIncome(ids))


def TotalIncomeForeignInvestor(phase):
    """Calculates total income for the foreign investor, including the bonus $5.

    Args:
      phase: the Phase named-tuple.
    Returns:
      The total income.
    """
    ids = phase.foreign_investor.companies
    return base.BaseIncome(ids) - CostOfOwnership(ids, phase) + 5
