#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Tests for the base module."""

import unittest

import base

class TestBase(unittest.TestCase):

    def testMakePrices(self):
        """Just a smoke test."""
        self.assertEqual(base.MakePrices()[20], -1)

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

    def testMinPrice(self):
        self.assertEqual(base.MinPrice(1), 1)
        self.assertEqual(base.MinPrice(2), 1)
        self.assertEqual(base.MinPrice(3), 2)

    def testNumberOfCompanies(self):
        self.assertEqual(base.NumberOfCompanies(0,1,'full'), -1)
        self.assertEqual(base.NumberOfCompanies(1,1,'full'), -1)
        self.assertEqual(base.NumberOfCompanies(2,1,'full'), -1)
        self.assertEqual(base.NumberOfCompanies(3,6,'full'), -1)
        self.assertEqual(base.NumberOfCompanies(3,5,'illegal'), -1)
        self.assertEqual(base.NumberOfCompanies(4,4,'training'), 0)
        self.assertEqual(base.NumberOfCompanies(4,5,'training'), 0)
        self.assertEqual(base.NumberOfCompanies(4,5,'short'), 0)
        self.assertEqual(base.NumberOfCompanies(3,0,'full'), 4)
        self.assertEqual(base.NumberOfCompanies(3,1,'full'), 4)
        self.assertEqual(base.NumberOfCompanies(3,2,'full'), 4)
        self.assertEqual(base.NumberOfCompanies(4,0,'full'), 5)
        self.assertEqual(base.NumberOfCompanies(4,1,'full'), 6)
        self.assertEqual(base.NumberOfCompanies(4,3,'full'), 5)
        self.assertEqual(base.NumberOfCompanies(5,0,'full'), 6)
        self.assertEqual(base.NumberOfCompanies(5,1,'full'), 8)
        self.assertEqual(base.NumberOfCompanies(5,4,'full'), 6)
        self.assertEqual(base.NumberOfCompanies(6,0,'full'), 6)
        self.assertEqual(base.NumberOfCompanies(6,1,'full'), 8)
        self.assertEqual(base.NumberOfCompanies(6,2,'full'), 8)
        self.assertEqual(base.NumberOfCompanies(6,3,'full'), 7)
        self.assertEqual(base.NumberOfCompanies(6,4,'full'), 8)
        self.assertEqual(base.NumberOfCompanies(6,5,'full'), 8)

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



if __name__ == '__main__':
    unittest.main()
