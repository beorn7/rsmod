#!/usr/bin/python
# -*- coding: utf-8 -*-

PRICES_RAW = ( 0,  5,  6,  7,  8,  9, 10, 11,
              12, 13, 14, 15, 16, 18, 20, 22,
              24, 26, 28, 31, 34, 37, 41, 45,
              50, 55, 60, 66, 73, 81, 90, 100)

def MakePrices():
  """Creates a map shareprice -> location.

  Location is the integer identifier of the corporation (between 0 and
  9). -1 means 'unused'. Initially, all locations are -1."""
  return dict((price, -1) for price in PRICES_RAW)

def NumberOfCompanies(number_of_players, tier, game_type):
  """Returns the number of companies in the game.

  Args:
    number_of_players: 3 to 5
    tier: 0 to 5, 0 is red, 5 is purple
    game_type: one of 'training', 'short', 'full'
  Returns:
    -1 for illegal parameters.
     0 if that tier has no companies in that game.
    >0 otherwise.
  """
  # Sanity check:
  if not 3 <= number_of_players <= 5: return -1
  if not 0 <= tier <= 5: return -1
  if game_type not in ('training', 'short', 'full'): return -1
  if tier == 5 and game_type in ('training', 'short'): return 0
  if tier == 4 and game_type == 'training': return 0
  if tier == 1: return number_of_players*2 - 2
  return number_of_players + 1

# Map is id -> (tier, income, (list of synergies with lower id's),
#               abbreviation, name).
COMPANIES = {
  # Red
    1: ( 0,  1, (), 'BME',
         'Bergisch-Märkische Eisenbahn-Gesellschaft'),
    2: ( 0,  1, (), 'BSE',
         'Berlin-Stettiner Eisenbahn-Gesellschaft'),
    5: ( 0,  2, (1,), 'KME',
         'Köln-Mindener Eisenbahn-Gesellschaft'),
    6: ( 0,  2, (), 'AKE',
         'Altona-Kieler Eisenbahn-Gesellschaft'),
    7: ( 0,  2, (2, 6), 'BPM',
         'Berlin-Potsdam-Magdeburger Eisenbahn'),
    8: ( 0,  2, (5, 6, 7), 'MHE',
         'Magdeburg-Halberstädter Eisenbahngesellschaft'),
  # Orange
   11: ( 1,  3, (), 'WT',
         'Königlich Württembergische Staats-Eisenbahnen'),
   12: ( 1,  3, (1, 11), 'BD',
         'Großherzoglich Badische Staatseisenbahnen'),
   13: ( 1,  3, (11,), 'BY',
         'Königlich Bayerische Staatseisenbahnen'),
   14: ( 1,  3, (5, 6, 8), 'OL', 
         'Großherzoglich Oldenburgische Staatseisenbahnen'),
   15: ( 1,  3, (1, 5, 12, 13), 'HE',
         'Großherzoglich Hessische Staatseisenbahnen'),
   16: ( 1,  3, (2, 7, 8, 13), 'SX',
         'Königlich Sächsische Staatseisenbahnen'),
   17: ( 1,  3, (2, 6, 7, 8, 14, 16), 'MS',
         'Großherzoglich Mecklenburgische Friedrich-Franz-Eisenbahn'),
   19: ( 1,  3, (1, 2, 5, 6, 7, 8, 14, 15, 16, 17), 'PR',
         'Preußische Staatseisenbahnen'),
  # Yellow
   20: ( 2,  6, (14, 17, 19), 'DSB',
         'Danske Statsbaner'),
   21: ( 2,  6, (14, 19), 'NS',
         'Nederlandse Spoorwegen'),
   22: ( 2,  6, (19, 21), 'B',
         'Nationale Maatschappij der Belgische Spoorwegen – Société '
         'Nationale des Chemins de fer Belges'),
   23: ( 2,  6, (16, 17, 19), 'PKP',
         'Polskie Koleje Państwowe'),
   24: ( 2,  6, (12, 22), 'SNCF',
         'Société nationale des chemins de fer français'),
   25: ( 2,  6, (13, 16, 23), 'KK',
         'k.k. Österreichische Staatsbahnen'),
   26: ( 2,  6, (11, 12, 24, 25), 'SBB',
         'Schweizerische Bundesbahnen – Chemins de fer fédéraux '
         'suisses – Ferrovie federali svizzere'),
   29: ( 2,  6, (11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24,
                 25, 26), 'DR',
         'Deutsche Reichsbahn'),
  # Green
   30: ( 3, 12, (), 'SJ',
         'Statens Järnvägar'),
   31: ( 3, 12, (23,), 'SŽD',
         'Советские железные дороги (Sovetskie železnye dorogi)'),
   32: ( 3, 12, (24,), 'RENFE',
         'Red Nacional de los Ferrocarriles Españoles'),
   33: ( 3, 12, (), 'BR',
         'British Rail'),
   37: ( 3, 10, (24, 25, 26), 'FS',
         'Ferrovie dello Stato'),
   40: ( 3, 10, (20, 23, 29, 30), 'BSR',
         'Baltic Sea Rail'),
   43: ( 3, 10, (21, 22, 24, 33), 'E',
         'Eurotunnel'),
  # Blue
   45: ( 4, 15, (32,), 'MAD',
         'Madrid-Barajas Airport'),
   47: ( 4, 15, (21, 22, 24, 43), 'HA',
         'Haven van Antwerpen'),
   48: ( 4, 15, (20, 23, 29, 40), 'HH',
         'Hamburger Hafen'),
   49: ( 4, 15, (21, 22, 29, 43), 'HR',
         'Haven van Rotterdam'),
   54: ( 4, 15, (33, 43), 'LHR',
         'London Heathrow Airport'),
   56: ( 4, 15, (24, 26, 43), 'CDG',
         'Aéroport Paris-Charles-de-Gaulle'),
   58: ( 4, 15, (23, 25, 26, 29), 'FRA',
         'Flughafen Frankfurt'),
   60: ( 4, 15, (45, 54, 56, 58), 'FR',
         'Ryanair'),
  # Purple
   70: ( 5, 25, (), 'OPC',
         'Outer Planet Consortium'),
   71: ( 5, 25, (), 'RCC',
         'Ring Construction Corporation'),
   75: ( 5, 25, (54, 58), 'MM',
         'Mars Mining Associates'),
   80: ( 5, 25, (45, 54, 56), 'VP',
         'Venus Prospectors'),
   85: ( 5, 25, (47, 48, 49, 70, 71), 'RU',
         'Resources Unlimited'),
   86: ( 5, 25, (47, 48, 49, 70, 71), 'AL',
         'Asteroid League'),
   90: ( 5, 25, (45, 54, 56, 58, 75, 80), 'LE',
         'Lunar Enterprises'),
  100: ( 5, 25, (70, 71, 75, 80, 85, 86, 90), 'TSI',
         'Trans-Space Inc.'),
  }

