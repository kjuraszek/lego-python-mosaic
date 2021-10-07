"""
utilities module

This module contains common constants, functions and classes.
"""

import wx
from colour.difference import delta_E_CIE2000

_FILES_SUFFIXES = ["_mosaic.png", "_mosaic_scaled.png", "_mosaic_instructions.pdf"]


def event_result(window, function, event_id):
    """Define Result Event."""
    window.Connect(-1, -1, event_id, function)


def validate_color(color):
    """
    Helper function, returns True if color is a
    tuple of 3 integers in range <0, 256) (R, G, B)
    """
    if(isinstance(color, tuple)
       and len(color) == 3 and all((isinstance(cc, int) and 0 <= cc < 256) for cc in color)):
        return True

    return False


def closest_pixel(pixel, temp, colors):
    """Helper function, finds closest pixel color based on palette"""
    if pixel in temp:
        return temp[pixel]
    temp[pixel] = min(colors, key=lambda func: delta_E_CIE2000(pixel, func))
    return temp[pixel]


class ResultEvent(wx.PyEvent):  # pylint: disable=R0903
    """Simple event to send thread results"""

    def __init__(self, event_id, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(event_id)
        self.data = data
