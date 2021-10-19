import copy
import re
from tkinter import filedialog

def rm_commnewlinesfromtext(text):    
    # function removes all the comments from the text
    # input list of strings, outputs the list of strings no comments and no blank newlines
    nocomments_txt = []
    commentmode = commentmodepct = False
    # go through line by line
    for line in text:
        li = line.strip() # rm the whitespace left and right
        if li.startswith("/*"): # comment starting with /*
            commentmode = True
        if li.startswith("%"): # comment starting with %
            commentmodepct = True
        if li.endswith("*/") and commentmode: # end of /* with */
            commentmode = False
            continue
        if li.endswith("\\") and commentmodepct: # end of % with \
            commentmodepct = False
            continue
        if not commentmode and not commentmodepct:
            if "//" in li:
                idx = li.index("//") # comments with //
                nocomments_txt.append(li[:idx].strip()) # line contained comments remove
            elif "%" in li:
                idx = li.index("%") # single line comments with % \, WHY would you ever do this?!
                nocomments_txt.append(li[:idx].strip()) # line contained comments remove
            elif "/*" in li:
                idx = li.index("/*") # single line comments with /*, WHY would you ever do this?!
                nocomments_txt.append(li[:idx].strip()) # line contained comments remove
            else:
                nocomments_txt.append(li) # line with no comments                
    out_txt = list(filter(None, nocomments_txt)) # remove empty strings in the list
    return out_txt

def obtcomminfo(text):
    # obtains the comm from a text that has comments and newlines removed
    # returns dictionary in format: 
    #       LINK: (str) with link name
    #       PROTOCOL: (str) with protocol name
    #       PORT: (str) port number
    #       BAUD: (str) baud rate
    #       STOPBITS: (str) stopbits number
    #       PARITY: (str) parity type
    #       PEER.ADDRESS: (str) P2P address, else 'None' if not P2P
    #       STATION.NAME: (str) P2P station name, else 'None' if not P2P
    #       OUTPUT: (str) output bits in a long string
    #       INPUT: (str) input bits in a long string

    port_list = []
    comm_text = text[text.index('COMM'): [id for id, val in enumerate(text) if ('BOOLEAN BITS' in val)][-1]]
    # find every instance of LINK and put index into array
    link_indexes = [i for i, x in enumerate(comm_text) if x.startswith("LINK:")]
    link_indexes.append(None) # this adds a limit, to slice the list
    # loop through the comm_text and get the link index
    for link_idx in range(len(link_indexes)-1):
        param_list = {
                    'LINK:':None,'PROTOCOL:':None,'PORT:':None,'BAUD:':None,
                    'STOPBITS:':None,'PARITY:':None,'PEER.ADDRESS:':None,'STATION.NAME:':None
                    }
        # slice of comm_text showing link
        link_text = comm_text[link_indexes[link_idx]:link_indexes[link_idx+1]]
        # obtain link parameters: LINK, PROTOCOL, PORT, BAUD, STOPBIT, PARITY
        for index, line in enumerate(link_text):
            for key in param_list.keys():
                if key in line:
                    param_list[key]=((line.split(':'))[-1].strip()).replace(';','')
                    break
        # May have more than 1 address, Obtain the address index
        add_search_term = 'ADDRESS:'
        if param_list["PROTOCOL:"] == 'MII.PEER':
            # If p2p address is called MII.ADDRESS
            add_search_term = 'MII.ADDRESS:'
        # obtain the address indexes
        address_indexes = [i for i, x in enumerate(link_text) if x.startswith(add_search_term)]
        address_indexes.append(None) # this adds a limit, to slice the list
        for address_idx in range(len(address_indexes)-1):
            # slice the link_text showing the address info
            address_text = link_text[address_indexes[address_idx]:address_indexes[address_idx+1]]
            # Obtain the address
            param_list['ADDRESS:'] = (address_text[0].split(':'))[-1].strip()
            # Obtain the output and input bits for the address
            outputmode = inputmode = False
            output_text = ''
            input_text = ''
            for line in address_text:
                if param_list["PROTOCOL:"] == 'MII.PEER':
                    # if P2P get PEER.ADDRESS, and STATION.NAME
                    if 'PEER.ADDRESS' in line:
                        param_list['PEER.ADDRESS:'] = ((line.split(':'))[-1].strip()).replace(';','')
                    if 'STATION.NAME' in line:
                        param_list['STATION.NAME:'] = ((line.split(':'))[-1].strip()).replace(';','')
                else:
                    # not P2P make them None
                    param_list['PEER.ADDRESS:'] = None
                    param_list['STATION.NAME:'] = None

                if 'OUTPUT' in line:
                    outputmode = True
                if 'INPUT' in line:
                    inputmode = True
                if outputmode == True:
                    output_text += line + "\n"
                if inputmode == True:
                    input_text += line + "\n"
                if line.endswith(';'):
                    outputmode = inputmode = False
                    continue
            param_list['OUTPUT:'] = (output_text.split(':'))[-1].strip()
            param_list['INPUT:'] = (input_text.split(':'))[-1].strip()
            # finished getting all the info, put the dictionary into a list
            port_list.append(copy.deepcopy(param_list))
        # delete the dictionary to start again
        del(param_list)
    return port_list

