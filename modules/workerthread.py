import wx
import pathlib
import datetime
import threading
from PIL import Image
from colour.difference import delta_E_CIE2000
from modules.lepymopdf import LePyMoPDF
from modules.utilities import ResultEvent


class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window, image_path, palette, nopdf, event_id):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self._abort = 0
        self._target = self.run_thread
        self.image_path = image_path
        self.palette = palette
        self.pdf = False
        self.nopdf = nopdf
        self.event_id = event_id
        self.start()

    def run_thread(self):
        """Run Thread - generate image and pdf"""

        run_date = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        temp = {}

        try:
            src_image = Image.open(pathlib.Path(self.image_path))
        except:
            src_image = False

        if src_image and self._abort == 0:
            try:
                result = []
                image_width, image_height = src_image.size
                for pixel_color in list(src_image.getdata()):
                    if self._abort == 1:
                        return

                    result.append(self.closest_pixel(pixel_color, temp, self.palette))

                src_image.putdata(result)
                mosaic_name = run_date + "_mosaic.png"
                mosaic_name_scaled = run_date + "_mosaic_scaled.png"
                src_image.save(mosaic_name)
                scaled_height = 400
                scale = scaled_height / image_height
                output_image = src_image.resize((int(scale * image_width), scaled_height))
                output_image.save(mosaic_name_scaled)

                if not self.nopdf and self._abort == 0:
                    self.pdf = LePyMoPDF(mosaic_name, mosaic_name_scaled, run_date)
                    self.pdf.main_page()
                    self.pdf.build_steps()
                    self.pdf.output(run_date + "_mosaic_instructions.pdf", "F")
                    self.pdf = False

                if self._abort == 0:
                    wx.PostEvent(self._notify_window, ResultEvent(self.event_id, True))

            except:
                wx.PostEvent(self._notify_window, ResultEvent(self.event_id, False))
                return

        elif self._abort == 0:
            wx.PostEvent(self._notify_window, ResultEvent(self.event_id, False))

    def closest_pixel(self, pixel, temp, colors):
        """Helper function, finds closest pixel color based on palette"""
        if pixel in temp:
            return temp[pixel]
        n = min(colors, key=lambda func: delta_E_CIE2000(pixel, func))
        temp[pixel] = n
        return temp[pixel]

    def abort(self):
        self._abort = 1
        if self.pdf and isinstance(self.pdf, LePyMoPDF):
            self.pdf.abort()

