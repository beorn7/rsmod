#!/usr/bin/python3
# -*- coding: utf-8 -*-

import static_html
import setup
import state

phase = setup.MakePhase(
            state.GameParams(
                name='testgame',
                players=('Alice', 'Bob', 'Charly', 'Dolly', 'Ed', 'F "bla" F.'),
                type='short',
                preselected_companies={8,19,29,43,60},
                open_companies=False,
                ascending_companies=False,
                share_redemption=True,
                file_root='/home/rabe/rsmod/tdir'))
phase.actions.extend(['<b>a</b> foo', '<b>b</b> bar'])
#phase.future_actions.extend(['1 bla', '2 blubb'])

phase.foreign_investor.companies.add(1)
phase.foreign_investor.companies.add(29)
phase.foreign_investor.companies.add(20)
phase.foreign_investor.companies.add(31)

phase.corporations[0].price=2
phase.corporations[0].shares=2
phase.corporations[1].price=29
phase.corporations[1].shares=8
phase.corporations[5].price=16
phase.corporations[5].shares=3
phase.corporations[5].money=42
phase.corporations[5].companies=set((21,22))
phase.corporations[7].price=30
phase.corporations[7].shares=2
phase.corporations[8].price=1
phase.corporations[8].shares=2
phase.corporations[9].price=13
phase.corporations[9].shares=2

phase.corporations[0].companies=set((11,12,13,14,15,16,17,19,5,6))
phase.corporations[0].companies_in_flight=set((7,8))
phase.corporations[0].money_in_flight = 5

phase.phase = 6

p = phase.players[1]
p.companies.add(45)
p.companies.add(11)
p.shares[1]=2
p.shares[5]=3
p.presidencies[5]=True

#phase.deck.clear()
#phase.deck.extend([45, 60])
#phase.last_turn = 1

static_html.WriteHtml(phase, overwrite_existing=True)



