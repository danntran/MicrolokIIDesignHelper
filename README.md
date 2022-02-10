# MicrolokIIDesignHelper
 Tools to help write data for Microlok II Railway interlocking

Packages Used:
- pygubu
- pygubu-designer
- pyinstaller 

To build: 
pyinstaller gui.py --add-data "MicrolokIIDesignHelperGUI.ui;." --add-data "MLKIIDesignHelperLogo_Large.ico;." --collect-all "pygubu" --name MLKIIDesignHelper --icon "MLKIIDesignHelperLogo_Large.ico" --noconsole --onefile

## Changelog:
### [3.2.0] - < 2022-02-10
#### Changes
- Removed buttons from bitformator and comparator.
- Changed layout of loading bits.
- Selecting Input/Output on File 1 will automatically inverse on file 2.

### [3.1.0] - < 2021-11-20
#### Changes
- Bit Formator no longer uses Tabs but determines the amount of spaces needed betweens bits.

### [3.0.0] - < 2021-10-20
#### Changes
- Added Compiler but doesn't work due to the MLK2 compiler limitations

### [2.0.0] - < 2021-10-18
#### Changes
- Added Bit comparator
- Bit comparator gives the ability to select 2 files, choose the address, input and output and compare whether the bits align.
- Bit formatter can now read ml2/gn2 files and automatically extract the bit input and output information

### [1.0.0] - < 2021-10-09
#### Changes
- First Version, Migrated Over CSVtoLineConvertor
- Renamed CSVtoLineConvertor to BitFormatter
- Added ability to remove commas from the formatted bits in BitFormatter
- Added ability to format the bits in 1, 2, 4 or 8 columns.