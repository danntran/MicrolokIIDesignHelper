import fn_callback as fn

# Rebuild code down here
import os
import tkinter as tk
import tkinter.ttk as ttk
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

        self.formatnrows = None
        self.removecomma = None
        self.builder.import_variables(self, ['formatnrows', 'removecomma'])
    
    def open_about_toplevel(self):
        # Open a New top-level
        self.builder2 = pygubu.Builder()
        self.builder2.add_resource_path(PROJECT_PATH)
        self.builder2.add_from_file(PROJECT_UI)
        self.aboutwindow = self.builder2.get_object('about_toplevel')
        self.builder2.connect_callbacks(self)

    def ConvertTextCallback(self):
        ## Format the text
        # Obtain the text from the text box
        self.in_textbox = self.builder.get_object('InputTextBox')
        self.input_txt = fn.rm_commnewlinesfromtext(fn.txt2column(self.in_textbox.get(1.0, tk.END)))
        self.formatted_txt = fn.formattxt(self.input_txt, self.formatnrows.get(), self.removecomma.get())
        # Print to the output text box
        self.out_textbox = self.builder.get_object('OutputTextBox')
        self.out_textbox.delete(1.0, tk.END)
        self.out_textbox.insert(tk.END, self.formatted_txt)

        ## Add to the Line and Bit count
        self.nlines, self.nbits = fn.ObtainNLines(input_text=self.input_txt)
        # Print to nline TB
        self.nlines_textbox = self.builder.get_object('TextNLines')
        self.nlines_textbox.delete(1.0, tk.END)
        self.nlines_textbox.insert(tk.END, self.nlines)
        # Print to nbit TB
        self.nlines_textbox = self.builder.get_object('TextNBits')
        self.nlines_textbox.delete(1.0, tk.END)
        self.nlines_textbox.insert(tk.END, self.nbits)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = MicrolokiidesignhelperguiApp()
    app.run()

