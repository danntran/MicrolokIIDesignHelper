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
