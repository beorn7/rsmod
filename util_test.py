#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Tests for the util module."""

import unittest

import setup
import state
import util

class TestUtil(unittest.TestCase):

    def setUp(self):
        self.phase = setup.MakePhase(
            state.GameParams(
                name='testgame',
                players=('Alice', 'Bob', 'Charly'),
                type='short',
                preselected_companies={8,19,29,43,60},
                file_root='/testdir',
                seed=42))
        self.phase.corporations[8].price = 29
        self.phase.corporations[5].price = 28
        self.phase.corporations[6].price = 26
        self.phase.corporations[8].shares = 5
        self.phase.corporations[5].shares = 6
        self.phase.corporations[6].shares = 4
        self.phase.players[1].companies = {7,8,17,19}
        self.phase.players[1].money = 11
        self.phase.players[1].shares[5] = 1
        self.phase.players[1].shares[6] = 2
        self.phase.players[1].shares[8] = 3
        self.phase.players[1].presidencies[8] = True
        self.phase.players[2].shares[5] = 3
        self.phase.players[2].shares[6] = 2
        self.phase.players[2].shares[8] = 1
        self.phase.players[2].presidencies[6] = True
        self.phase.players[2].presidencies[5] = True
        self.phase.players[0].shares[1] = 4
        self.phase.players[0].presidencies[1] = True
        self.phase.corporations[1].companies = {7,8,19}
        self.phase.corporations[1].money = 17
        self.phase.corporations[1].companies_in_flight = {17}
        self.phase.corporations[1].money_in_flight = 13
        self.phase.corporations[1].price = 1
        self.phase.corporations[1].shares = 6
        self.phase.foreign_investor.companies = {7,8,17,19}

    def tearDown(self):
        pass

    def testPlayerOrder(self):
        self.assertEqual(util.PlayerOrder(self.phase.players),
                         [2, 0, 1])

    def testSharePriceOrder(self):
        self.assertEqual(util.SharePriceOrder(self.phase.corporations),
                         [8, 5, 6, 1, 0, 2, 3, 4, 7, 9])

    def testTierOnTop(self):
        self.assertEqual(util.TierOnTop(self.phase), 0)
        self.phase.deck = self.phase.deck[1:]
        self.assertEqual(util.TierOnTop(self.phase), 1)
        self.phase.deck = self.phase.deck[3:]
        self.assertEqual(util.TierOnTop(self.phase), 1)
        self.phase.deck = self.phase.deck[1:]
        self.assertEqual(util.TierOnTop(self.phase), 2)
        self.phase.deck = self.phase.deck[3:]
        self.assertEqual(util.TierOnTop(self.phase), 2)
        self.phase.deck = self.phase.deck[1:]
        self.assertEqual(util.TierOnTop(self.phase), 3)
        self.phase.deck = self.phase.deck[3:]
        self.assertEqual(util.TierOnTop(self.phase), 3)
        self.phase.deck = self.phase.deck[1:]
        self.assertEqual(util.TierOnTop(self.phase), 4)
        self.phase.deck = self.phase.deck[3:]
        self.assertEqual(util.TierOnTop(self.phase), 4)
        self.phase.deck = self.phase.deck[1:]
        self.assertEqual(util.TierOnTop(self.phase), 6)
        self.phase.last_turn = 1
        self.assertEqual(util.TierOnTop(self.phase), 7)

    def testCostOfOwnership(self):
        ids = {1,2,11,20,31}
        self.assertEqual(util.CostOfOwnership(ids, self.phase), 0)
        self.phase.deck = self.phase.deck[9:]
        self.assertEqual(util.CostOfOwnership(ids, self.phase), 2)
        self.phase.deck = self.phase.deck[4:]
        self.assertEqual(util.CostOfOwnership(ids, self.phase), 9)
        self.phase.deck = self.phase.deck[4:]
        self.assertEqual(util.CostOfOwnership(ids, self.phase), 24)
        self.phase.last_turn = 1
        self.assertEqual(util.CostOfOwnership(ids, self.phase), 75)

    def testTotalIncomePlayer(self):
        self.assertEqual(util.TotalIncomePlayer(1, self.phase), 10)
        self.phase.deck = self.phase.deck[9:]
        self.assertEqual(util.TotalIncomePlayer(1, self.phase), 8)
        self.phase.deck = self.phase.deck[4:]
        self.assertEqual(util.TotalIncomePlayer(1, self.phase), -2)

    def testTotalIncomeCorporation(self):
        self.assertEqual(util.TotalIncomeCorporation(1, self.phase), 17)
        self.phase.deck = self.phase.deck[9:]
        self.assertEqual(util.TotalIncomeCorporation(1, self.phase), 15)
        self.phase.deck = self.phase.deck[4:]
        self.assertEqual(util.TotalIncomeCorporation(1, self.phase), 5)

    def testTotalIncomeForeignInvestor(self):
        self.assertEqual(util.TotalIncomeForeignInvestor(self.phase), 15)
        self.phase.deck = self.phase.deck[9:]
        self.assertEqual(util.TotalIncomeForeignInvestor(self.phase), 13)
        self.phase.deck = self.phase.deck[4:]
        self.assertEqual(util.TotalIncomeForeignInvestor(self.phase), 3)

    def testSharePrice(self):
        self.assertEqual(util.SharePrice(5, self.phase), 73)
        self.assertEqual(util.SharePrice(6, self.phase), 60)
        self.assertEqual(util.SharePrice(8, self.phase), 81)
        self.assertEqual(util.SharePrice(1, self.phase), 5)
        self.assertEqual(util.SharePrice(2, self.phase), -1)

    def testMaxPayout(self):
        self.assertEqual(util.MaxPayout(5, self.phase), 24)
        self.assertEqual(util.MaxPayout(6, self.phase), 20)
        self.assertEqual(util.MaxPayout(8, self.phase), 27)
        self.assertEqual(util.MaxPayout(1, self.phase), 1)
        self.assertEqual(util.MaxPayout(2, self.phase), -1)

    def testBookValuePlayer(self):
        self.assertEqual(util.BookValuePlayer(1, self.phase),
                         51+11+73+2*60+3*81)

    def testBookValueCorporation(self):
        self.assertEqual(util.BookValueCorporation(1, self.phase), 51+30)

    def testMarketCap(self):
        self.assertEqual(util.MarketCap(1, self.phase), 30)
        self.assertEqual(util.MarketCap(5, self.phase), 438)
        self.assertEqual(util.MarketCap(6, self.phase), 240)
        self.assertEqual(util.MarketCap(8, self.phase), 405)

    def testBankShares(self):
        self.assertEqual(util.BankShares(1, self.phase), 2)
        self.assertEqual(util.BankShares(5, self.phase), 2)
        self.assertEqual(util.BankShares(6, self.phase), 0)
        self.assertEqual(util.BankShares(8, self.phase), 1)

    def testPresident(self):
        players = self.phase.players
        self.assertEqual(util.President(1, players), 0)
        self.assertEqual(util.President(5, players), 2)
        self.assertEqual(util.President(6, players), 2)
        self.assertEqual(util.President(8, players), 1)


if __name__ == '__main__':
    unittest.main()
