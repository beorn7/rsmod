#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Module containing the action class hierarchy.

TODO: Explain how actions work in general.
"""

class Action(object):
    """Base class for actions."""
    def __init__(self, **kwargs):
        self.message = kwargs.get('message','')
        
    def __repr__(self):
        return 'Action(message=%r)' % self.message

    def __str__(self):
        pass # TODO something for the HTML page

class PhaseEndAction(Action):
    """Action to end a phase."""
    def __repr__(self):
        return 'PhaseEndAction(message=%r)' % self.message
