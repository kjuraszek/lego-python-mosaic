"""
utilities module

This module contains common constants, functions and classes.
"""

import re
import wx
from colour.difference import delta_E_CIE2000

_FILES_SUFFIXES = ["_mosaic.png", "_mosaic_scaled.png", "_mosaic_instructions.pdf"]

_PDF_FORMATS = {
    "A4": {
        "pdf_width": 210,
        "pdf_height": 297,
        "big_header_font_size": 38,
        "medium_header_font_size": 24,
        "small_header_font_size": 14,
        "footer_font_size": 10,
        "footer_text_y_pos": 294,
        "footer_link_y": 290,
        "footer_link_height": 5,
        "paging_y_pos": 290,
        "paging_font_size": 16,
        "page_y_pos": 20,
        "page_max_y_pos": 280,
        "main_page_image_size": 60,
        "small_header_margin": 5,
        "medium_header_margin": 10,
        "deafult_header_margin_top": 12,
        "small_brick_font_size": 14,
        "small_brick_x_pos": 75,
        "small_brick_text_x_pos": 85,
        "small_brick_margin": 8,
        "small_brick_size": 5,
        "small_brick_ellipsis_pos": 1.0,
        "small_brick_ellipsis_size": 3.0
    },
    "A5": {
        "pdf_width": 148,
        "pdf_height": 210,
        "big_header_font_size": 26,
        "medium_header_font_size": 16,
        "small_header_font_size": 10,
        "footer_font_size": 7,
        "footer_text_y_pos": 206,
        "footer_link_y": 203,
        "footer_link_height": 4,
        "paging_y_pos": 203,
        "paging_font_size": 11,
        "page_y_pos": 14,
        "page_max_y_pos": 196,
        "main_page_image_size": 42,
        "small_header_margin": 4,
        "medium_header_margin": 7,
        "deafult_header_margin_top": 8,
        "small_brick_font_size": 10,
        "small_brick_x_pos": 52,
        "small_brick_text_x_pos": 60,
        "small_brick_margin": 6,
        "small_brick_size": 4,
        "small_brick_ellipsis_pos": 0.75,
        "small_brick_ellipsis_size": 2.5
    },
}


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


def validate_hex_color(color):
    """
    Helper function, returns True if color is a
    valid HEX color
    """
    pattern = r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"
    result = re.match(pattern, color)
    return bool(result)


def convert_hex_to_rgb(color):
    """
    Helper function, returns True if color is a
    tuple of 3 integers in range <0, 256) (R, G, B)
    """
    if len(color) == 3:
        color = ''.join(c * 2 for c in color)
    color = [color[i] + color[i + 1] for i in range(0, len(color), 2)]
    return tuple(int(i, 16) for i in color)


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
