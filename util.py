#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""General utility functions.

These functions make combined use of the state and the base module.
They are still pure, i.e. not object-oriented.
"""

import base


def CostOfOwnership(ids, phase):
    """Calculates cost of ownership for a set of company IDs."""
    if phase.turn == phase.last_turn:
        tier_on_top = 7
    elif len(phase.deck):
        tier_on_top = base.COMPANIES[phase.deck[0]].tier
    else:  # Empty deck, but not last turn yet.
        tier_on_top = 6
    result = base.CostOfOwnership(ids, tier_on_top, phase.params.type)
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
