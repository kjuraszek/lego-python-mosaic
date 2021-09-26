"""
LePyMo Frame module

This is application's main frame.
"""

import sys
import csv
import wx
import wx.lib.scrolledpanel as scrolled
from modules.utilities import event_result
from modules.workerthread import WorkerThread


class LePyMoFrame(wx.Frame):
    """LePyMo main frame class"""

    def __init__(self):
        """Init LePyMo Class."""
        wx.Frame.__init__(self, None, wx.ID_ANY, "LePyMo", size=(240, 500))

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.selected_file = ""
        self.palette = {}
        self.nopdf = True
        self.event_id = wx.ID_ANY
        self.input_ids = []
        self.worker = None
        self.version = (0, 0, 0, 4)

        event_result(self, self.on_result, self.event_id)

        self.scrolled_panel = scrolled.ScrolledPanel(self.panel, -1,
                                                     style=wx.TAB_TRAVERSAL |
                                                     wx.SUNKEN_BORDER, name="MainPanel")
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()

        self.file_sizer = wx.BoxSizer(wx.VERTICAL)
        self.palette_sizer = wx.BoxSizer(wx.VERTICAL)
        self.colors_sizer = wx.GridSizer(cols=2, hgap=2, vgap=2)
        self.csv_sizer = wx.BoxSizer(wx.VERTICAL)
        self.generate_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_sizer = wx.BoxSizer(wx.VERTICAL)

        self.scrolled_panel.SetSizer(self.palette_sizer)

        self.select_file_label = wx.StaticText(self.panel, wx.ID_ANY,
                                               label="Select source image:",
                                               name="selectFileLabel")
        self.select_file_status = wx.StaticText(self.panel, wx.ID_ANY,
                                                label="File: Not selected",
                                                name="selectFileStatus")

        self.file_picker = wx.FilePickerCtrl(self.panel, id=wx.ID_ANY, path="",
                                             message="Open image file",
                                             style=wx.FLP_DEFAULT_STYLE)
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_change)
        self.input_ids.append(self.file_picker.GetId())

        color_palette_label = wx.StaticText(self.panel, wx.ID_ANY,
                                            label="Color palette:",
                                            name="colorPalette")

        self.file_sizer.AddSpacer(10)
        self.file_sizer.Add(self.select_file_label)
        self.file_sizer.Add(self.file_picker)
        self.file_sizer.Add(self.select_file_status)
        self.file_sizer.AddSpacer(10)
        self.file_sizer.Add(color_palette_label)

        self.palette_sizer.AddSpacer(10)

        add_btn = wx.Button(self.panel, wx.ID_ANY, label="Add color")
        self.color_picker = wx.ColourPickerCtrl(self.panel, wx.ID_ANY)
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_color)

        self.input_ids.append(add_btn.GetId())

        self.colors_sizer.Add(self.color_picker)
        self.colors_sizer.Add(add_btn)

        self.select_csv_file_label = wx.StaticText(self.panel, wx.ID_ANY,
                                                   label="Add colors from .CSV file:",
                                                   name="selectCSVFileLabel")
        self.csv_file_picker = wx.FilePickerCtrl(self.panel, id=wx.ID_ANY, path="",
                                                 message="Add colors from .CSV file",
                                                 style=wx.FLP_OPEN|wx.FLP_FILE_MUST_EXIST)
        self.csv_file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_colors_load)
        self.input_ids.append(self.csv_file_picker.GetId())
        self.csv_sizer.Add(self.select_csv_file_label)
        self.csv_sizer.Add(self.csv_file_picker)

        self.nopdf_checkbox = wx.CheckBox(self.panel, wx.ID_ANY, label="Don't generate PDF")
        self.nopdf_checkbox.SetValue(True)
        self.nopdf_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        self.input_ids.append(self.nopdf_checkbox.GetId())

        nopdf_checkbox_info = wx.StaticText(self.panel, wx.ID_ANY,
                                            label="(Use this option to test\n "
                                            "your color palette.)", name="colorPalette")

        generate_btn = wx.Button(self.panel, wx.ID_ANY, label="Generate PDF and image")
        generate_btn.Bind(wx.EVT_BUTTON, self.on_generate)
        self.input_ids.append(generate_btn.GetId())

        self.generate_sizer.Add(self.nopdf_checkbox)
        self.generate_sizer.Add(nopdf_checkbox_info)
        self.generate_sizer.AddSpacer(10)
        self.generate_sizer.Add(generate_btn)

        abort_btn = wx.Button(self.panel, wx.ID_ANY, label="Abort")
        abort_btn.Bind(wx.EVT_BUTTON, self.on_abort)
        clear_btn = wx.Button(self.panel, wx.ID_ANY, label="Clear")
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        self.input_ids.append(clear_btn.GetId())
        self.buttons_sizer.Add(abort_btn)
        self.buttons_sizer.Add(clear_btn)

        self.lepymo_status = wx.StaticText(self.panel, wx.ID_ANY,
                                           label='Status: Idle', name="lepymoStatus")
        self.status_sizer.Add(self.lepymo_status)

        panel_sizer = wx.BoxSizer(wx.VERTICAL)

        panel_sizer.Add(self.file_sizer, 0, wx.ALIGN_LEFT)
        panel_sizer.Add(self.scrolled_panel, 1, wx.EXPAND)
        panel_sizer.AddSpacer(10)
        panel_sizer.Add(self.colors_sizer, 0, wx.ALIGN_LEFT)
        panel_sizer.AddSpacer(10)
        panel_sizer.Add(self.csv_sizer, 0, wx.ALIGN_LEFT)
        panel_sizer.AddSpacer(20)
        panel_sizer.Add(self.generate_sizer, 0, wx.ALIGN_LEFT)
        panel_sizer.AddSpacer(10)
        panel_sizer.Add(self.buttons_sizer, 0, wx.ALIGN_LEFT)
        panel_sizer.AddSpacer(30)
        panel_sizer.Add(self.status_sizer, 0, wx.ALIGN_LEFT)
        panel_sizer.AddSpacer(5)

        self.panel.SetSizer(panel_sizer)

        file_menu = wx.Menu()

        exit_item = file_menu.Append(-1, "Close", "Close program")

        help_menu = wx.Menu()
        info_item = help_menu.Append(-1, "Info", "Info")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "File")
        menu_bar.Append(help_menu, "Help")

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_info, info_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_CLOSE, self.on_exit)


        if sys.executable.lower().endswith("lepymo.exe"):
            icon = wx.Icon(sys.executable, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)
        # except:
        #     wx.MessageBox(message="Loading program icon failed",
        #                   caption="Loading program icon failed",
        #                   style=wx.OK | wx.ICON_ERROR)

    def on_add_color(self, _):
        """Helper function, adds color from color picker to the palette"""
        color_from_picker = self.color_picker.GetColour()
        color = tuple(color_from_picker[:3])
        if color not in self.palette.values():
            self.add_color_to_palette(color)
            self.scrolled_panel.Layout()
            self.scrolled_panel.SetupScrolling()
        else:
            wx.MessageBox(message="This color has already been added to the palette.",
                          caption="Color duplicate",
                          style=wx.OK)

    def on_file_change(self, _):
        """Helper function, changes selected file label"""
        self.selected_file = self.file_picker.GetPath()
        select_file_text = "File: " + (self.selected_file if self.selected_file else "Not selected")
        self.select_file_status.SetLabel(select_file_text)

    def on_checkbox_change(self, _):
        """Helper function, changes checkbox value"""
        self.nopdf = not self.nopdf

    def on_colors_load(self, _):
        """Helper function, loads colors from CSV file"""
        csv_file_path = self.csv_file_picker.GetPath()
        colors = []
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';', quotechar='|')
                rows = list(csv_reader)

        except:
            wx.MessageBox(message="Loading colors failed",
                          caption="Unable to open CSV file",
                          style=wx.OK | wx.ICON_ERROR)

        for row in rows:
            if len(row) == 3:
                color_tuple = tuple(int(z) for z in row if z.isdigit())
                if len(color_tuple) == 3 and color_tuple not in self.palette.values():
                    colors.append(color_tuple)

        colors = list(set(colors))
        added_colors = 0
        for color in colors:
            if self.add_color_to_palette(color):
                added_colors += 1

        self.scrolled_panel.Layout()
        self.scrolled_panel.SetupScrolling()
        wx.MessageBox(message=f"{added_colors} color{'s' if added_colors != 1 else ''} "
                              f"have been added to the palette ",
                      caption="Added colors", style=wx.OK)

    def add_color_to_palette(self, color):
        """Helper function, adds color to the palette"""
        if self.validate_color(color):
            color_rect = wx.StaticText(self.scrolled_panel, label=20 * " ")
            color_rect.SetBackgroundColour(color)

            btn = wx.Button(self.scrolled_panel, wx.ID_ANY, label="Remove")
            btn.Bind(wx.EVT_BUTTON, self.remove_color, id=btn.GetId())

            color_label = wx.StaticText(self.scrolled_panel, label=f'rgb{color}',
                                        name="colorLabel")
            single_color = wx.GridSizer(cols=2, hgap=2, vgap=2)
            single_color.AddMany([color_rect, btn, color_label])

            self.palette[btn.GetId()] = color
            self.palette_sizer.Add(single_color)
            return True

        return False

    def validate_color(self, color):
        """
        Helper function, returns True if color is a
        tuple of 3 integers in range <0, 256) (R, G, B)
        """
        if (isinstance(color, tuple) and
            len(color) == 3 and
            all((isinstance(cc, int) and 0 <= cc < 256) for cc in color)):
            return True

        return False

    def remove_color(self, event):
        """Helper function, removes color from the palette"""
        btn = event.GetEventObject()
        self.palette.pop(btn.GetId(), None)
        btn.GetPrevSibling().Destroy()
        btn.GetNextSibling().Destroy()
        btn.Destroy()
        self.scrolled_panel.Layout()
        self.scrolled_panel.SetupScrolling()

    def on_generate(self, _):
        """Function initiates WorkerThread"""
        if len(self.palette) == 0 or self.selected_file == '':
            error_message = ""
            if len(self.palette) == 0:
                error_message += "Color palette is empty. "
            if self.selected_file == '':
                error_message += "No file selected."

            wx.MessageBox(message=error_message,
                          caption="Generating image and pdf failed",
                          style=wx.OK | wx.ICON_ERROR)

        else:
            self.set_status("Starting")
            self.disable_inputs()
            self.worker = WorkerThread(self, self.selected_file,
                                       list(self.palette.values()),
                                       self.nopdf, self.event_id)

    def disable_inputs(self):
        """Helper function, disables inputs"""
        inputs = self.input_ids + list(self.palette.keys())
        for input_id in inputs:
            input_widget = self.panel.FindWindowById(input_id)
            if input_widget and getattr(input_widget, "Disable", None):
                input_widget.Disable()

    def enable_inputs(self):
        """Helper function, enables inputs"""
        self.set_status("Idle")
        inputs = self.input_ids + list(self.palette.keys())
        for input_id in inputs:
            input_widget = self.panel.FindWindowById(input_id)
            if input_widget and getattr(input_widget, "Enable", None):
                input_widget.Enable()

    def set_status(self, status):
        """Helper function, sets text on status label"""
        self.lepymo_status.SetLabel(f'Status: {status}')

    def on_result(self, event):
        """Helper function, shows WorkerThread result"""
        if event.data is not None and event.data["event_type"] is not None:
            if event.data["event_type"] == "result":
                if event.data["status"] is None or event.data["status"] is False:
                    wx.MessageBox(message="Generating image and pdf failed",
                                  caption="Generating image and pdf failed",
                                  style=wx.OK | wx.ICON_ERROR)
                else:
                    wx.MessageBox(message="Finished!", caption="Finished!", style=wx.OK)

                self.worker = None
                self.enable_inputs()

            elif event.data["event_type"] == "status_change":
                self.set_status(event.data["status"])

    def on_info(self, _):
        """Helper function, shows messagebox"""
        wx.MessageBox(
            message="This program was developed to simplify creating mosaic from images using Lego-like bricks. "
                    "Firstly this program transforms selected image to a palette of certain colors. After that it "
                    "creates a PDF containing building instructions for this new image. "
                    "\n\nFirst you have to prepare your desired image - its dimensions (in pixels) must be equal to "
                    "the size (in bricks) of mosaic you are planning to create. E.g. when your plate is 50 by 50 "
                    "bricks, your image dimensions must be 50px by 50px.\n\nThe next step is to add colors to your "
                    "palette. Keep in mind that some colors aren't used in brick production - you are limited to less "
                    "than 300 colors. At this stage it is better to keep Don't generate PDF option turned on to test "
                    "selected color palette. The process of creating desired image can take even up to a few minutes - "
                    "it depends on amount of colors in your palette and dimensions of image.\nYou also can add "
                    "colors to the palette using .csv file - look at example-colors.csv file. Each row represents "
                    "one color, and each column - red (R), green (G) or blue (B) part of color (in that order). Each "
                    "column must be separated with semicolon ; and each row with a newline.\n\nWhen you are satisfied "
                    "with output image you can turn off Don't generate PDF option. This process also can take up to a"
                    "few minutes - it depends on amount of colors in your palette and dimensions of image. The PDF "
                    "consists of total bricks amount of each color and building instructions divided in steps - each "
                    "step is one row.\n\nYou can stop current action using Abort button - all files created in "
                    "current run will be removed. You can clear inputs (source image, color palette, No PDF checkbox) "
                    "using Clear button.\n\nHave fun!\n\nLePyMo version: " + ".".join([str(num) for num in self.version]),
            caption="Info",
            style=wx.OK | wx.ICON_INFORMATION)

    def on_clear(self, _):
        """Helper function, clears all input fields"""
        if self.worker is None:
            palette_sizer_children = list(self.palette_sizer.GetChildren())
            while len(palette_sizer_children) > 1:
                self.palette_sizer.Hide(len(palette_sizer_children) - 1)
                self.palette_sizer.Remove(len(palette_sizer_children) - 1)
                palette_sizer_children = list(self.palette_sizer.GetChildren())

            self.palette = {}
            self.selected_file = ""
            self.file_picker.SetPath("")
            self.select_file_status.SetLabel("Not selected")
            self.nopdf = True
            self.nopdf_checkbox.SetValue(True)
            self.palette_sizer.Layout()

    def on_abort(self, event):
        """Helper function, aborts current action"""
        if self.worker:
            dialog = wx.MessageDialog(self, message="Are you sure you want to abort current action?", caption="Abort?",
                                      style=wx.YES_NO, pos=wx.DefaultPosition)
            response = dialog.ShowModal()
            if response == wx.ID_YES and self.worker:
                self.worker.abort()

                self.worker = None
                wx.MessageBox(message="Action aborted.", caption="Action aborted", style=wx.OK)
                self.enable_inputs()
            else:
                event.StopPropagation()
        else:
            wx.MessageBox(message="There's nothing to abort !", caption="Unable to abort", style=wx.OK)

    def on_exit(self, event):
        """Helper function, shows messagebox on exit attempt"""
        dialog = wx.MessageDialog(self, message="Are you sure you want to quit?", caption="Quit?",
                                  style=wx.YES_NO, pos=wx.DefaultPosition)
        response = dialog.ShowModal()

        if response == wx.ID_YES:
            self.exit_program(event)
        else:
            event.StopPropagation()

    def exit_program(self, _):
        """Helper function, aborts worker and exits program"""
        if self.worker:
            self.worker.abort()
            self.worker = None
        self.Destroy()