def returnaddresslist(port_list, port_num):
    # input port_list and port number
    # output string of address from the chosen port e.g. '1 20 49 110 123'
    output_txt = ""
    if port_list and port_num:
        for links in port_list:
            if port_num in links["PORT:"]:
                output_txt += links["ADDRESS:"] + " "
    return output_txt

def returnportnumlist(port_list):
    # input port_list
    # output string of port for e.g. '1 2 3 4 '
    output_txt = ""
    if port_list:
        for links in port_list:
            if links["PORT:"] not in output_txt:
                output_txt += links["PORT:"] + " "
    return output_txt

def indexportinfofromaddr(port_list, address, port_num):
    # input portlist dictionary, address
    # returns index in port_list
    if port_list and address and port_num: # error check for blanks
        for idx, value in enumerate(port_list):
            if address in value["ADDRESS:"] and port_num in value["PORT:"]:
                return idx
    return None

def obtainportinfofromaddr(port_list, address, port_num):
    # input portlist dictionary, address
    # returns long string with port info for use in tkinter message box
    output_str = ''
    if port_list and address and port_num: # error check for blanks
        idx = indexportinfofromaddr(port_list, address, port_num)
        for key in port_list[idx].keys():
            if key in ['OUTPUT:', 'INPUT:']:
                # Don't include output and input info 
                continue
            output_str += str(port_list[idx][key]) + "\n"
    return output_str

def obtaininoutfromaddr(port_list, address, inputoutput, port_num):
    # input portlist dictionary, address, input or output
    # returns long str with input or output information
    output_str = ''
    if port_list and address and inputoutput: # error check for blanks
        idx = indexportinfofromaddr(port_list, address, port_num)
        output_str += str(port_list[idx][inputoutput])
    return output_str
    
def getfilename(text):
    # input text from readlines
    # output the filename as a string
    if text:
        text_ncomms = rm_commnewlinesfromtext(text)
        filenamelist = list(filter(None, re.split(r'[ ;]', text_ncomms[0])))
        return filenamelist[-1]
    return ''

# if __name__ == '__main__':
#     file_types = (
#                 ('Microlok II/Genisys II Files', ['*.ml2','*.gn2']),
#                 ('All files', '*.*'))
#     openfile_text = filedialog.askopenfile(title='Open a file', filetypes=file_types).read().splitlines()
#     portlist = rm_commnewlinesfromtext(openfile_text)
#     outfile = open('testfile.gn2','w')
#     for line in portlist:
#         outfile.writelines(line)
#         outfile.writelines('\n')
#     outfile.close()
#     print('1')