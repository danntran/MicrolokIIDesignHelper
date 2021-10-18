import fn_callback as fn
import parse_document as parsedoc

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
        # needed for the callback for combobox
        for CBs in ['file1inout_combobox','file1address_combobox']:
            Cbbox = self.builder.get_object(CBs)
            Cbbox.bind("<<ComboboxSelected>>", self.file1loadbitsCB)
        for CBs in ['file2inout_combobox','file2address_combobox']:
            Cbbox = self.builder.get_object(CBs)
            Cbbox.bind("<<ComboboxSelected>>", self.file2loadbitsCB)
    
    def portlistfile(self, filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT):
        # gets theport info for a given file 
        file_types = (
            ('Microlok II/Genisys II Files', ['*.ml2','*.gn2']),
            ('All files', '*.*'))
        try:
            # TO DO: Need to add error check for correct file
            openfile_text = filedialog.askopenfile(title='Open a file', filetypes=file_types).read().splitlines()
        except: # opening file failed
            openfile_text = ''
            portlist = ''
        if openfile_text:
            filenameinput = self.builder.get_object(filenameMSG)
            addresscombobox = self.builder.get_object(fileaddressCB)
            # clear the fields
            self.clearallfields(fileaddressCB,inoutCB,portdataMSG,bitsTXT)
            # get the file name
            filenameinput.configure(text=parsedoc.getfilename(openfile_text))
            portlist = parsedoc.obtcomminfo(parsedoc.rm_commnewlinesfromtext(openfile_text))
            addresscombobox['values'] = parsedoc.returnaddresslist(portlist)
        return portlist

    def open_about_toplevel(self, *args):
        # Open About window
        builder2 = pygubu.Builder()
        builder2.add_resource_path(PROJECT_PATH)
        builder2.add_from_file(PROJECT_UI)
        builder2.get_object('about_toplevel')

    def bitformat_convertCB(self, *args):
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

    def bitformat_openfileCB(self, *args):
        # call back for bit formatter, open file
        filenameMSG = 'filenameinput'
        fileaddressCB = 'addresscombobox'
        inoutCB = 'inputoutputcombobox'
        portdataMSG = 'portinfomessage'
        bitsTXT = 'InputTextBox'
        self.port_list[0] = self.portlistfile(filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT)
    
    def bitformat_loadCB(self, *args):
        # call back for bit formatter, load bit
        addresscombobox = self.builder.get_object('addresscombobox')
        inputoutputcombobox = self.builder.get_object('inputoutputcombobox')
        portinfomessage = self.builder.get_object('portinfomessage')
        in_textbox = self.builder.get_object('InputTextBox')
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(self.port_list[0], addresscombobox.get()))
        in_textbox.delete(1.0, tk.END)
        in_textbox.insert(tk.END, parsedoc.obtaininoutfromaddr(self.port_list[0], addresscombobox.get(), inputoutputcombobox.get()))
        
    def clearallfields(self, addressCB='', inoutCB='', portinfoMSG='', textbox=''):
        # clear the fields, addressCB, inputoutputCB, port information msg, input textbox
        addresscombobox = self.builder.get_object(addressCB)
        inoutcombobox = self.builder.get_object(inoutCB)
        portinfomsg = self.builder.get_object(portinfoMSG)
        inputtextbox = self.builder.get_object(textbox)
        addresscombobox.set("")
        inoutcombobox.set("")
        portinfomsg.configure(text="")
        inputtextbox.delete(1.0, tk.END)

    def file1openfileCB(self, *args):
        # callback for the file 1 open file
        filenameMSG = 'file1name_input'
        fileaddressCB = 'file1address_combobox'
        inoutCB = 'file1inout_combobox'
        portdataMSG = 'file1portdata_message'
        bitsTXT = 'file1bits_text'
        self.port_list[1] = self.portlistfile(filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT)

    def file1loadbitsCB(self, *args):
        # callback for the file 1 load bits
        fileaddressCB = 'file1address_combobox'
        inoutCB = 'file1inout_combobox'
        portdataMSG = 'file1portdata_message'
        bitsTXT = 'file1bits_text'
        portlist = self.port_list[1]
        addresscombobox = self.builder.get_object(fileaddressCB)
        inputoutputcombobox = self.builder.get_object(inoutCB)
        portinfomessage = self.builder.get_object(portdataMSG)
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(portlist, addresscombobox.get()))
        input_txt = fn.txt2column(parsedoc.obtaininoutfromaddr(portlist, addresscombobox.get(),inputoutputcombobox.get()))
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

    def file2openfileCB(self, *args):
        # callback for the file 2 open file
        filenameMSG = 'file2name_input'
        fileaddressCB = 'file2address_combobox'
        inoutCB = 'file2inout_combobox'
        portdataMSG = 'file2portdata_message'
        bitsTXT = 'file2bits_text'

        self.port_list[2] = self.portlistfile(filenameMSG, fileaddressCB, inoutCB, portdataMSG, bitsTXT)

    def file2loadbitsCB(self, *args):
        # callback for the file 2 load bits
        fileaddressCB = 'file2address_combobox'
        inoutCB = 'file2inout_combobox'
        portdataMSG = 'file2portdata_message'
        bitsTXT = 'file2bits_text'
        portlist = self.port_list[2]
        addresscombobox = self.builder.get_object(fileaddressCB)
        inputoutputcombobox = self.builder.get_object(inoutCB)
        portinfomessage = self.builder.get_object(portdataMSG)
        # write to the port info box
        portinfomessage.configure(text=parsedoc.obtainportinfofromaddr(portlist, addresscombobox.get()))
        input_txt = fn.txt2column(parsedoc.obtaininoutfromaddr(portlist, addresscombobox.get(),inputoutputcombobox.get()))
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

    def comparebitsCB(self, *args):
        # call back for the compare button
        bits1_textbox = self.builder.get_object('file1bits_text')
        bits2_textbox = self.builder.get_object('file2bits_text')
        [nerrors, compare_resultstr] = fn.comparebits(bits1_textbox.get(1.0, tk.END), bits2_textbox.get(1.0, tk.END))
        compare_textbox = self.builder.get_object('bitcompare_textbox')
        compare_textbox.delete(1.0, tk.END)
        compare_textbox.insert(tk.END, ('NUMBER OF ERRORS: ' + str(nerrors) + '\n'))
        compare_textbox.insert(tk.END, compare_resultstr)

    def run(self):
        self.mainwindow.mainloop()

# main
if __name__ == '__main__':
    app = MicrolokiidesignhelperguiApp()
    app.run()