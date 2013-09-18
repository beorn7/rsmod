#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Tests for the setup module."""

import unittest

import setup

from state import Phase, Player, Corporation, ForeignInvestor, GameParams

class TestSetup(unittest.TestCase):

    def testThreePlayers(self):
        phase = setup.MakePhase(
            GameParams(
                name='testgame',
                players=('Alice', 'Bob', 'Charly'),
                type='short',
                preselected_companies={8,19,20,29},
                open_companies=False,
                ascending_companies=False,
                share_redemption=False,
                file_root='/home/test',
                css_file='../test.css',
                image_dir='../img',
                seed=42))
        self.assertEqual(str(phase), str(Phase(params=GameParams(name='testgame', players=('Alice', 'Bob', 'Charly'), type='short', preselected_companies={8, 19, 20, 29}, open_companies=False, ascending_companies=False, share_redemption=False, file_root='/home/test', css_file='../test.css', image_dir='../img', seed=42), turn=1, phase=1, last_turn=0, available={8, 1, 7}, unavailable=set(), closed=set(), deck=[5, 19, 16, 11, 12, 26, 20, 29, 21, 32, 31, 43, 33, 54, 45, 58, 47], foreign_investor=ForeignInvestor(money=4, companies=set()), players=[Player(money=30, companies=set(), order=2, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=3, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=1, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False])], corporations=[Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0)], actions=[], future_actions=[])))
     
    def testFourPlayers(self):
        phase = setup.MakePhase(
            GameParams(
                name='testgame',
                players=('Alice', 'Bob', 'Charly', 'Dolly'),
                type='full',
                preselected_companies={1,2,5,6,8,19,30,100},
                open_companies=False,
                ascending_companies=True,
                share_redemption=False,
                file_root='/home/test',
                css_file='../test.css',
                image_dir='../img',
                seed=42))
        self.assertEqual(str(phase), str(Phase(params=GameParams(name='testgame', players=('Alice', 'Bob', 'Charly', 'Dolly'), type='full', preselected_companies={1, 2, 100, 5, 6, 8, 19, 30}, open_companies=False, ascending_companies=True, share_redemption=False, file_root='/home/test', css_file='../test.css', image_dir='../img', seed=42), turn=1, phase=1, last_turn=0, available={1, 2, 5, 6}, unavailable=set(), closed=set(), deck=[8, 11, 13, 15, 16, 17, 19, 20, 21, 23, 24, 25, 30, 31, 32, 40, 43, 45, 47, 54, 58, 60, 71, 80, 85, 90, 100], foreign_investor=ForeignInvestor(money=4, companies=set()), players=[Player(money=30, companies=set(), order=1, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=3, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=4, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=2, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False])], corporations=[Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0)], actions=[], future_actions=[])))

    def testFivePlayers(self):
        phase = setup.MakePhase(
            GameParams(
                name='testgame',
                players=('Alice', 'Bob', 'Charly', 'Dolly', 'Ed'),
                type='full',
                preselected_companies={8,19,30,100},
                open_companies=False,
                ascending_companies=True,
                share_redemption=False,
                file_root='/home/test',
                css_file='../test.css',
                image_dir='../img',
                seed=42))
        self.assertEqual(str(phase), str(Phase(params=GameParams(name='testgame', players=('Alice', 'Bob', 'Charly', 'Dolly', 'Ed'), type='full', preselected_companies={8, 19, 100, 30}, open_companies=False, ascending_companies=True, share_redemption=False, file_root='/home/test', css_file='../test.css', image_dir='../img', seed=42), turn=1, phase=1, last_turn=0, available={1, 2, 5, 6, 7}, unavailable=set(), closed=set(), deck=[8, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 25, 26, 29, 30, 31, 32, 33, 40, 43, 45, 47, 49, 54, 58, 60, 70, 71, 75, 86, 90, 100], foreign_investor=ForeignInvestor(money=4, companies=set()), players=[Player(money=30, companies=set(), order=3, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=2, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=5, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=4, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=30, companies=set(), order=1, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False])], corporations=[Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0)], actions=[], future_actions=[])))

    def testSixPlayers(self):
        phase = setup.MakePhase(
            GameParams(
                name='testgame',
                players=('Alice', 'Bob', 'Charly', 'Dolly', 'Ed', 'F. F.'),
                type='training',
                preselected_companies={1,2},
                open_companies=True,
                ascending_companies=False,
                share_redemption=True,
                file_root='/home/test',
                css_file='../test.css',
                image_dir='../img',
                seed=42))
        self.assertEqual(str(phase), str(Phase(params=GameParams(name='testgame', players=('Alice', 'Bob', 'Charly', 'Dolly', 'Ed', 'F. F.'), type='training', preselected_companies={1, 2}, open_companies=True, ascending_companies=False, share_redemption=True, file_root='/home/test', css_file='../test.css', image_dir='../img', seed=42), turn=1, phase=1, last_turn=0, available={1, 2, 5, 6, 7, 8}, unavailable=set(), closed=set(), deck=[14, 15, 17, 19, 12, 16, 11, 13, 21, 22, 25, 24, 23, 29, 26, 20, 33, 30, 40, 31, 43, 32, 37], foreign_investor=ForeignInvestor(money=4, companies=set()), players=[Player(money=25, companies=set(), order=6, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=25, companies=set(), order=4, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=25, companies=set(), order=5, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=25, companies=set(), order=2, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=25, companies=set(), order=1, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False]), Player(money=25, companies=set(), order=3, shares=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], presidencies=[False, False, False, False, False, False, False, False, False, False])], corporations=[Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0), Corporation(money=0, companies=set(), money_in_flight=0, companies_in_flight=0, done=False, price=-1, shares=0)], actions=[], future_actions=[])))


if __name__ == '__main__':
    unittest.main()
