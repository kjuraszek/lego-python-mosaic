from PIL import Image
from fpdf import FPDF
from collections import Counter


class LePyMoPDF(FPDF):
    """LePyMoPDF class"""

    def __init__(self, image_src, image_scaled, start_date):
        """Init LePyMoPDF class"""
        super().__init__()
        self._abort = 0
        self.pdf_width = 210
        self.pdf_height = 297
        self.image_src = Image.open(image_src)
        self.image_scaled = image_scaled
        self.start_date = start_date
        self.colors = Counter(self.image_src.getdata())
        self.image_width, self.image_height = self.image_src.size

    def main_page(self):
        """Generates main page of PDF"""
        self.add_page()
        self.big_header("LePyMo")
        self.small_header("Lego Python Mosaic", 20)

        self.set_xy(self.pdf_width / 2 - 30, 25)
        self.image(self.image_scaled, link='', type='', w=60, h=60)

        self.medium_header("Build instructions for your image", 95)
        self.small_header(f"Dimensions: {self.image_width} x {self.image_height} bricks", 105)
        self.small_header(f"Bricks in total: {self.image_width * self.image_height}", 110)
        self.medium_header("Bricks by color:", 120)
        y_pos = 130

        for color, qty in self.colors.items():
            if self._abort == 1:
                return
            if 280 < y_pos + 8:
                self.add_page()
                y_pos = 10
            self.small_brick(75, y_pos - 4, color)
            self.brick_text(f"x {qty} {color}", 85, y_pos)
            y_pos += 8

        y_pos += 10
        if 280 < y_pos + 30:
            self.add_page()
            y_pos = 20

        self.big_header("Have fun!", y_pos)

    def build_step(self, step):
        """Generates a single step of the building instructions"""
        current_row = []
        img_data = list(self.image_src.getdata())
        img_data = img_data[step * self.image_width:(step + 1) * self.image_width]
        for i, x in enumerate(img_data):
            if self._abort == 1:
                return
            if i % self.image_width == 0:
                d = {
                    "color": x,
                    "count": 1
                }
                current_row.append(d)
            else:
                p = img_data[i - 1]
                if x == p:
                    current_row[-1]["count"] += 1
                else:
                    d = {
                        "color": x,
                        "count": 1
                    }
                    current_row.append(d)

        if self._abort == 1:
            return

        self.add_page()
        self.big_header("Step " + str(step + 1))
        row_colors = Counter(list(self.image_src.getdata())[step * self.image_width:(step + 1) * self.image_width])
        y_pos = 25
        self.small_header("You'll need in this step:", y_pos)
        y_pos += 5

        for color, qty in row_colors.items():
            if self._abort == 1:
                return
            if 280 < y_pos + 8:
                self.add_page()
                y_pos = 10
            self.small_brick(75, y_pos - 4, color)
            self.brick_text(f"x {qty} {color}", 85, y_pos)
            y_pos += 8

        y_pos += 10
        self.small_header("Bricks from left to the right:", y_pos)
        y_pos += 5
        for r in current_row:
            if self._abort == 1:
                return
            if 280 < y_pos + 8:
                self.add_page()
                y_pos = 10
            self.small_brick(75, y_pos - 4, r["color"])
            self.brick_text(f"x {r['count']} {str(r['color'])}", 85, y_pos)
            y_pos += 8

    def big_header(self, header_text, from_top=12):
        """Adds a big header to the current page"""
        self.set_font('Arial', '', 38)
        self.text((self.pdf_width - self.get_string_width(header_text)) / 2, from_top, header_text)

    def medium_header(self, header_text, from_top=12):
        """Adds a medium header to the current page"""
        self.set_font('Arial', '', 24)
        self.text((self.pdf_width - self.get_string_width(header_text)) / 2, from_top, header_text)

    def small_header(self, header_text, from_top=12):
        """Adds a small header to the current page"""
        self.set_font('Arial', '', 14)
        self.text((self.pdf_width - self.get_string_width(header_text)) / 2, from_top, header_text)

    def brick_text(self, text, x, y):
        """Adds a brick text to the page"""
        self.set_font('Arial', '', 14)
        self.text(x, y, text)

    def small_brick(self, x, y, color):
        """Adds a brick to the page"""
        self.set_fill_color(*color)
        self.set_xy(x, y)
        self.cell(5, 5, fill=True, border=1)
        self.ellipse(x + 1.0, y + 1.0, 3, 3)

    def abort(self):
        """Stops creating PDF"""
        self._abort = 1
