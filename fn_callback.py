# --------------------------- #
# --- Function Definitons --- #
# --------------------------- #
# Functions for the 

import re

def txt2column(text):
    # Splits the long string into a list delimited by \n, ',' and ';'
    # input: bits/text in long string
    # output: bits/text in a list delimited by newline, comma and semicolon
    output_txt = []
    for bit in re.split(r'[\n,;]', text):
        if bit.strip(): # check for empty string
            output_txt.append(bit.strip())
    return output_txt # returns text in a signal column

def ObtainNLines(input_text):
    # input into the Nbits slots b y counting the number of new lines - number of comments
    # returns a array with [Nlines, NBits]
    NNewlines = NComments = NSpares = 0
    NNewlines = len(input_text)
    NComments = input_text.count("//")
    NSpares = input_text.count("SPARE")
    Nbits = NNewlines - NComments - NSpares
    return [NNewlines, Nbits] # returns Num NL and Num bits

def comparebits(inputlist1, inputlist2):
    # input 2 strings and outputs a string which tells the user which bits dont match 
    # INPUT: inputlist1 - (string) input/output bits of a port
    #        inputlist2 - (string) input/output bits of a port
    # OUTPUT: (int) nerrors (-1, cannot compare, 0 no errors, >0 number of errors), (string) list of errors
    errorlist = ''
    nerrors = 0
    bitlist1 = inputlist1.split('\n')
    bitlist2 = inputlist2.split('\n')
    if len(bitlist1) == len(bitlist2): # same length
        for idx, val in enumerate(list(zip(bitlist1,bitlist2))): #traverse through list
            if (val[0] not in val[1]) or (val[1] not in val[0]):
                nerrors += 1
                errorlist += 'BIT ' + str(idx) + ' ERROR: [' + str(val[0]) + '] : [' + str(val[1]) +'] - MISMATCH!\n'
        if not errorlist:
            errorlist += 'NO ERRORS: ALL BITS MATCH!'
    else: # not same length
        nerrors = -1
        errorlist += 'ERROR: ASSIGNED BITS HAVE DIFFERENT LENGTHS'
    return [nerrors, errorlist]