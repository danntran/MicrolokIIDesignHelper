import copy

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

def obtcomminfo(text):
    # obtains the comm from a text that has comments and newlines removed
    # returns dictionary in format: 
    # [name of link, protocol, address, port num, baud]
    # If p2p: [link name, protocol, MII address, Station Name, peer address]
    port_list = []
    comm_text = text[text.index('COMM'): [id for id, val in enumerate(text) if ('BOOLEAN BITS' in val)][-1]]
    # find every instance of LINK and put index into array
    link_indexes = [i for i, x in enumerate(comm_text) if x.startswith("LINK:")]
    link_indexes.append(None) # this adds a limit, to slice the list
    # loop through the comm_text and get the link index
    for link_idx in range(len(link_indexes)-1):
        param_list = {
                    'LINK:':None,'PROTOCOL:':None,'PORT:':None,'BAUD:':None,
                    'STOPBITS:':None,'PARITY:':None
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
                    output_text += line
                if inputmode == True:
                    input_text += line
                if line.endswith(';'):
                    outputmode = inputmode = False
                    continue
            param_list['OUTPUT:'] = (output_text.split(':'))[-1]
            param_list['INPUT:'] = (input_text.split(':'))[-1]
            # finished getting all the info, put the dictionary into a list
            port_list.append(copy.deepcopy(param_list))
        # delete the dictionary to start again
        del(param_list)
    return port_list

# TEST CODE BELOW
if __name__ == "__main__":
    file = open('test_mlk.ml2','r')
    words = file.read().splitlines()
    file.close()

    txt = rm_commnewlinesfromtext(words)
    port_list = obtcomminfo(txt)

    print(port_list[0]["PORT:"])
    # output to a file
    write_file = open("output_test.ml2", "w")
    for lines in txt:
        write_file.write(lines)
        write_file.write("\n")
    for address in port_list:
        for key in address.keys():
            write_file.write(str(key) + " : " + str(address[key]) + "\n")
        write_file.write("\n")
    write_file.close()