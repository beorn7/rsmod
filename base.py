#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Base parameters and closely related utility functions.

Everything in this module is supposed to be 'pure', i.e. it does not
depend on the game state.
"""

import collections

# Raw tuple of the share price row.
PRICES = (  0,  5,  6,  7,  8,  9, 10, 11,
           12, 13, 14, 15, 16, 18, 20, 22,
           24, 26, 28, 31, 34, 37, 41, 45,
           50, 55, 60, 66, 73, 81, 90, 100)

# Tier names.
TIERS = (
  'red',
  'orange',
  'yellow',
  'green',
  'blue',
  'purple'
  )

# First and last share price allowed as start price per tier
# (expressed as index in PRICES).
PRICE_RANGES = (
  ( 6, 10),
  ( 6, 14),
  ( 6, 17),
  (11, 20),
  (15, 23),
  (18, 23)
  )

# Corporation names.
CORPORATIONS = (
  'Android',
  'Bear',
  'Eagle',
  'Horse',
  'Jupiter',
  'Orion',
  'Saturn',
  'Ship',
  'Star',
  'Wheel'
)

N_CORPORATIONS = len(CORPORATIONS)

# 'synergies' is a tuple of synergies with lower id's.
Company = collections.namedtuple('Company',
                                 'tier income synergies abbreviation name')

# Companies map, mapping id (== face value) to a Company namedtuple.
COMPANIES = {
  # Red
    1: Company(0,  1, (), 'BME',
               'Bergisch-Märkische Eisenbahn-Gesellschaft'),
    2: Company(0,  1, (), 'BSE',
               'Berlin-Stettiner Eisenbahn-Gesellschaft'),
    5: Company(0,  2, (1,), 'KME',
               'Köln-Mindener Eisenbahn-Gesellschaft'),
    6: Company(0,  2, (), 'AKE',
               'Altona-Kieler Eisenbahn-Gesellschaft'),
    7: Company(0,  2, (2, 6), 'BPM',
               'Berlin-Potsdam-Magdeburger Eisenbahn'),
    8: Company(0,  2, (5, 6, 7), 'MHE',
               'Magdeburg-Halberstädter Eisenbahngesellschaft'),
  # Orange
   11: Company(1,  3, (), 'WT',
               'Königlich Württembergische Staats-Eisenbahnen'),
   12: Company(1,  3, (1, 11), 'BD',
               'Großherzoglich Badische Staatseisenbahnen'),
   13: Company(1,  3, (11,), 'BY',
               'Königlich Bayerische Staatseisenbahnen'),
   14: Company(1,  3, (5, 6, 8), 'OL', 
               'Großherzoglich Oldenburgische Staatseisenbahnen'),
   15: Company(1,  3, (1, 5, 12, 13), 'HE',
               'Großherzoglich Hessische Staatseisenbahnen'),
   16: Company(1,  3, (2, 7, 8, 13), 'SX',
               'Königlich Sächsische Staatseisenbahnen'),
   17: Company(1,  3, (2, 6, 7, 8, 14, 16), 'MS',
               'Großherzoglich Mecklenburgische Friedrich-Franz-Eisenbahn'),
   19: Company(1,  3, (1, 2, 5, 6, 7, 8, 14, 15, 16, 17), 'PR',
               'Preußische Staatseisenbahnen'),
  # Yellow
   20: Company(2,  6, (14, 17, 19), 'DSB',
               'Danske Statsbaner'),
   21: Company(2,  6, (14, 19), 'NS',
               'Nederlandse Spoorwegen'),
   22: Company(2,  6, (19, 21), 'B',
               'Nationale Maatschappij der Belgische Spoorwegen – Société '
               'Nationale des Chemins de fer Belges'),
   23: Company(2,  6, (16, 17, 19), 'PKP',
               'Polskie Koleje Państwowe'),
   24: Company(2,  6, (12, 22), 'SNCF',
               'Société nationale des chemins de fer français'),
   25: Company(2,  6, (13, 16, 23), 'KK',
               'k.k. Österreichische Staatsbahnen'),
   26: Company(2,  6, (11, 12, 24, 25), 'SBB',
               'Schweizerische Bundesbahnen – Chemins de fer fédéraux '
               'suisses – Ferrovie federali svizzere'),
   29: Company(2,  6, (11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24,
                 25, 26), 'DR',
               'Deutsche Reichsbahn'),
  # Green
   30: Company(3, 12, (), 'SJ',
               'Statens Järnvägar'),
   31: Company(3, 12, (23,), 'SŽD',
               'Советские железные дороги (Sovetskie železnye dorogi)'),
   32: Company(3, 12, (24,), 'RENFE',
               'Red Nacional de los Ferrocarriles Españoles'),
   33: Company(3, 12, (), 'BR',
               'British Rail'),
   37: Company(3, 10, (24, 25, 26), 'FS',
               'Ferrovie dello Stato'),
   40: Company(3, 10, (20, 23, 29, 30), 'BSR',
               'Baltic Sea Rail'),
   43: Company(3, 10, (21, 22, 24, 33), 'E',
               'Eurotunnel'),
  # Blue
   45: Company(4, 15, (32,), 'MAD',
               'Madrid-Barajas Airport'),
   47: Company(4, 15, (21, 22, 24, 43), 'HA',
               'Haven van Antwerpen'),
   48: Company(4, 15, (20, 23, 29, 40), 'HH',
               'Hamburger Hafen'),
   49: Company(4, 15, (21, 22, 29, 43), 'HR',
               'Haven van Rotterdam'),
   54: Company(4, 15, (33, 43), 'LHR',
               'London Heathrow Airport'),
   56: Company(4, 15, (24, 26, 43), 'CDG',
               'Aéroport Paris-Charles-de-Gaulle'),
   58: Company(4, 15, (23, 25, 26, 29), 'FRA',
               'Flughafen Frankfurt'),
   60: Company(4, 15, (45, 54, 56, 58), 'FR',
               'Ryanair'),
  # Purple
   70: Company(5, 25, (), 'OPC',
               'Outer Planet Consortium'),
   71: Company(5, 25, (), 'RCC',
               'Ring Construction Corporation'),
   75: Company(5, 25, (54, 58), 'MM',
               'Mars Mining Associates'),
   80: Company(5, 25, (45, 54, 56), 'VP',
               'Venus Prospectors'),
   85: Company(5, 25, (47, 48, 49, 70, 71), 'RU',
               'Resources Unlimited'),
   86: Company(5, 25, (47, 48, 49, 70, 71), 'AL',
               'Asteroid League'),
   90: Company(5, 25, (45, 54, 56, 58, 75, 80), 'LE',
               'Lunar Enterprises'),
  100: Company(5, 25, (70, 71, 75, 80, 85, 86, 90), 'TSI',
               'Trans-Space Inc.'),
  }

# A map id -> list of synergies with higher id:s.
COMPANIES_SYNERGIES_UP = dict(
    (id,
     [other_id for other_id, other_company in COMPANIES.items()
      if id in other_company.synergies])
    for id in COMPANIES)

# Map game type -> cost tuple
# Cost tuple: index is tier of card on top of deck, value is a named tuple
# (cost, max_affected_tier). Second to last value is with no cards
# left in deck, last value is for last turn.
Cost = collections.namedtuple('Cost', 'cost max_affected_tier')
COST = {
  "training": (Cost( 0, -1), Cost( 0, -1), Cost( 0, -1), Cost( 1, 0),
               Cost(-1, -1), Cost(-1, -1), Cost( 3,  1), Cost( 8, 2)),
  "short":    (Cost( 0, -1), Cost( 0, -1), Cost( 0, -1), Cost( 1, 0),
               Cost( 3,  1), Cost(-1, -1), Cost( 6,  2), Cost(15, 3)),
  "full":     (Cost( 0, -1), Cost( 0, -1), Cost( 0, -1), Cost( 1, 0),
               Cost( 3,  1), Cost( 6,  2), Cost(10,  3), Cost(16, 3))
  }

MAX_TIER = {
  "training": 3,
  "short": 4,
  "full": 5
}

# Synergy bonus for each tier. 
SYNERGIES = (1, 2, 4, 4, 8, 16)

def GetStartMoney(number_of_players):
  """Returns the starting cash in a game with the given number of players.

  Raises:
    ValueError: If fewer than 3 or more than 6 players
  """
  if 3 <= number_of_players <= 5: return 30
  if number_of_players == 6: return 25
  raise ValueError("Invalid number of players: %d" % number_of_players)

def NumberOfCompanies(number_of_players, tier, game_type):
  """Returns the number of companies in the game.

  Args:
    number_of_players: 3 to 6.
    tier: 0 to 5, 0 is red, 5 is purple.
    game_type: one of 'training', 'short', 'full'.
  Returns:
    0 if that tier has no companies in that game.
    >0 otherwise.
  Raises:
    ValueError for illegal values.
  """
  # Sanity check:
  if not 3 <= number_of_players <= 6: raise ValueError(
    "Invalid number of players: %d" % number_of_players)
  if not 0 <= tier <= 5: raise ValueError("Invalid tier number: %d" % tier)
  if tier > MAX_TIER[game_type]: return 0
  if number_of_players == 6:
    # Always all companies of each tier.
    return sum(1 for c in COMPANIES.values() if c.tier == tier)
  if tier == 1: return number_of_players*2 - 2
  return number_of_players + 1

def MinPrice(id):
  """Returns the minimal price for id."""
  return (id+1)//2

# Each lambda takes two params: f: face value, i: income.
# Index in tuple == tier.
_MAX_PRICE_LAMBDAS = (
  lambda f, i: f+i,       # Red
  lambda f, i: f*1.22+1,  # Orange
  lambda f, i: f*1.20+2,  # Yellow
  lambda f, i: f*1.19+7,  # Green
  lambda f, i: f*1.14+16, # Blue
  lambda f, i: f*1.10+30, # Purple
  )

def MaxPrice(id):
  """Returns the maximal price for id."""
  company = COMPANIES[id]
  return int(_MAX_PRICE_LAMBDAS[company[0]](id, company.income))

def Synergies(id, down_only=False):
  """Returns a map synergy bonus -> set of company id's."""
  result = {}
  company = COMPANIES[id]
  for other_id in company.synergies + (
      () if down_only else tuple(COMPANIES_SYNERGIES_UP[id])):
    other_company = COMPANIES[other_id]
    bonus = SYNERGIES[min(company.tier, other_company.tier)]
    result.setdefault(bonus, set()).add(other_id)
  return result

