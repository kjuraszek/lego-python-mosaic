"""
LePyMo Main module

This module runs the main loop.
"""
import wx
from modules.lepymoframe import LePyMoFrame


if __name__ == "__main__":
    app = wx.App(False)
    frame = LePyMoFrame().Show()
    app.MainLoop()
