# lego+python=mosaic
 Program LePyMo was developed to simplify creating mosaic from images using Lego-like bricks.

 ![LePyMo - main window](./img/lepymo-main-window.jpg "LePyMo - main window")
## The idea
 I was thinking about a birthday gift for my fiancée, and I came with this concept - to create a mosaic using our pictures and Lego bricks.

## How does it work ?
 Firstly this program transforms selected image to a palette of certain colors. 
 After that LePyMo creates a PDF containing building instructions for this new image.

## How to run LePyMo ?
 There are 3 ways to run this program:

### Using LePyMo.exe created by myself
 This is the easiest one - just download .exe from [here](https://kjuraszek.pl/lego-python-mosaic/).

### Running script
 #### Using Makefile - Linux only

 Clone this repository to your hard drive with:
 #### `git clone https://github.com/kjuraszek/lego-python-mosaic`

 Set virtual environment and install dependecies:
 #### `make venv && make reqs`

 Run program:
 #### `make run`

 Create executable:
 #### `make reqs-dev && make dist`

 #### Windows
 
 It's a good idea to create and activate a virtual environment first using e.g. `virtualnenv`.

 Clone this repository to your hard drive with:
 #### `git clone https://github.com/kjuraszek/lego-python-mosaic`

 Install packages in project directory using e.g. `pip` and `requirements.txt` file.
 #### `pip3 install -r requirements.txt`

 Run program:
 #### `python3 lepymo.py`

### Creating .exe on your own
 This is a similar way to the previous one. Instead of running .py script - you build an executable file (.exe).
 You can use pyinstaller:
 #### `pyinstaller --onefile --windowed --icon=app.ico --version-file=version.txt lepymo.py`

## How to use it ?

First you have to prepare your desired image - its dimensions (in pixels) must be equal to 
the size (in bricks) of mosaic you are planning to create. E.g. when your plate is 50 by 50 
bricks, your image dimensions must be 50px by 50px. 

The next step is to add colors to your palette. Keep in mind that some colors aren't used in brick production - you are limited to less than 300 colors. At this stage it is better to keep Don't generate PDF option turned on to test 
selected color palette. The process of creating desired image can take even up to a few minutes - 
it depends on amount of colors in your palette and dimensions of image. 

You also can add colors to the palette using .csv file - look at `example-colors.csv` file. Each row represents one color, and each column - red (R), green (G) or blue (B) part of color (in that order). You can use HEX instead of RGB format of the colors - insert a full color respresentation (with `#` symbol) in the first column. Each column must be separated with semicolon `;` and each row with a newline.

When you are satisfied with output image you can turn off Don't generate PDF option. This process also can take up to a
few minutes - it depends on amount of colors in your palette and dimensions of image. The PDF 
consists of total bricks amount of each color and building instructions divided in steps - each 
step is one row.

You can stop current action using Abort button - all files created in current run will be removed. You can clear inputs (source image, color palette, No PDF checkbox) using Clear button.

Have fun!

### Brick colors in real life

Here are some links which might be useful to determine your color palette (based on bricks used in real sets):
- [Ryan Howerter's website](http://ryanhowerter.net/colors.php)
- [brickset.com](https://brickset.com/colours)
- [rebrickable.com](https://rebrickable.com/colors/)
- [brickipedia.com](https://brickipedia.fandom.com/wiki/Colour_Palette)

## Disclaimer
 LEGO® is a trademark of the LEGO Group of companies which does not sponsor, authorize or endorse this project.

 ## Examples
 ### Build instructions:
 ![LePyMo - Building instructions main page](./img/lepymo-1.jpg "LePyMo - Building instructions main page")
 ![LePyMo - Building instructions step 11](./img/lepymo-2.jpg "LePyMo - Building instructions step 11")
 ![LePyMo - Building instructions Sandro](./img/lepymo-5.jpg "LePyMo - Building instructions Sandro")
 ### Final effect:
![LePyMo - final effect](./img/lepymo-6.jpg "LePyMo - final effect")
![LePyMo - final effect](./img/lepymo-3.jpg "LePyMo - final effect")
 ### Mosaic timelapse:
(click to watch it on Youtube)
[![Lego Mosaic Timelapse Video](./img/lepymo-4.jpg "Lego Mosaic Timelapse Video")](https://youtu.be/oBODOYErHhU)
