import wx


_FILES_SUFFIXES = ["_mosaic.png", "_mosaic_scaled.png", "_mosaic_instructions.pdf"]

def event_result(window, function, event_id):
    """Define Result Event."""
    window.Connect(-1, -1, event_id, function)


class ResultEvent(wx.PyEvent):
    """Simple event to send thread results"""

    def __init__(self, event_id, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(event_id)
        self.data = data
