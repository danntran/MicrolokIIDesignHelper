import subprocess
import os
import shutil
from tkinter import filedialog

def compileropencompilercallback():
    try:
        # TO DO: Need to add error check for correct file
        file_types = (('Microlok II/Genisys II Compiler', '*.exe'),('All files', '*.*'))
        openfile_text = filedialog.askopenfile(title='Open a file', filetypes=file_types)
    except: # opening file failed
        openfile_text = ''
    openfile_text.name
    return openfile_text.name

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_COMP = os.path.join(PROJECT_PATH, "compile\\gen2.exe")
PROJECT_FILE = os.path.join(PROJECT_PATH, "compile\\test")
compileropencompilercallback()
print(PROJECT_COMP)
print(PROJECT_FILE)
# p = os.system('start /wait cmd /k gen2.exe MO_GEN_11JAN21_23.gn2')
shutil.copy(PROJECT_COMP,PROJECT_FILE)
cmd_line = 'start cmd.exe /k \"C:\\gen2.exe\" \"C:\\MO_GEN_11JAN21_23.gn2\"'
print(cmd_line)
p = subprocess.Popen(cmd_line, shell=True)
print("hello world")
