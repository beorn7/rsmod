#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""General utility functions.

These functions make combined use of the state and the base module.
They are still pure, i.e. not object-oriented.
"""

import base


# TODO: test these functions!

def PlayerOrder(players):
    """Returns a list with the indices of the players in player order.

    The order is checked at the time of calling this function. Later changes
    are ignored.
    """
    order = [0] * len(players)
    for i, player in enumerate(players):
        order[player.order-1] = i
    return order


def SharePriceOrder(corporations):
    """Returns an list with the indices of the corporations in share price order.

    The order is checked at the time of calling this function. Later changes
    are ignored.
    """
    return [j for j, _ in
            sorted(((i, corp.price) for i, corp in enumerate(corporations)),
                   key=lambda x: x[1], reverse=True)]


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
      i: 0-based position of the player in the players list in phase.
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
      i: 0-based position of the corporation in the corporations list in phase.
      phase: the Phase named-tuple.
    Returns:
      The total income.
    """
    corp = phase.corporations[i]
    ids = corp.companies | corp.companies_in_flight
    return (base.BaseIncome(ids) - CostOfOwnership(ids, phase)
            + base.SynergyIncome(ids))


def TotalIncomeForeignInvestor(phase):
    """Calculates total income for the foreign investor, including the bonus $5.

    Args:
      phase: the phase object.
    Returns:
      The total income.
    """
    ids = phase.foreign_investor.companies
    return base.BaseIncome(ids) - CostOfOwnership(ids, phase) + 5


def SharePrice(i, phase):
    """Returns the share price of a corporation.

    Args:
      i: 0-based position of the corporation in the corporations list in phase.
      phase: the phase object.
    Returns:
      The share price in $ (not the position in the share price tuple).
     """
    return base.PRICES[phase.corporations[i].price]


def BookValuePlayer(i, phase):
    """Calculates book value for a player.

    Args:
      i: 0-based position of the player in the players list in phase.
      phase: the phase object.
    Returns:
      The book value.
    """
    player = phase.players[i]
    return player.money + sum(player.companies) + sum(
        shares * SharePrice(i, phase) for i, shares in enumerate(player.shares))


def BookValueCorporation(i, phase):
    """Calculates book value for a corporation.

    Args:
      i: 0-based position of the corporation in the corporations list in phase.
      phase: the phase object.
    Returns:
      The book value.
    """
    corp = phase.corporations[i]
    return (corp.money + corp.money_in_flight +
            sum(corp.companies) + sum(corp.companies_in_flight)) 


def MarketCap(i, phase):
    """Calculates market capitalization for a corporation.

    Args:
      i: 0-based position of the corporation in the corporations list in phase.
      phase: the phase.
    Returns:
      The market capitalization.
    """
    return phase.corporations[i].shares * SharePrice(i, phase)


def BankShares(i, phase):
    """Returns number of a corporation's shares owned by the bank.

    Args:
      i: 0-based position of the corporation in the corporations list in phase.
      phase: the phase.
    Returns:
      The number of the corporation's shares owned by the bank.
    """
    return phase.corporations[i].shares - sum(
        p.shares[i] for p in phase.players)


def President(i, players):
    """Returns the index of the player that is the president of a corporation.

    Args:
      i: 0-based position of the corporation in the corporations list in phase.
      players: the players list.
    Returns:
      The index of the player being president in the players list. -1 if none.
    """
    for p, player in enumerate(players):
        if player.presidencies[i]: return p
    return -1 

    
