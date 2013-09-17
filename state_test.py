#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Tests for the state module."""

import os
import shutil
import tempfile
import unittest

import setup
import state

class TestState(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def testSaveAndRestore(self):
        phase = setup.MakePhase(
            state.GameParams(
                name='testgame',
                players=('Alice', 'Bob', 'Charly', 'Dolly', 'Ed', 'F. F.'),
                type='training',
                preselected_companies={1,2},
                open_companies=True,
                ascending_companies=False,
                share_redemption=True,
                file_root=self.tempdir,
                css_file='../test.css',
                image_dir='../img',
                seed=42))
        state.SavePhase(phase)
        restored_phase = state.RestorePhase(
            os.path.join(self.tempdir, 't1p1.py'))
        self.assertEqual(phase, restored_phase)


if __name__ == '__main__':
    unittest.main()
