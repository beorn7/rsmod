#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Tests for the base module."""

import unittest

import base

class TestBase(unittest.TestCase):

    def testMakePrices(self):
        """Just a smoke test."""
        self.assertEqual(base.MakePrices()[20], -1)

    def testNumberOfCompanies(self):
        self.assertRaises(ValueError, base.NumberOfCompanies, 0, 1, 'full')
        self.assertRaises(ValueError, base.NumberOfCompanies, 1, 1, 'full')
        self.assertRaises(ValueError, base.NumberOfCompanies, 2, 1, 'full')
        self.assertRaises(ValueError, base.NumberOfCompanies, 3, 6, 'full')
        self.assertRaises(ValueError, base.NumberOfCompanies, 3, 5, 'illegal')
        self.assertEqual(base.NumberOfCompanies( 4, 4, 'training'), 0)
        self.assertEqual(base.NumberOfCompanies( 4, 5, 'training'), 0)
        self.assertEqual(base.NumberOfCompanies( 4, 5, 'short'), 0)
        self.assertEqual(base.NumberOfCompanies( 3, 0, 'full'), 4)
        self.assertEqual(base.NumberOfCompanies( 3, 1, 'full'), 4)
        self.assertEqual(base.NumberOfCompanies( 3, 2, 'full'), 4)
        self.assertEqual(base.NumberOfCompanies( 4, 0, 'full'), 5)
        self.assertEqual(base.NumberOfCompanies( 4, 1, 'full'), 6)
        self.assertEqual(base.NumberOfCompanies( 4, 3, 'full'), 5)
        self.assertEqual(base.NumberOfCompanies( 5, 0, 'full'), 6)
        self.assertEqual(base.NumberOfCompanies( 5, 1, 'full'), 8)
        self.assertEqual(base.NumberOfCompanies( 5, 4, 'full'), 6)
        self.assertEqual(base.NumberOfCompanies( 6, 0, 'full'), 6)
        self.assertEqual(base.NumberOfCompanies( 6, 1, 'full'), 8)
        self.assertEqual(base.NumberOfCompanies( 6, 2, 'full'), 8)
        self.assertEqual(base.NumberOfCompanies( 6, 3, 'full'), 7)
        self.assertEqual(base.NumberOfCompanies( 6, 4, 'full'), 8)
        self.assertEqual(base.NumberOfCompanies( 6, 5, 'full'), 8)

    def testMinPrice(self):
        self.assertEqual(base.MinPrice(1), 1)
        self.assertEqual(base.MinPrice(2), 1)
        self.assertEqual(base.MinPrice(3), 2)

    def testMaxPrice(self):
        self.assertEqual(base.MaxPrice(1), 2)
        self.assertEqual(base.MaxPrice(2), 3)
        self.assertEqual(base.MaxPrice(5), 7)
        self.assertEqual(base.MaxPrice(8), 10)
        self.assertEqual(base.MaxPrice(11), 14)
        self.assertEqual(base.MaxPrice(15), 19)
        self.assertEqual(base.MaxPrice(19), 24)
        self.assertEqual(base.MaxPrice(20), 26)
        self.assertEqual(base.MaxPrice(29), 36)
        self.assertEqual(base.MaxPrice(30), 42)
        self.assertEqual(base.MaxPrice(43), 58)
        self.assertEqual(base.MaxPrice(56), 79)
        self.assertEqual(base.MaxPrice(100), 140)

    def testSynergies(self):
        self.assertEqual(base.Synergies(1),
                         {1: {5, 12, 15, 19}})
        self.assertEqual(base.Synergies(17),
                         {1: {2, 6, 7, 8}, 2: {14, 16, 19, 20, 23, 29}})
        self.assertEqual(base.Synergies(29),
                         {2: {11, 12, 13, 14, 15, 16, 17, 19},
                          4: {20, 21, 22, 23, 24, 25, 26, 40, 48, 49, 58}})
        self.assertEqual(base.Synergies(56),
                         {4: {24, 26, 43},
                          8: {60, 80, 90}})
        self.assertEqual(base.Synergies(70),
                         {16: {85, 86, 100}})
        self.assertEqual(base.Synergies(1, True),
                         {})
        self.assertEqual(base.Synergies(17, True),
                         {1: {2, 6, 7, 8}, 2: {14, 16}})
        self.assertEqual(base.Synergies(29, True),
                         {2: {11, 12, 13, 14, 15, 16, 17, 19},
                          4: {20, 21, 22, 23, 24, 25, 26}})
        self.assertEqual(base.Synergies(56, True),
                         {4: {24, 26, 43}})
        self.assertEqual(base.Synergies(70, True),
                         {})

    def testBaseIncome(self):
        self.assertEqual(base.BaseIncome({}), 0)
        self.assertEqual(base.BaseIncome({1,}), 1)
        self.assertEqual(base.BaseIncome({8,}), 2)
        self.assertEqual(base.BaseIncome({1,8}), 3)
        self.assertEqual(base.BaseIncome({11,}), 3)
        self.assertEqual(base.BaseIncome({19,}), 3)
        self.assertEqual(base.BaseIncome({2,11}), 4)
        self.assertEqual(base.BaseIncome({7,11}), 5)
        self.assertEqual(base.BaseIncome({20,}), 6)
        self.assertEqual(base.BaseIncome({30,}), 12)
        self.assertEqual(base.BaseIncome({43,}), 10)
        self.assertEqual(base.BaseIncome({56,}), 15)
        self.assertEqual(base.BaseIncome({100,}), 25)
        self.assertEqual(base.BaseIncome({1,8,14,22}), 12)
        self.assertEqual(base.BaseIncome({45,47,70}), 55)
        self.assertEqual(base.BaseIncome({43,45,60,70}), 65)
        self.assertEqual(base.BaseIncome({33,12,90}), 40)
        self.assertEqual(base.BaseIncome({1,2,5,6,7,11,12,19,20}), 23)

    def testSynergyIncome(self):
        self.assertEqual(base.SynergyIncome({}), 0)
        self.assertEqual(base.SynergyIncome({1,}), 0)
        self.assertEqual(base.SynergyIncome({8,}), 0)
        self.assertEqual(base.SynergyIncome({5,8}), 1)
        self.assertEqual(base.SynergyIncome({14,8}), 1)
        self.assertEqual(base.SynergyIncome({19,}), 0)
        self.assertEqual(base.SynergyIncome({2,12}), 0)
        self.assertEqual(base.SynergyIncome({1,12}), 1)
        self.assertEqual(base.SynergyIncome({20,14}), 2)
        self.assertEqual(base.SynergyIncome({20,40}), 4)
        self.assertEqual(base.SynergyIncome({43,47}), 4)
        self.assertEqual(base.SynergyIncome({56,43}), 4)
        self.assertEqual(base.SynergyIncome({100,43}), 0)
        self.assertEqual(base.SynergyIncome({1,8,14,22}), 1)
        self.assertEqual(base.SynergyIncome({43,47,85}), 12)
        self.assertEqual(base.SynergyIncome({43,45,60,70}), 8)
        self.assertEqual(base.SynergyIncome({33,12,90}), 0)
        self.assertEqual(base.SynergyIncome({1,2,5,6,7,11,12,19,20}), 13)

    def testCostOfOwnership(self):
        self.assertEqual(base.CostOfOwnership({}, 7, "full"), 0)
        self.assertRaises(ValueError,
                          base.CostOfOwnership, {}, 7, "invalid")
        self.assertRaises(ValueError,
                          base.CostOfOwnership, {1,19,20,43,45,100}, -1, "training")
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 0, "training"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 0, "short"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 0, "full"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 1, "training"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 1, "short"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 1, "full"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 2, "training"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 2, "short"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 2, "full"), 0)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 3, "training"), 1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 3, "short"), 1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 3, "full"), 1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 4, "training"), -1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 4, "short"), 6)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 4, "full"), 6)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 5, "training"), -1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 5, "short"), -1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 5, "full"), 18)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 6, "training"), 6)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 6, "short"), 18)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 6, "full"), 40)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 7, "training"), 24)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 7, "short"), 60)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 7, "full"), 64)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 8, "training"), -1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 8, "short"), -1)
        self.assertEqual(base.CostOfOwnership({1,19,20,43,45,100}, 8, "full"), -1)


if __name__ == '__main__':
    unittest.main()