def BaseIncome(ids):
  """Calculates the total base income of the given set of company id's."""
  return sum(COMPANIES[id].income for id in ids)

def SynergyIncome(ids):
  """Calculates the total synergy income for the given set of company id's."""
  result = 0
  for id in ids:
    company = COMPANIES[id]
    result += sum(SYNERGIES[min(company.tier, COMPANIES[other_id].tier)]
                  for other_id in company.synergies
                  if other_id in ids)
  return result

def CostOfOwnership(ids, tier_on_top, type_of_game):
  """Calculates the total cost of ownership for the given set of company id's.

  tier_on_top is the tier number of the company card on top of the deck,
  or 6 if the deck is empty or 7 if this is the last turn of the game.
  type_of_game is a string "training", "short" or "full".

  Returns:
    The total cost of ownership, or -1 if tier_on_top is not present in the
    selected type_of_game.

  Raises:
    ValueError: If tier_on_top is negative or type_of_game does not exist.
  """
  if tier_on_top < 0: raise ValueError(
    "Tier on top is negative: %d" % tier_on_top)
  if tier_on_top > 7: return -1
  if type_of_game not in COST: raise ValueError(
    "Invalid type of game: %s" % type_of_game)
  cost = COST[type_of_game][tier_on_top]
  if cost.cost == -1: return -1
  if cost.max_affected_tier == -1: return 0
  return sum(cost.cost for id in ids
             if COMPANIES[id].tier <= cost.max_affected_tier)
