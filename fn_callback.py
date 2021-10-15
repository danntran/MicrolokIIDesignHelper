import re

def txt2column(text):
    # replaces the unwarnted character and puts the input text all in 1 row
    # replaces , (comma) with newline
    output_txt = re.split(r'[\n,;]', text)
    return output_txt # returns text in a signal column

def formattxt(text, nrows, rmcomma):
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