import fn_callback as fn
import parse_document as parsedoc
import subprocess
# Rebuild code down here
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pygubu

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "MicrolokIIDesignHelperGUI.ui")

class MicrolokiidesignhelperguiApp:
    def __init__(self, master=None):
        self.builder =  pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow_toplevel', master)
        self.builder.connect_callbacks(self)
        self.port_list = [None, None, None]
        self.formatnrows = None
        self.removecomma = None
        self.builder.import_variables(self, ['formatnrows', 'removecomma'])
        self.file_types = (
            ('Microlok II/Genisys II Files', ['*.ml2','*.gn2']),
            ('All files', '*.*'))


        # Callback for the comboboxes        
        (self.builder.get_object('bitcomp_portcombobox')).bind("<<ComboboxSelected>>", self.bitformat_loadaddresscallback)
        for CBs in ['file1inout_combobox','file1address_combobox']:
            (self.builder.get_object(CBs)).bind("<<ComboboxSelected>>", self.file1loadbitscallback)
        for CBs in ['file2inout_combobox','file2address_combobox']:
            (self.builder.get_object(CBs)).bind("<<ComboboxSelected>>", self.file2loadbitscallback)
        (self.builder.get_object('file1port_combobox')).bind("<<ComboboxSelected>>", self.file1loadaddresscallback)
        (self.builder.get_object('file2port_combobox')).bind("<<ComboboxSelected>>", self.file2loadaddresscallback)
    
    def portlistfile(self, filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT, portnumCB):
        # gets theport info for a given file 
        try:
            # TO DO: Need to add error check for correct file
            openfile_text = filedialog.askopenfile(title='Open a file', filetypes=self.file_types).read().splitlines()
        except: # opening file failed
            openfile_text = ''
            portlist = ''
        if openfile_text:
            portnumcombobox = self.builder.get_object(portnumCB)
            filenameinput = self.builder.get_object(filenameMSG)
            addresscombobox = self.builder.get_object(fileaddressCB)
            # clear the fields
            self.clearallfields(fileaddressCB,inoutCB,portdataMSG,bitsTXT,portnumCB)
            # get the file name
            filenameinput.configure(text=parsedoc.getfilename(openfile_text))
            portlist = parsedoc.obtcomminfo(parsedoc.rm_commnewlinesfromtext(openfile_text))
            portnumcombobox['values'] = parsedoc.returnportnumlist(portlist)
        return portlist
    
    def loadaddresscallback(self, portlist, fileaddressCB, portnumCB):
        portnumcombobox = self.builder.get_object(portnumCB)
        addresscombobox = self.builder.get_object(fileaddressCB)
        addresscombobox['values'] = parsedoc.returnaddresslist(portlist, portnumcombobox.get())
        

    def open_about_toplevel(self, *args):
        # Open About window
        builder2 = pygubu.Builder()
        builder2.add_resource_path(PROJECT_PATH)
        builder2.add_from_file(PROJECT_UI)
        builder2.get_object('about_toplevel')

    def bitformat_convertcallback(self, *args):
        ## Format the text
        # Obtain the text from the text box
        in_textbox = self.builder.get_object('InputTextBox')
        input_txt = fn.txt2column(in_textbox.get(1.0, tk.END))
        formatted_txt = fn.formattxt(input_txt, self.formatnrows.get(), self.removecomma.get())
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

    def bitformat_openfilecallback(self, *args):
        # call back for bit formatter, open file
        filenameMSG = 'filenameinput'
        fileaddressCB = 'addresscombobox'
        inoutCB = 'inputoutputcombobox'
        portdataMSG = 'portinfomessage'
        bitsTXT = 'InputTextBox'
        portnumCB = 'bitcomp_portcombobox'
        self.port_list[0] = self.portlistfile(filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT, portnumCB)
    
    def bitformat_loadcallback(self, *args):
        # call back for bit formatter, load bit
        addresscombobox = self.builder.get_object('addresscombobox')
        inputoutputcombobox = self.builder.get_object('inputoutputcombobox')
        portinfomessage = self.builder.get_object('portinfomessage')
        in_textbox = self.builder.get_object('InputTextBox')
        portnumcombobox = self.builder.get_object('bitcomp_portcombobox')
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(self.port_list[0], addresscombobox.get(), portnumcombobox.get()))
        in_textbox.delete(1.0, tk.END)
        in_textbox.insert(tk.END, parsedoc.obtaininoutfromaddr(self.port_list[0], addresscombobox.get(), inputoutputcombobox.get(), portnumcombobox.get()))

    def bitformat_loadaddresscallback(self, *args):
        self.clearallfields(addressCB='addresscombobox', inoutCB='inputoutputcombobox', textbox='InputTextBox', portinfoMSG='bitcomp_portcombobox')
        self.loadaddresscallback(self.port_list[0],'addresscombobox','bitcomp_portcombobox')
        
    def clearallfields(self, addressCB='', inoutCB='', portinfoMSG='', textbox='', portnumCB=''):
        # clear the fields, addressCB, inputoutputCB, port information msg, input textbox
        if addressCB:
            addresscombobox = self.builder.get_object(addressCB)
            addresscombobox.set("")
        if inoutCB:
            inoutcombobox = self.builder.get_object(inoutCB)
            inoutcombobox.set("")
        if portinfoMSG:
            portinfomsg = self.builder.get_object(portinfoMSG)
            portinfomsg.configure(text="")
        if textbox:
            inputtextbox = self.builder.get_object(textbox)
            inputtextbox.delete(1.0, tk.END)
        if portnumCB:
            portnumcombobox = self.builder.get_object(portnumCB)
            portnumcombobox.set("")

    def file1openfilecallback(self, *args):
        # callback for the file 1 open file
        filenameMSG = 'file1name_input'
        fileaddressCB = 'file1address_combobox'
        inoutCB = 'file1inout_combobox'
        portdataMSG = 'file1portdata_message'
        bitsTXT = 'file1bits_text'
        portnumCB = 'file1port_combobox'
        self.port_list[1] = self.portlistfile(filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT, portnumCB)

    def file1loadbitscallback(self, *args):
        # callback for the file 1 load bits
        fileaddressCB = 'file1address_combobox'
        inoutCB = 'file1inout_combobox'
        portdataMSG = 'file1portdata_message'
        bitsTXT = 'file1bits_text'
        portnumCB = 'file1port_combobox'
        portlist = self.port_list[1]
        addresscombobox = self.builder.get_object(fileaddressCB)
        inputoutputcombobox = self.builder.get_object(inoutCB)
        portinfomessage = self.builder.get_object(portdataMSG)
        portnumcombobox = self.builder.get_object(portnumCB)
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(portlist, addresscombobox.get(), portnumcombobox.get()))
        input_txt = fn.txt2column(parsedoc.obtaininoutfromaddr(portlist, addresscombobox.get(), inputoutputcombobox.get(), portnumcombobox.get()))
        formatted_txt = fn.formattxt(input_txt, 1, True)
        # Print to the output text box
        out_textbox = self.builder.get_object(bitsTXT)
        out_textbox.delete(1.0, tk.END)
        out_textbox.insert(tk.END, formatted_txt)
        ## Add to the Line and Bit count
        nlines, nbits = fn.ObtainNLines(input_txt)
        # Print to nline TB
        nlines_textbox = self.builder.get_object('file1nlines_text')
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nlines)
        # Print to nbit TB
        nlines_textbox = self.builder.get_object('file1nbits_text')
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nbits)
        # clear comparison
        outputtxtbox = self.builder.get_object('bitcompare_textbox')
        outputtxtbox.delete(1.0, tk.END)
    
    def file1loadaddresscallback(self, *args):
        self.clearallfields(addressCB='file1address_combobox', inoutCB='file1inout_combobox', textbox='file1bits_text', portinfoMSG='file1portdata_message')
        self.loadaddresscallback(self.port_list[1],'file1address_combobox','file1port_combobox')

    def file2openfilecallback(self, *args):
        # callback for the file 2 open file
        filenameMSG = 'file2name_input'
        fileaddressCB = 'file2address_combobox'
        inoutCB = 'file2inout_combobox'
        portdataMSG = 'file2portdata_message'
        bitsTXT = 'file2bits_text'
        portnumCB = 'file2port_combobox'
        self.port_list[2] = self.portlistfile(filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT, portnumCB)

    def file2loadbitscallback(self, *args):
        # callback for the file 2 load bits
        fileaddressCB = 'file2address_combobox'
        inoutCB = 'file2inout_combobox'
        portdataMSG = 'file2portdata_message'
        bitsTXT = 'file2bits_text'
        portnumCB = 'file2port_combobox'
        portlist = self.port_list[2]
        addresscombobox = self.builder.get_object(fileaddressCB)
        inputoutputcombobox = self.builder.get_object(inoutCB)
        portinfomessage = self.builder.get_object(portdataMSG)
        portnumcombobox = self.builder.get_object(portnumCB)
        # write to the port info box
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(portlist, addresscombobox.get(), portnumcombobox.get()))
        input_txt = fn.txt2column(parsedoc.obtaininoutfromaddr(portlist, addresscombobox.get(), inputoutputcombobox.get(), portnumcombobox.get()))
        # format the bits with 1 column, commas removed
        formatted_txt = fn.formattxt(input_txt, 1, True)
        # Print to the output text box
        out_textbox = self.builder.get_object(bitsTXT)
        out_textbox.delete(1.0, tk.END)
        out_textbox.insert(tk.END, formatted_txt)
        # Add to the Line and Bit count
        nlines, nbits = fn.ObtainNLines(input_txt)
        # Print to nline TB
        nlines_textbox = self.builder.get_object('file2nlines_text')
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nlines)
        # Print to nbit TB
        nlines_textbox = self.builder.get_object('file2nbits_text')
        nlines_textbox.delete(1.0, tk.END)
        nlines_textbox.insert(tk.END, nbits)
        # clear comparison
        outputtxtbox = self.builder.get_object('bitcompare_textbox')
        outputtxtbox.delete(1.0, tk.END)

    def file2loadaddresscallback(self, *args):
        self.clearallfields(addressCB='file2address_combobox', inoutCB='file2inout_combobox', textbox='file2bits_text', portinfoMSG='file2portdata_message')
        self.loadaddresscallback(self.port_list[2],'file2address_combobox','file2port_combobox')

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