COMPANIES_SYNERGIES_UP = dict(
    (id,
     [other_id for other_id in COMPANIES if id in COMPANIES[other_id][2]])
    for id in COMPANIES)

def MinPrice(id):
  return (id+1)/2

# Each lambda takes two params: f: face value, i: income.
# Index in tuple == tier.
MAX_PRICE_LAMBDAS = (
  lambda f, i: f+i,       # Red
  lambda f, i: f*1.22+1,  # Orange
  lambda f, i: f*1.20+2,  # Yellow
  lambda f, i: f*1.19+7,  # Green
  lambda f, i: f*1.14+16, # Blue
  lambda f, i: f*1.10+30, # Purple
  )

def MaxPrice(id):
  company = COMPANIES[id]
  return int(MAX_PRICE_LAMBDAS[company[0]](id, company[1]))

# Map game type -> cost tuple
# Cost tuple: index is tier of card on top of deck, value is a tuple
# (cost, max affected tier). Second to last value is with no cards
# left in deck, last value is for last turn.
COST = {
  "training": ((0, -1), (0, -1), (0, -1),  (1, 0), (-1, -1), (-1, -1),
               ( 3, 1), ( 8, 2)),
  "short":    ((0, -1), (0, -1), (0, -1),  (1, 0),  (3,  1), (-1, -1),
               ( 6, 2), (15, 3)),
  "full":     ((0, -1), (0, -1), (0, -1),  (1, 0),  (3,  1), ( 6,  2),
               (10, 3), (16, 4))
  }

SYNERGIES = (1, 2, 4, 4, 8, 16)

def Synergies(id):
  """Returns a map synergy bonus -> set of company id's."""
  result = {}
  company = COMPANIES[id]
  for other_id in COMPANIES[id][2] + tuple(COMPANIES_SYNERGIES_UP[id]):
    other_company = COMPANIES[other_id]
    bonus = SYNERGIES[min(company[0], other_company[0])]
    result.setdefault(bonus, set()).add(other_id)
  return result
    
