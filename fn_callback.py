import os
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
import re

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "MicrolokIIDesignHelperGUI.ui")

def closemenu():
    tk.destroy()

def txt2column(input_txt):
    # replaces the unwarnted character and puts the input text all in 1 row
    # replaces , (comma) with newline
    input_txt = input_txt.replace(" ", "") # spaces
    input_txt = input_txt.replace("\t", "") # tabs
    input_txt = input_txt.replace("\r", "") # CR
    input_txt = input_txt.replace("\n", "") # Newline
    input_txt = input_txt.replace(";", "\n") # semicolon
    input_txt = input_txt.replace(",", "\n") # comma to NL
    return input_txt

def formattxt(input_txt, nrows, rmcomma):
    # format the text to rows and shows/hides comma
    if nrows == 1: # only 1 column
        if rmcomma == 1:
            output_txt = input_txt
        else:
            text_array = input_txt.split('\n')
            output_txt = text_array[0]
            # go through the array 
            for idx, bit in enumerate(text_array[1:]):
                # check empty str
                if bit:
                    output_txt += ",\n" + bit
            output_txt += ';'
    else: # more than 1 column 
        if rmcomma == 1: # remove commas?
            ins_tab = '\t\t'
            ins_nl = '\n'
        else:
            ins_tab = ',\t\t'
            ins_nl = ',\n'
        # split the data into an array for easier formatting
        text_array = input_txt.split('\n')
        output_txt = text_array[0]
        # go through the array 
        for idx, bit in enumerate(text_array[1:]):
            # check for empty string
            if bit :
                # nl or tabs?
                if (idx + 1) % nrows == 0:
                    output_txt += ins_nl
                    if (idx + 1) % 8 == 0:
                        # add new linee every 8 bits
                        output_txt += '\n'
                else:
                    output_txt += ins_tab
                # concat the bit
                output_txt += bit
        if rmcomma == 0:
            # end of the list so add semi colon
            output_txt += ';'
    return output_txt

def ObtainNLines(input_text):
    # input into the Nbits slots b y counting the number of new lines - number of comments
    # returns a array with [Nlines, NBits]
    NNewlines = NComments = NSpares = 0
    NNewlines = input_text.count("\n")
    NComments = input_text.count("//")
    NSpares = input_text.count("SPARE")
    Nbits = NNewlines - NComments - NSpares
    return [NNewlines, Nbits]

