# MicrolokIIDesignHelper
 Tools to help write data for Microlok II Railway interlocking

To build: pyinstaller gui.py --add-data "MicrolokIIDesignHelperGUI.ui;." --add-data "MLKIIDesignHelperLogo_Large.ico;." --collect-all "pygubu" --name MLKIIDesignHelper --icon "MLKIIDesignHelperLogo_Large.ico" --noconsole --onefile

## Changelog:
### [1.0.0] - < 2021-10-09
#### Changes
- First Version, Migrated Over CSVtoLineConvertor
- Renamed CSVtoLineConvertor to BitFormatter
- Added ability to remove commas from the formatted bits in BitFormatter
- Added ability to format the bits in 1, 2, 4 or 8 columns.

### [2.0.0] - < 2021-10-18
#### Changes
- Added Bit comparator
- Bit comparator gives the ability to select 2 files, choose the address, input and output and compare whether the bits align.
- Bit formatter can now read ml2/gn2 files and automatically extract the bit input and output information