import re

def txt2column(text):
    # input: file in long string
    # replaces the unwarnted character and puts the input text all in 1 row
    # replaces , (comma) with newline
    output_txt = re.split(r'[\n,;]', text)
    return output_txt # returns text in a signal column

def formattxt1(text, nrows, rmcomma):
    # format the text to rows and shows/hides comma
    if nrows == 1: # only 1 column
        if rmcomma == 1:
            output_txt = '\n'.join(text)
        else:
            output_txt = text[0]
            # go through the array 
            for idx, bit in enumerate(text[1:]):
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
        output_txt = text[0]
        # go through the array 
        for idx, bit in enumerate(text[1:]):
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
    NNewlines = len(input_text)
    NComments = input_text.count("//")
    NSpares = input_text.count("SPARE")
    Nbits = NNewlines - NComments - NSpares
    return [NNewlines, Nbits] # returns Num NL and Num bits

in_text = """//hello
ND458HZR.N123.N128,             ND458HHZR.N123.N128,
ND458DZR.N123.N128,             SPARE,
NU458HZR.N123.N128,             NU458HHZR.N123.N128,
NU458DZR.N123.N128,             SPARE,
BU_MO.DL.DN.FLPR.N123.N128,     BU_MO.UL.DN.FLPR.N123.N128,
439BT1PR.N123.N128,             439BT1CPR.N123.N128,
439ATS1PR.N123.N128,            425CT1PR.N123.N128,
458CT1PR.N123.N128,             458CT1CPR.N123.N128,
444ATS1PR.N123.N128,            444BT1PR.N123.N128,
SPARE,                          SPARE,
SPARE,                          SPARE,
SPARE,                          SPARE;"""

text1 = txt2column(in_text)
text2 = formattxt1(text1,2,1)
Nlines, Nbits = ObtainNLines(text1)
print(text1, text2, Nlines, Nbits)