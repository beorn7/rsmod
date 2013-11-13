#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os

import action
import setup

class Game(object):
    """Represents a whole game (in contrast to a single phase).

    This class manages the various Phase objects and provides various
    methods to simplify the management of the rather low-level data
    model provided by the Phase objects.

    Only use factory methods to create Game objects, not __init__
    directly.
    """

    def __init__(self):
        """Do not use __init__ directly, use New() or Load() instead."""
        # Additional game state tracking.
        self.over = False  # Is the game over yet?
        self.spo = []  # Active corps in share price order.
        self.i_spo = -1  # Where in spo are we?
        self.fvo = []  # Player-owned companies in face value order.
        self.i_fvo = -1  # Where in fvo are we?

    @classmethod
    def New(cls, params):
        """Creates a newly started game from the given parameters.

        Args:
          params: A state.GameParams object.
        Returns:
          The game object, ready to start the game.
        """
        game = cls()
        game.phase = setup.MakePhase(params)
        return game
    
    @classmethod
    def Load(cls, filename):
        """Reconstruct a game from the given file.

        The actions contained in the loaded file are replayed
        immediately. A next_action is then calculated (i.e. not
        read from the file).
        """
        # TODO: implement

    def Save(self, filename=None, overwrite_existing=False):
        """Saves the game state to a file.

        You only need to call this method explicitly if you want to
        save an intermediate game state or you want to save the game
        state to a separate file (outside of the standard directory
        structure). At the end of a phase or the game, the game state
        is saved automatically.

        next_action is not saved.

        Args:
          filename: If None, the standard file name in the game directory
            is used. If you wish to use a non-standard filename, you can
            pass it in as this paramater.
          overwrite_existing: Set to True if you want to overwrite an
            existing file.
        Returns:
          True if saving was successful.
        """
        try:
            state.SavePhase(self.init_phase, filename, overwrite_existing)
        except OSError as e:
            logging.exception('Saving game state failed: %s', e)
            return False
        return True

    def WriteHtml(self):
        """Writes static HTML of the current game state.

        You only need to call this method explicitly if you want to create
        HTML output for an intermediate game state. At the end of a phase and
        at the end of the game, HTML is automatically created.
        """
        # TODO: implement

    def Next(self, **kwargs):
        """Executes the next action.

        If the execution is successful, a new next action is created
        and the next_action attribute is updated accordingly. If that
        new action is already executable, it is executed immediately
        and so on until a next action is reached that is not yet
        executable (or the game is over).

        Args:
          kwargs: Those are passed to the SetParameters() method of the next
            action object prior to executing it.
        Returns:
          True if all executed actions were successful. False if anything
          has gone wrong. An error message is logged. Typical failure modes are
          the following:
          - The next action is not yet executable (because it needs more
            parameters).
          - The parameters provided as arguments to this method are incompatible
            with the parameters already set or possible to be set for the next
            action.
          - One of the actions itself creates an error during execution.
        """
        if not self.next_action.SetParameters(**kwargs):
            logging.error(
                "Setting parameters failed. next action not executed.")
            return False
        if not self.next_action.IsExecutable():
            logging.error(
                "Next action not yet executable. Current parameters: %s",
                self.next_action.parameters)
            return False
        while not self.over and self.next_action.IsExecutable():
            if not self.next_action.Execute(self):
                logging.error("Execution of next action failed.")
                return False
            self.CreateNextAction()
        if self.over:
            # Game is over, just execute the final action, which is a
            # GameEndAction.
            return self.next_action.Execute(self)
        return True

    def CreateNextAction(self):
        """Creates a new next action (and sets self.next_action)."""
        if self.over:
            self.next_action = action.GameEndAction()
            return
        # TODO implement
