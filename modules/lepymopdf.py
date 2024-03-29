"""
LePyMoPDF module

This module contains LePyMoPDF class.
LePyMoPDF class is used to generate pdf.
"""

from collections import Counter
from PIL import Image
from fpdf import FPDF

from modules.utilities import _PDF_FORMATS


class LePyMoPDF(FPDF):
    """LePyMoPDF class"""

    def __init__(self, image_src, image_scaled, start_date, pdf_format):
        """Init LePyMoPDF class"""
        if pdf_format not in _PDF_FORMATS.keys():
            pdf_format = "A4"
        super().__init__(format=pdf_format)
        self._abort = 0
        self.pdf_format = pdf_format
        self.pdf_width = _PDF_FORMATS[self.pdf_format]["pdf_width"]
        self.pdf_height = _PDF_FORMATS[self.pdf_format]["pdf_height"]
        self.image_src = Image.open(image_src)
        self.image_scaled = image_scaled
        self.start_date = start_date
        self.colors = Counter(self.image_src.getdata())
        self.image_width, self.image_height = self.image_src.size

    def main_page(self):
        """Generates main page of PDF"""
        self.add_page()
        y_pos = _PDF_FORMATS[self.pdf_format]["page_y_pos"]
        self.big_header("LePyMo", _PDF_FORMATS[self.pdf_format]["deafult_header_margin_top"])
        self.small_header("Lego Python Mosaic", y_pos)

        y_pos += _PDF_FORMATS[self.pdf_format]["small_header_margin"]
        self.set_xy((self.pdf_width - _PDF_FORMATS[self.pdf_format]["main_page_image_size"]) // 2, y_pos)
        self.image(self.image_scaled, link='', type='',
                   w=_PDF_FORMATS[self.pdf_format]["main_page_image_size"],
                   h=_PDF_FORMATS[self.pdf_format]["main_page_image_size"])

        y_pos += _PDF_FORMATS[self.pdf_format]["medium_header_margin"] + _PDF_FORMATS[self.pdf_format]["main_page_image_size"]
        self.medium_header("Build instructions for your image", y_pos)

        y_pos += _PDF_FORMATS[self.pdf_format]["medium_header_margin"]
        self.small_header(f"Dimensions: {self.image_width} x {self.image_height} bricks", y_pos)

        y_pos += _PDF_FORMATS[self.pdf_format]["small_header_margin"]
        self.small_header(f"Bricks in total: {self.image_width * self.image_height}", y_pos)

        y_pos += _PDF_FORMATS[self.pdf_format]["medium_header_margin"]
        self.medium_header("Bricks by color:", y_pos)

        y_pos += _PDF_FORMATS[self.pdf_format]["medium_header_margin"]

        for color, qty in self.colors.items():
            if self._abort == 1:
                return
            if y_pos + _PDF_FORMATS[self.pdf_format]["small_brick_margin"] > _PDF_FORMATS[self.pdf_format]["page_max_y_pos"]:
                self.add_page()
                y_pos = _PDF_FORMATS[self.pdf_format]["medium_header_margin"]
            self.small_brick(_PDF_FORMATS[self.pdf_format]["small_brick_x_pos"],
                             y_pos - _PDF_FORMATS[self.pdf_format]["small_brick_margin"] / 2, color)
            self.brick_text(f"x {qty} {color}", _PDF_FORMATS[self.pdf_format]["small_brick_text_x_pos"], y_pos)
            y_pos += _PDF_FORMATS[self.pdf_format]["small_brick_margin"]

        y_pos += _PDF_FORMATS[self.pdf_format]["medium_header_margin"]
        if y_pos + _PDF_FORMATS[self.pdf_format]["medium_header_font_size"] > _PDF_FORMATS[self.pdf_format]["page_max_y_pos"]:
            self.add_page()
            y_pos = _PDF_FORMATS[self.pdf_format]["page_y_pos"]

        self.big_header("Have fun!", y_pos)

    def build_step(self, step):
        """Generates a single step of the building instructions"""
        current_row = []
        img_data = list(self.image_src.getdata())
        img_data = img_data[step * self.image_width:(step + 1) * self.image_width]
        for index, value in enumerate(img_data):
            if self._abort == 1:
                return
            if index % self.image_width == 0:
                current_data = {
                    "color": value,
                    "count": 1
                }
                current_row.append(current_data)
            else:
                current_value = img_data[index - 1]
                if value == current_value:
                    current_row[-1]["count"] += 1
                else:
                    current_data = {
                        "color": value,
                        "count": 1
                    }
                    current_row.append(current_data)

        if self._abort == 1:
            return

        self.add_page()
        self.big_header("Step " + str(step + 1), _PDF_FORMATS[self.pdf_format]["deafult_header_margin_top"])
        row_colors = Counter(list(self.image_src.getdata())[step * self.image_width:(step + 1) * self.image_width])

        y_pos = _PDF_FORMATS[self.pdf_format]["page_y_pos"] + _PDF_FORMATS[self.pdf_format]["small_header_margin"]
        self.small_header("You'll need in this step:", y_pos)
        y_pos += _PDF_FORMATS[self.pdf_format]["small_header_margin"]

        for color, qty in row_colors.items():
            if self._abort == 1:
                return
            if y_pos + _PDF_FORMATS[self.pdf_format]["small_brick_margin"] > _PDF_FORMATS[self.pdf_format]["page_max_y_pos"]:
                self.add_page()
                y_pos = _PDF_FORMATS[self.pdf_format]["medium_header_margin"]
            self.small_brick(_PDF_FORMATS[self.pdf_format]["small_brick_x_pos"],
                             y_pos - _PDF_FORMATS[self.pdf_format]["small_brick_margin"] / 2, color)
            self.brick_text(f"x {qty} {color}", _PDF_FORMATS[self.pdf_format]["small_brick_text_x_pos"], y_pos)
            y_pos += _PDF_FORMATS[self.pdf_format]["small_brick_margin"]

        y_pos += _PDF_FORMATS[self.pdf_format]["medium_header_margin"]
        self.small_header("Bricks from left to the right:", y_pos)

        y_pos += _PDF_FORMATS[self.pdf_format]["small_header_margin"]
        for current_row_element in current_row:
            if self._abort == 1:
                return
            if y_pos + _PDF_FORMATS[self.pdf_format]["small_brick_margin"] > _PDF_FORMATS[self.pdf_format]["page_max_y_pos"]:
                self.add_page()
                y_pos = _PDF_FORMATS[self.pdf_format]["medium_header_margin"]
            self.small_brick(_PDF_FORMATS[self.pdf_format]["small_brick_x_pos"],
                             y_pos - _PDF_FORMATS[self.pdf_format]["small_brick_margin"] / 2,
                             current_row_element["color"])
            self.brick_text(f"x {current_row_element['count']} {str(current_row_element['color'])}",
                            _PDF_FORMATS[self.pdf_format]["small_brick_text_x_pos"], y_pos)
            y_pos += _PDF_FORMATS[self.pdf_format]["small_brick_margin"]

    def big_header(self, header_text, from_top):
        """Adds a big header to the current page"""
        self.set_font('Arial', '', _PDF_FORMATS[self.pdf_format]["big_header_font_size"])
        self.text((self.pdf_width - self.get_string_width(header_text)) / 2, from_top, header_text)

    def medium_header(self, header_text, from_top):
        """Adds a medium header to the current page"""
        self.set_font('Arial', '', _PDF_FORMATS[self.pdf_format]["medium_header_font_size"])
        self.text((self.pdf_width - self.get_string_width(header_text)) / 2, from_top, header_text)

    def small_header(self, header_text, from_top):
        """Adds a small header to the current page"""
        self.set_font('Arial', '', _PDF_FORMATS[self.pdf_format]["small_header_font_size"])
        self.text((self.pdf_width - self.get_string_width(header_text)) / 2, from_top, header_text)

    def footer(self):
        """Adds a small footer to the current page with link to project's Github"""
        if self.page_no() > 1:
            footer_text = "Generated using LePyMo"
            self.set_font('Arial', '', _PDF_FORMATS[self.pdf_format]["footer_font_size"])
            self.set_text_color(222, 222, 222)
            self.text((self.pdf_width - self.get_string_width(footer_text)) / 2,
                      _PDF_FORMATS[self.pdf_format]["footer_text_y_pos"], footer_text)
            self.link(x=(self.pdf_width - self.get_string_width(footer_text)) / 2, y=_PDF_FORMATS[self.pdf_format]["footer_link_y"],
                      w=self.get_string_width(footer_text), h=_PDF_FORMATS[self.pdf_format]["footer_link_height"],
                      link='https://github.com/kjuraszek/lego-python-mosaic/')
            self.set_text_color(0, 0, 0)
            self.set_font('Arial', '', _PDF_FORMATS[self.pdf_format]["paging_font_size"])
            current_page = f'- {self.page_no()} -'
            self.text((self.pdf_width - self.get_string_width(current_page)) / 2,
                      _PDF_FORMATS[self.pdf_format]["paging_y_pos"], current_page)

    def brick_text(self, text, position_x, position_y):
        """Adds a brick text to the page"""
        self.set_font('Arial', '', _PDF_FORMATS[self.pdf_format]["small_brick_font_size"])
        self.text(position_x, position_y, text)

    def small_brick(self, position_x, position_y, color):
        """Adds a brick to the page"""
        self.set_fill_color(*color)
        self.set_xy(position_x, position_y)
        self.cell(_PDF_FORMATS[self.pdf_format]["small_brick_size"], _PDF_FORMATS[self.pdf_format]["small_brick_size"], fill=True, border=1)
        self.ellipse(position_x + _PDF_FORMATS[self.pdf_format]["small_brick_ellipsis_pos"],
                     position_y + _PDF_FORMATS[self.pdf_format]["small_brick_ellipsis_pos"],
                     _PDF_FORMATS[self.pdf_format]["small_brick_ellipsis_size"],
                     _PDF_FORMATS[self.pdf_format]["small_brick_ellipsis_size"])

    def abort(self):
        """Stops creating PDF"""
        self._abort = 1
