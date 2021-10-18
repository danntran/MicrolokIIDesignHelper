import re

def txt2column(text):
    # Splits the long string into a list delimited by \n, ',' and ';'
    # input: bits/text in long string
    # output: bits/text in a list delimited by newline, comma and semicolon
    output_txt = []
    for bit in re.split(r'[\n,;]', text):
        if bit: # check for empty string
            output_txt.append(bit.strip())
    return output_txt # returns text in a signal column

def formattxt(text, ncols, rmcomma):
    # formats the text based on how many columns the user wants and if they want commas
    # formats the text from list of strings to 
    # input: text- bits/text in a list delimited by newline, comma and semicolon. Valid: List of stings
    #        nrows- number of rows the user want to put the formted txt into. Valid: 1,2,4,8
    #        rmcomma- user want to remove the comma? Valid: 0-remain commas, 1-remove commas
    # output: a long sting
    if text: # check not empty list
        if ncols == 1: # only 1 column
            if rmcomma == 1: # no commas
                output_txt = '\n'.join(text)
            else: # yes commas
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
                    # put into columns defined by user
                    if (idx + 1) % ncols == 0:
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
    return '' # reutn empty string if input list is empty

def ObtainNLines(input_text):
    # input into the Nbits slots b y counting the number of new lines - number of comments
    # returns a array with [Nlines, NBits]
    NNewlines = NComments = NSpares = 0
    NNewlines = len(input_text)
    NComments = input_text.count("//")
    NSpares = input_text.count("SPARE")
    Nbits = NNewlines - NComments - NSpares
    return [NNewlines, Nbits] # returns Num NL and Num bits

def rm_commnewlinesfromtext(text):    
    # function removes all the comments from the text 
    # input list of strings, outputs the list of strings no comments, no blank newlines
    # and stripped of white space before and after each element
    nocomments_txt = []
    commentmode = commentmodepct = False
    # go through line by line
    for line in text:
        li = line.strip() # rm the whitespace left and right
        if li.startswith("/*"): # comment starting with /*
            commentmode = True
        if li.startswith("%"): # comment starting with %
            commentmodepct = True
        if li.endswith("*/"): # end of /* with */
            commentmode = False
            continue
        if li.endswith("\\"): # end of % with \
            commentmodepct = False
            continue
        if not commentmode and not commentmodepct:
            try:
                idx = li.index("//") # comments with //
            except:
                nocomments_txt.append(li) # line with no comments
            else:
                nocomments_txt.append(li[:idx].strip()) # line contained comments remove
    out_txt = list(filter(None, nocomments_txt)) # remove empty strings in the list
    return out_txt

def comparebits(inputlist1, inputlist2):
    # input 2 strings and outputs a string which tells the user which bits dont match 
    # INPUT: inputlist1 - (string) input/output bits of a port
    #        inputlist2 - (string) input/output bits of a port
    # OUTPUT: (string) list of errors
    errorlist = ''
    bitlist1 = inputlist1.split('\n')
    bitlist2 = inputlist2.split('\n')
    if len(bitlist1) == len(bitlist2): # same length
        for idx, val in enumerate(list(zip(bitlist1,bitlist2))): #traverse through list
            if val[0] != val[1]:
                errorlist += 'BIT ' + str(idx) + ' ERROR: [' + str(val[0]) + '] : [' + str(val[1]) +'] - MISMATCH!\n'
        if not errorlist:
            errorlist += 'NO ERRORS: ALL BITS MATCH!'
    else: # not same length
        errorlist += 'ERROR: ASSIGNED BITS HAVE DIFFERENT LENGTHS'
    return errorlist