#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Module containing the action class hierarchy.

TODO: Explain how actions work in general.

TODO: Do something about I18N. (English messages are hardcoded here.)
"""

import copy
import itertools
import logging


class Action(object):
    """Base class for actions."""

    PARAMETERS = set()

    def __init__(self, **kwargs):
        self.message = kwargs.get('message','')
        self.parameters = {key: None for key in self.PARAMETERS}
        if not self.SetParameters(**kwargs):
            logging.error('Could not set all parameters in %s.', kwargs) 
        
    def __repr__(self):
        items = ['%s=%r' % (k, v) for k, v in self.parameters]
        items.append('message=%r' % self.message)
        return '%s(%s)' % (self.__class__.__name__, ', '.join(items))
 
    def __str__(self):
        return self.message

    def SetParameters(self, **kwargs):
        """Sets parameters for this action.

        Args:
          kwargs: The parameters to set. A mapping with the key 'message'
            will be ignored.
        Returns:
          True if all parameters could be set successfully, otherwise False.
          Reasons for failure to set a parameter include:
          - The parameter does not exist for this action.
          - The parameter is already set to a fixed value that is different
            from the one being set here.
          - The parameter allows a set of values, but the value being
            set here is neither in that set nor a subset of that set.
            """
        ok = True
        for k, v in kwargs:
            if k == 'message':
                # Ignore key 'message'.
                continue
            if k not in self.parameters:
                logging.error('Parameter "%s% does not exist in this action.',
                              k)
                ok = False
                continue
            current = self.parameters[k]
            if current is None:
                # Not yet set, so do it now:
                self.parameters[k] = v
                continue
            if current == v:
                # Already set to that value, fine.
                continue
            if not isinstance(current, set):
                logging.error('Parameter "%s" already set to "%s". Cannot be '
                              'set to "%s".', k, current, v)
                ok = false
                continue
            if (isinstance(v, set) and v.issubset(current)) or v in current:
                self.parameters[k] = v
                continue
            logging.error('Parameter "%s" already set to "%s". Cannot be '
                          'set to "%s".', k, current, v)
            ok = false
        return ok
    
    def SetAndLogMessage(self, message):
        self.message = message
        logger.info('Action in T%d, P%d: %s',
                    game.phase.turn, game.phase.phase, message)

    def IsExecutable(self):
        """Returns True if this action is ready to be executed.

        An action can be executed if all its parameters are set to a
        fixed value (i.e. they are neither a set nor None).

        Returns:
          True if this Action is ready to be executed.
        """
        return all(v is not None and not isinstance(v, set)
                   for _, v in self.parameters)

    def Execute(self, game):
        """Executes the action.

        Args:
          The Game object on which the action is executed.

        Returns:
          True after successful execution, otherwise False.
          This implementation returns the result of IsExecutable() and logs
          if IsExecutable() returns False. (It can be called via 'super' in
          derived classes to test executability.)
        """
        if not self.IsExecutable():
            logging.error('Action is not yet executable.')
            return False
        return True

class PhaseBeginAction(Action):
    """Action to begin a phase."""

    def Execute(self, game):
        """All the required setup/initialization of state information is
        done here."""
        p = game.phase.phase
        game.phase.actions = []
        # Remember the phase object as it was at the beginning of the phase:
        game.init_phase = copy.deepcopy(game.phase)
        # Actions are shared, though.
        game.init_phase.actions = game.phase.actions
        game.init_phase.next_action = None
        if p == 1:
            game.spo = sorted(
                (c for c in game.phase.corperations if c.price > 0),
                key=c.price,
                reverse=True)
            game.i_spo = 0
        elif p == 2:
            game.fvo = sorted(
                (c for c in itertools.chain(
                        player.companies for player in game.phase.players)),
                reverse=True)
            game.i_fvo = 0

        # TODO more phase specific setup
        self.SetAndLogMessage("Phase %p begins." % p)
        return True


class PhaseEndAction(Action):
    """Action to end a phase."""

    def Execute(self, game):
        """Generally, this is just doing phase dependent wrapping-up.

        After the wrapping-up, the game is saved and static HTML is
        generated and finally the turn/phase number is incremented,
        unless this is P9 and the game is over. In that case,
        game.over is set instead of saving files and incrementing the
        turn/phase number.
        """
        message = []
        p = game.phase.phase
        if p == 1:
            if game.i_spo == 0:
                message.append('Nothing happens.')
        elif p == 2:
            if game.i_fvo == 0:
                message.append('Nothing happens.')
        elif p == 9:
            if not game.phase.available and game.phase.last_turn == 0:
                game.phase.last_turn = game.phase.turn + 1
                message.append('Game end card is flipped.')
            elif game.i_spo == 0:
                message.append('Nothing happens.')
        # TODO more phase specific wrap up.
        message.append("Phase %d ends." % p)
        self.SetAndLogMessage(" ".join(message))
        if p == 9 and game.phase.turn == game.phase.last_turn:
            game.over = True
            return True
        game.Save(overwrite_existing=True)
        game.WriteHtml()
        if p == 9:
            game.phase.turn += 1
            game.phase.phase = 1
        else:
            game.phase.phase += 1
        return True


class GameEndAction(Action):
    """Action to end the game."""
    
    def Execute(self, game):
        """Saves the game and writes HTML. Puts the final ranking in
        the message."""
        self.SetAndLogMessage('Game over.')
         # TODO: Append ranking.
        game.Save()
        game.WriteHtml()
        return True
  
