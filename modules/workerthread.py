"""
LePyMo Workerthread module

This module contains WorkerThread class.
Thread is responsible of generating image and pdf.
"""

import os
import pathlib
import datetime
import threading
import wx
from PIL import Image
from modules.lepymopdf import LePyMoPDF
from modules.utilities import ResultEvent, _FILES_SUFFIXES, closest_pixel


class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window, image_path, palette, nopdf, event_id, pdf_format):  # pylint: disable=R0913
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self._abort = 0
        self._target = self.run_thread
        self.image_path = image_path
        self.palette = palette
        self.pdf = False
        self.nopdf = nopdf
        self.pdf_format = pdf_format
        self.event_id = event_id
        self.run_date = False
        self.start()

    def run_thread(self):
        """Run Thread - generate image and pdf"""

        # pylint: disable=R0915
        self.run_date = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        temp = {}

        try:
            src_image = Image.open(pathlib.Path(self.image_path))
        except:
            src_image = False

        if src_image and self._abort == 0:
            try:
                event_data = {"event_type": "status_change", "status": "Calculating pixels"}
                wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))
                result = []
                image_width, image_height = src_image.size
                for index, pixel_color in enumerate(list(src_image.getdata())):
                    if image_width * image_height > 10000 and index % 10000 == 0:
                        # update status change by 10000 pixels only for larger images
                        event_data = {
                            "event_type": "status_change",
                            "status": f"Calculating pixel {index} / {image_width * image_height}"}
                        wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))

                    if self._abort == 1:
                        return

                    result.append(closest_pixel(pixel_color, temp, self.palette))

                event_data = {"event_type": "status_change", "status": "Generating image"}
                wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))

                src_image.putdata(result)
                mosaic_name = self.run_date + "_mosaic.png"
                mosaic_name_scaled = self.run_date + "_mosaic_scaled.png"
                src_image.save(mosaic_name)
                scaled_height = 400
                scale = scaled_height / image_height
                output_image = src_image.resize((int(scale * image_width), scaled_height))
                output_image.save(mosaic_name_scaled)

                if not self.nopdf and self._abort == 0:

                    self.pdf = LePyMoPDF(mosaic_name, mosaic_name_scaled, self.run_date, self.pdf_format)
                    self.pdf.main_page()
                    for i in range(image_height):
                        event_data = {"event_type": "status_change", "status": f"Creating PDF page {i+1} / {image_height}"}
                        wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))
                        self.pdf.build_step(i)
                        if self._abort == 1:
                            return

                    event_data = {"event_type": "status_change", "status": "Building PDF"}
                    wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))
                    self.pdf.output(self.run_date + "_mosaic_instructions.pdf", "F")
                    self.pdf = False

                if self._abort == 0:
                    event_data = {"event_type": "status_change", "status": "Idle"}
                    wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))

                    event_data = {"event_type": "result", "status": True}
                    wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))

            except:
                event_data = {"event_type": "status_change", "status": "Idle"}
                wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))

                event_data = {"event_type": "result", "status": False}
                wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))
                return

        elif self._abort == 0:
            event_data = {"event_type": "status_change", "status": "Idle"}
            wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))

            event_data = {"event_type": "result", "status": False}
            wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))

    def abort(self):
        """Helper function, stops current WorkerThread"""
        if self.pdf and isinstance(self.pdf, LePyMoPDF):
            self.pdf.abort()

        self._abort = 1
        if self.run_date:
            filenames = [self.run_date + suffix for suffix in _FILES_SUFFIXES]
            for filename in filenames:
                if filename in os.listdir('.'):
                    try:
                        os.remove(filename)
                    except:
                        error_message = f"LePyMo Was unable to remove {filename}, try to remove it manually."
                        wx.MessageBox(message=error_message, caption="Removing file failed", style=wx.OK | wx.ICON_ERROR)

        event_data = {"event_type": "status_change", "status": "Idle"}
        wx.PostEvent(self._notify_window, ResultEvent(self.event_id, event_data))
