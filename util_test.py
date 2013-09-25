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

    def tearDown(self):
        pass

    def testPlayerOrder(self):
        self.assertEqual(util.PlayerOrder(self.phase.players),
                         [2, 0, 1])

    def testSharePriceOrder(self):
        self.assertEqual(util.SharePriceOrder(self.phase.corporations),
                         [8, 5, 6, 0, 1, 2, 3, 4, 7, 9])

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



if __name__ == '__main__':
    unittest.main()
