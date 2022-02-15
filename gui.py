import fn_callback as fn
import parse_document as parsedoc
import formatbits_dynamic as format
import subprocess
# Rebuild code down here
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pygubu

# File/project paths
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "MicrolokIIDesignHelperGUI.ui")

class MicrolokiidesignhelperguiApp:
    def __init__(self, master=None):
        # Front End Variables
        self.builder =  pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow_toplevel', master)
        self.builder.connect_callbacks(self)
        self.port_list = [None, None, None] # port info, 0=BF, 1=BC_file1, 2=BC_file2
        self.formatnrows = None
        self.removecomma = None
        self.sSuffix = None
        self.sPrefix = None
        self.builder.import_variables(self, ['sPrefix', 'formatnrows', 'removecomma', 'sSuffix'])
        self.file_types = (
            ('Microlok II/Genisys II Files', ['*.ml2','*.gn2']),
            ('All files', '*.*'))

        # Initialisation of Input/output list boxes
        (self.builder.get_object('BF_inoutlistbox')).insert(tk.END, *['INPUT:','OUTPUT:'])
        (self.builder.get_object('file1inoutlb')).insert(tk.END, *['INPUT:','OUTPUT:'])
        (self.builder.get_object('file2inoutlb')).insert(tk.END, *['INPUT:','OUTPUT:'])

        # Callback for the comboboxes
        # File 1 of bit comparator callbacks        
        (self.builder.get_object('file1addlb')).bind("<<ListboxSelect>>", self.file1loadbitscallback)
        (self.builder.get_object('file1portlb')).bind("<<ListboxSelect>>", self.file1loadaddresscallback)
        (self.builder.get_object('file1inoutlb')).bind("<<ListboxSelect>>", self.file1inoutcallback) #different callback cuz of the selection of input/output
        # File 2 of the bit comparator callbacks
        for CBs in ['file2inoutlb','file2addlb']:
            (self.builder.get_object(CBs)).bind("<<ListboxSelect>>", self.file2loadbitscallback)
        (self.builder.get_object('file2portlb')).bind("<<ListboxSelect>>", self.file2loadaddresscallback)
        # Bit formattor callbacks
        (self.builder.get_object('BF_PortListbox')).bind("<<ListboxSelect>>", self.BF_loadaddresscallback) # loadaddresscallback when PortListBox selected
        for CBs in ['BF_addresslistbox','BF_inoutlistbox']:
            (self.builder.get_object(CBs)).bind("<<ListboxSelect>>", self.BF_loadcallback) # loadcallback when addressLB or inoutLB selected
        (self.builder.get_object('PrefixEntry')).bind("<Return>", self.BF_loadcallback) # Press enter on the Prefix box
        (self.builder.get_object('SuffixEntry')).bind("<Return>", self.BF_loadcallback) # Press enter on the Suffix box
        
    def open_about_toplevel(self, *args):
        # Open About window
        builder2 = pygubu.Builder()
        builder2.add_resource_path(PROJECT_PATH)
        builder2.add_from_file(PROJECT_UI)
        builder2.get_object('about_toplevel')

    def portlistfileLB(self, filenameMSG, fileaddress, inout, portdataMSG, bitsTXT, portnum):
        # gets the port info for a given file 
        try:
            # TO DO: Need to add error check for correct file
            openfile_text = filedialog.askopenfile(title='Open a file', filetypes=self.file_types).read().splitlines()
        except: # opening file failed
            openfile_text = ''
            portlist = ''
        if openfile_text: # opened correctly
            portnumbox = self.builder.get_object(portnum)
            filenameinput = self.builder.get_object(filenameMSG)
            # clear the fields
            self.clearallfieldsLB(address=fileaddress, portinfoMSG=portdataMSG, textbox=bitsTXT, portnum=portnum)
            # get the file name and information
            filenameinput.configure(text=parsedoc.getfilename(openfile_text))
            portlist = parsedoc.obtcomminfo(parsedoc.rm_commnewlinesfromtext(openfile_text))
            portnumbox.insert(tk.END, *parsedoc.returnportnumlist(portlist))
        return portlist

    def loadaddresscallbackLB(self, portlist, fileaddress, portnum):
        # loads the addresses into the listbox
        portnumbox = self.builder.get_object(portnum)
        addressbox = self.builder.get_object(fileaddress)
        putnumboxval = portnumbox.get(portnumbox.curselection()) if portnumbox.curselection() else '' # check cursor select, if not return ''
        addlist = parsedoc.returnaddresslist(portlist, putnumboxval)
        addressbox.insert(tk.END, *addlist)

    def BF_openfilecallback(self, *args):
        # call back for bit formatter, open file
        filenameMSG = 'BF_filenameinput'
        fileaddressCB = 'BF_addresslistbox'
        inoutCB = 'BF_inoutlistbox'
        portdataMSG = 'portinfomessage'
        bitsTXT = 'InputTextBox'
        portnumCB = 'BF_PortListbox'
        self.port_list[0] = self.portlistfileLB(filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT, portnumCB)

    def BF_loadcallback(self, *args):
        # call back for bit formatter, load bit using the listbox
        addressbox = self.builder.get_object('BF_addresslistbox')
        inputoutputbox = self.builder.get_object('BF_inoutlistbox')
        portinfomessage = self.builder.get_object('portinfomessage')
        in_textbox = self.builder.get_object('InputTextBox')
        portnumbox = self.builder.get_object('BF_PortListbox')
        addressboxval = addressbox.get(addressbox.curselection()) if addressbox.curselection() else '' # check cursor select, if not return ''
        inoutval = inputoutputbox.get(inputoutputbox.curselection()) if inputoutputbox.curselection() else '' # check cursor select, if not return ''
        putnumboxval = portnumbox.get(portnumbox.curselection()) if portnumbox.curselection() else '' # check cursor select, if not return ''
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(self.port_list[0], addressboxval, putnumboxval)) # add info to the port info msgbox
        in_textbox.delete(1.0, tk.END) # delete odd data
        in_textbox.insert(tk.END, parsedoc.obtaininoutfromaddr(self.port_list[0], addressboxval, inoutval, putnumboxval)) # place new data
        self.bitformat_convertcallback() # run convert imediately as new data loaded

    def BF_loadaddresscallback(self, *args):
        # call back for the bit formatter for load addresses in box
        self.clearallfieldsLB(address='BF_addresslistbox', textbox='InputTextBox', portinfoMSG='portinfomessage') # clear fields
        self.loadaddresscallbackLB(self.port_list[0],'BF_addresslistbox','BF_PortListbox') 
    
    def clearallfieldsLB(self, address='', inout='', portinfoMSG='', textbox='', portnum=''):
        # clear the fields, addressCB, inputoutputCB, port information msg, input textbox
        if address: #listbox
            addressbox = self.builder.get_object(address)
            addressbox.delete(0, tk.END)
        if inout: # listbox
            inoutbox = self.builder.get_object(inout)
            inoutbox.delete(0, tk.END)
        if portinfoMSG: # message box
            portinfomsg = self.builder.get_object(portinfoMSG)
            portinfomsg.configure(text="")
        if textbox: # text box
            inputtextbox = self.builder.get_object(textbox)
            inputtextbox.delete(1.0, tk.END)
        if portnum: # listbox
            portnumbox = self.builder.get_object(portnum)
            portnumbox.delete(0, tk.END)

    def bitformat_convertcallback(self, *args):
        ## Format the text
        # Obtain the text from the text box
        in_textbox = self.builder.get_object('InputTextBox')
        input_txt = format.txt2column(in_textbox.get(1.0, tk.END))
        txt_presuffix = format.addprefixsuffix(input_txt, self.sPrefix.get(), self.sSuffix.get())
        formatted_txt = format.formattxt(txt_presuffix, self.formatnrows.get(), self.removecomma.get())
        # Print to the output text box
        out_textbox = self.builder.get_object('OutputTextBox')
        out_textbox.delete(1.0, tk.END)
        out_textbox.insert(tk.END, formatted_txt)
        ## Add to the Line and Bit count
        nlines, nbits = fn.ObtainNLines(input_txt)
        # Print to nline TB
        nlines_textbox = self.builder.get_object('TextNLines')
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nlines)
        # Print to nbit TB
        nlines_textbox = self.builder.get_object('TextNBits')
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nbits)

    def file1openfilecallback(self, *args):
        # callback for the file 1 open file
        filenameMSG = 'file1filename'
        fileaddress = 'file1addlb'
        inout = 'file1inoutlb'
        portdataMSG = 'file1portdata_message'
        bitsTXT = 'file1bits_text'
        portnum = 'file1portlb'
        # get port info and place in the dict
        self.port_list[1] = self.portlistfileLB(filenameMSG, fileaddress, inout, portdataMSG, bitsTXT, portnum)

    def file1inoutcallback(self, *args):
        # callback which looks at whether input or output is selected on file 1 and chooses the opposite on file 2
        f1inoutcursel = (self.builder.get_object('file1inoutlb')).curselection() # get highlighted pos
        if f1inoutcursel: # may not be highlighted
            f2inoutform = self.builder.get_object('file2inoutlb')
            f2inoutform.selection_clear(f1inoutcursel[0])
            f2inoutform.activate(1 - f1inoutcursel[0]) # activate the other pos
            f2inoutform.selection_set(1 - f1inoutcursel[0])
        self.file1loadbitscallback()
        self.file2loadbitscallback()

    def file1loadbitscallback(self, *args):
        # callback for the file 1 load bits
        fileaddress = 'file1addlb'
        inout = 'file1inoutlb'
        portdataMSG = 'file1portdata_message'
        bitsTXT = 'file1bits_text'
        portnum = 'file1portlb'
        nbitsform = 'file1nbits_text'
        nlinesform = 'file1nlines_text'
        outputform = 'bitcompare_textbox'
        portlist = self.port_list[1]
        addressbox = self.builder.get_object(fileaddress)
        inputoutputbox = self.builder.get_object(inout)
        portinfomessage = self.builder.get_object(portdataMSG)
        portnumbox = self.builder.get_object(portnum)
        addressboxval = addressbox.get(addressbox.curselection()) if addressbox.curselection() else ''
        inoutval = inputoutputbox.get(inputoutputbox.curselection()) if inputoutputbox.curselection() else ''
        putnumboxval = portnumbox.get(portnumbox.curselection()) if portnumbox.curselection() else ''
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(portlist, addressboxval, putnumboxval))
        input_txt = format.txt2column(parsedoc.obtaininoutfromaddr(portlist, addressboxval, inoutval, putnumboxval))
        formatted_txt = format.formattxt(input_txt, 1, True)
        # Print to the output text box
        out_textbox = self.builder.get_object(bitsTXT)
        out_textbox.delete(1.0, tk.END)
        out_textbox.insert(tk.END, formatted_txt)
        ## Add to the Line and Bit count
        nlines, nbits = fn.ObtainNLines(input_txt)
        # Print to nline TB
        nlines_textbox = self.builder.get_object(nlinesform)
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nlines)
        # Print to nbit TB
        nbits_textbox = self.builder.get_object(nbitsform)
        nbits_textbox.delete(1.0, tk.END)
        nbits_textbox.insert(tk.END, nbits)
        # clear comparison
        outputtxtbox = self.builder.get_object(outputform)
        outputtxtbox.delete(1.0, tk.END)
    
    def file1loadaddresscallback(self, *args):
        # CB for bit comp file 1
        self.clearallfieldsLB(address='file1addlb', textbox='file1bits_text', portinfoMSG='file1portdata_message')
        self.loadaddresscallbackLB(self.port_list[1],'file1addlb','file1portlb')

    def file2openfilecallback(self, *args):
        # callback for the file 2 open file
        filenameMSG = 'file2filename'
        fileaddress = 'file2addlb'
        inout = 'file2inoutlb'
        portdataMSG = 'file2portdata_message'
        bitsTXT = 'file2bits_text'
        portnum = 'file2portlb'
        self.port_list[2] = self.portlistfileLB(filenameMSG, fileaddress, inout, portdataMSG, bitsTXT, portnum)

    def file2loadbitscallback(self, *args):
        # callback for the file 2 load bits
        fileaddress = 'file2addlb'
        inout = 'file2inoutlb'
        portdataMSG = 'file2portdata_message'
        bitsTXT = 'file2bits_text'
        portnum = 'file2portlb'
        nbitsform = 'file2nbits_text'
        nlinesform = 'file2nlines_text'
        outputform = 'bitcompare_textbox'
        portlist = self.port_list[2]
        addressbox = self.builder.get_object(fileaddress)
        inputoutputbox = self.builder.get_object(inout)
        portinfomessage = self.builder.get_object(portdataMSG)
        portnumbox = self.builder.get_object(portnum)
        addressboxval = addressbox.get(addressbox.curselection()) if addressbox.curselection() else ''
        inoutval = inputoutputbox.get(inputoutputbox.curselection()) if inputoutputbox.curselection() else ''
        putnumboxval = portnumbox.get(portnumbox.curselection()) if portnumbox.curselection() else ''
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(portlist, addressboxval, putnumboxval))
        input_txt = format.txt2column(parsedoc.obtaininoutfromaddr(portlist, addressboxval, inoutval, putnumboxval))
        formatted_txt = format.formattxt(input_txt, 1, True)
        # Print to the output text box
        out_textbox = self.builder.get_object(bitsTXT)
        out_textbox.delete(1.0, tk.END)
        out_textbox.insert(tk.END, formatted_txt)
        ## Add to the Line and Bit count
        nlines, nbits = fn.ObtainNLines(input_txt)
        # Print to nline TB
        nlines_textbox = self.builder.get_object(nlinesform)
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nlines)
        # Print to nbit TB
        nbits_textbox = self.builder.get_object(nbitsform)
        nbits_textbox.delete(1.0, tk.END)
        nbits_textbox.insert(tk.END, nbits)
        # clear comparison
        outputtxtbox = self.builder.get_object(outputform)
        outputtxtbox.delete(1.0, tk.END)

    def file2loadaddresscallback(self, *args):
        self.clearallfieldsLB(address='file2addlb', textbox='file2bits_text', portinfoMSG='file2portdata_message')
        self.loadaddresscallbackLB(self.port_list[2],'file2addlb','file2portlb')

    def comparebitscallback(self, *args):
        # call back for the compare button
        bits1_textbox = self.builder.get_object('file1bits_text')
        bits2_textbox = self.builder.get_object('file2bits_text')
        [nerrors, compare_resultstr] = fn.comparebits(bits1_textbox.get(1.0, tk.END), bits2_textbox.get(1.0, tk.END))
        compare_textbox = self.builder.get_object('bitcompare_textbox')
        compare_textbox.delete(1.0, tk.END)
        compare_textbox.insert(tk.END, ('NUMBER OF ERRORS: ' + str(nerrors) + '\n'))
        compare_textbox.insert(tk.END, compare_resultstr)
    
    def compileropencompilercallback(self):
        compfile_textbox = self.builder.get_object('compiler_compilername_combobox')
        try:
            # TO DO: Need to add error check for correct file
            file_types = (('Microlok II/Genisys II Compiler', '*.exe'),('All files', '*.*'))
            openfile_text = filedialog.askopenfile(title='Open a file', filetypes=file_types)
            compfile_textbox.set(openfile_text.name)
        except: # opening file failed
            openfile_text = ''
            compfile_textbox.set("")        
        return 1
        
    def compileropenfilecallback(self):
        file_textbox = self.builder.get_object('compiler_filename_combobox')
        try:
            # TO DO: Need to add error check for correct file
            openfile_text = filedialog.askopenfile(title='Open a file', filetypes=self.file_types)
            file_textbox.set(openfile_text.name)
        except: # opening file failed
            openfile_text = ''
            file_textbox.set("")        
        return 1

    def compilecallback(self):
        compfile_textbox = self.builder.get_object('compiler_compilername_combobox')
        file_textbox = self.builder.get_object('compiler_filename_combobox')
        cmd_line = 'start cmd.exe /k "' + compfile_textbox.get() + '" "' + file_textbox.get() + '"'
        print(cmd_line)
        subprocess.Popen(cmd_line, shell=True)

    def run(self):
        self.mainwindow.mainloop()

# main
if __name__ == '__main__':
    app = MicrolokiidesignhelperguiApp()
    app.run()