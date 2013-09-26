#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Game(object):
    """Represents a whole game (in contrast to a single phase).

    This class manages the various Phase objects and provides various
    methods to simplify the management of the rather low-level data
    model provided by the Phase objects.

    Only use factory methods to create Game objects, not __init__
    directly.
    """

    def New():
        """Creates a newly started game from the given parameters."""
        # TODO: implement
        
    def Load(filename):
        """Reconstruct a game from the given file.

        The actions contained in the loaded file are replayed immediately.
        """
        # TODO: implement

    def Save(filename=None):
        """Saves the game state to a file.

        You only need to call this method explicitly if you want to
        save an intermediate game state or you want to save the game
        state to a separate file (outside of the stanhard directory
        structure). At the end of a phase or the game, the game state
        is saved automatically.

        Args:
          filename: If None, the standard file name in the game directory
            is used. If you wish to use a non-standard filename, you can
            pass it in as this paramater.
        Returns:
          A Game object.
        """
        # TODO: implement

    def WriteHtml():
        """Writes static HTML of the current game state.

        You only need to call this method explicitly if you want to create
        HTML output for an intermediate game state. At the end of a phase and
        at the end of the game, HTML is automatically created.
        """
        # TODO: implement

    def Next(**kwargs):
        """Executes the next action.

        If the execution is successful, the next_action attribute is updated
        to the returned action. If that action is already executable, the
        new next action is executed immediately and so on until a next action
        is reached that is not yet executable (or the game is over).

        Args:
          kwargs: Those are passed to the SetParameter() method of the next
            action object prior to executing it.
        Returns:
          True if the action executes successfully. False if something
          goes wrong. An error message is logged. Typical failure modes are
          the following:
          - The next action is not yet executable (because it needs more
            parameters).
          - The parameters provided as arguments to this method are incompatible
            with the parameters already set or possible to be set for the next
            action.
          - The action itself creates an error during execution.
        """
        # TODO: implement
