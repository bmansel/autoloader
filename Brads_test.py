
'''Brads_test.py'''

# need to put on a canvas and bind the click position to that of the canvas not the window...



import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import simpledialog
from PIL import Image, ImageTk
import string


#import time
from l3a_plate import Plate # l not 1


class MainWindow(tk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        # self.save_loc
        save_loc = None
        initialized = False
        self.row = None
        self.col = None
        self.well_labels = []
        self.plate = Plate()

        image1 = Image.open("96-well-plate-template-sm.jpeg")
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test)
        label1.image = test
        label1.place(x=0, y=100)



        if initialized is False:
            self.initialize()
            for key in self.plate.well_list:
                print("line 37")
                print("well", key, "has run order", self.plate.well_list[key].run_order)
            
            
            for key in self.plate.well_list:
                self.draw_order_label(self.well_labels,key[0], key[1:])

        self.root.bind("<Button 1>", self.click)

    #def load_plate(self):



    def initialize(self):
        global initialized
        out = mb.askyesnocancel(title="Welcome!", message=''' Welcome to plateMaker, do you want to append to an existing plate file (.plt)?  
        ''')
        if out is True:
            filename = fd.askopenfilename(title='open .plt file', initialdir='~/',
                                          filetypes=(
                                              ('plate file', '*.plt'), ('All files', '*.*')))
            
            self.plate.read(filename) 
            for key in self.plate.well_list:
                print("line 61")
                print("well", key, "has run order", self.plate.well_list[key].run_order)
            
                                         
            # need to make the plate object
        if out is False:
            temperature = simpledialog.askfloat("Enter experiment temperature in Celcius.", "e.g. 15 (can be updated later)",initialvalue=15)
            name = simpledialog.askstring("Enter a name for plate.", "e.g. 20220902_Chen_lysozyme")
            filename = fd.asksaveasfilename(title='Create .plt file',initialdir='~/',
                                          filetypes=(
                                              ('plate file', '*.plt'), ('All files', '*.*')))

            self.plate.name = name
            self.plate.temperature = temperature
            self.plate.filename = filename
        #print(out)
        #plate.save('/home/brad/test_line_56.plt')
        print(self.plate.filename)
        print(type(self.plate))
        #for key in plate.well_list:
        #    print("line 76")
        #    print("well", key, "has run order", plate.well_list[key].run_order)

        # need to finish this off

        #filename = fd.asksaveasfilename(title='open .plt file', initialdir='~/', filetypes=(('plate file','*.plt'),('All files','*.*')))

    def open_window(self):
        window = TopWindow(self)
        # window.grab_set()

    def click(self, event):
        #global x, y
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))
        self.row, self.col = self.check_well_clicked(x, y)
        self.open_window()

    def check_well_clicked(self, x, y):

        # xaxis first
        start = 62
        step = 39
        for i in range(0, 12):
            first_edge = start + step * i
            second_edge = start + step * (i + 1)
            # print(first_edge)
            #print(str(first_edge), " ", str(second_edge))
            if x > first_edge and x < second_edge:
                col = i+1
                #print("The column is ", str(col))
                break
        # y axis second
        rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
        start = 60
        step = 40
        for i in range(0, 8):
            first_edge = start + step * i
            second_edge = start + step * (i + 1)
            # print(first_edge)
            #print(str(first_edge), " ", str(second_edge))
            if y > first_edge and y < second_edge:
                row = rows[i]
                #print("The row is ", row)
                break
        return row, col

    def draw_order_label(self,well_labels, row, col):
        # need to draw label in this class instead
        well_row_loc = {}
        well_col_loc = {}
        start_row = 168
        start_col = 35
        step = 39
        rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for index, val in enumerate(rows): 
            well_row_loc[val] = start_row + step * index

        for i in range(13): 
            well_col_loc[str(i)] = start_col + step * i # starts down 100

        if self.plate.well_list[row + str(col)].is_background == "yes":
            color = "plum1"
        elif self.plate.well_list[row + str(col)].is_background == "no":
            color = "SeaGreen1"
        
        self.well_labels.append(tk.Label(text = str(self.plate.well_list[row + str(col)].run_order), bg=color, font=("TkDefaultFont", 14)))
                
        self.well_labels[-1].place(x=well_col_loc[str(col)], y=well_row_loc[row])
        self.well_labels[-1].bind
        self.update_idletasks()
        


class TopWindow(tk.Toplevel):
    def __init__(self, root, **kwargs):
        super().__init__(root)
        # self.geometry("300x200")
        self.row = root.row
        self.col = root.col
        self.plate = root.plate
        self.root = root
        self.well_labels = root.well_labels
        self.title('Toplevel Window')
        self.str_var_bkg = tk.StringVar(self)
        self.str_var_bkg.set("yes")
        self.str_var_run_order = tk.StringVar(self)
        self.str_var_run_order.set("0")
        self.str_var_smp_name = tk.StringVar(self)

        label_id = tk.Label(self, text="Well ID: " + self.row +
                            str(self.col), font=("TkDefaultFont", 16))
        label_id.pack()
        label_bkg = tk.Label(self, text="Is this a background?")
        label_bkg.pack()
        op_menu_bkg = tk.OptionMenu(self, self.str_var_bkg, "yes", "no")
        op_menu_bkg.pack()
        label_run_order = tk.Label(self, text="Run order number:")
        label_run_order.pack()
        entry_run_order = tk.Entry(self, textvariable=self.str_var_run_order)
        entry_run_order.pack()
        label_smp_name = tk.Label(self, text="Sample Name:")
        label_smp_name.pack()
        entry_smp_name = tk.Entry(self, textvariable=self.str_var_smp_name)
        entry_smp_name.pack()
        btn_save = tk.Button(self, text="Save", command=self.save_well)
        btn_save.pack()
        
        try:
            self.check_well_used()
            # increase run order
            self.str_var_run_order.set( int(self.increase_run_order()) + 1 )    
        except:
            print("no wells yet")



    def check_well_used(self):
        for well in self.plate.well_list:
            if well == self.row + str(self.col):
                print("well is ", well)
                print("row, col is ", self.row + str(self.col))
                self.load_well()
                return

    def increase_run_order(self):
        run_order_list = []
        for well in self.plate.well_list:
            run_order_list.append( int(self.plate.well_list[well].run_order ) )
        print("run order list is ", run_order_list)
        return max(run_order_list)
        

    def load_well(self):
        #self.plate.well_list[self.row + str(self.col)].is_background
        self.str_var_bkg.set( self.plate.well_list[self.row + str(self.col)].is_background )
        print(self.plate.well_list[self.row + str(self.col)].is_background)
        self.str_var_run_order.set( self.plate.well_list[self.row + str(self.col)].run_order )
        self.str_var_smp_name.set( self.plate.well_list[self.row + str(self.col)].smp_name )
        #root.draw_order_label(self.well_labels)
        
        self.update_idletasks()

    def save_well(self):
        print(type(self.plate))
        self.plate.well_list[self.row + str(self.col)] = Plate.Well( 
            id = self.row + str(self.col), is_background= self.str_var_bkg.get(), 
            run_order= self.str_var_run_order.get(), smp_name= self.str_var_smp_name.get())
        self.root.draw_order_label(self.root.well_labels, self.row, self.col)   
        self.plate.save(self.plate.filename)

def main():
    myapp = tk.Tk()
    myapp.geometry("590x528")
    myapp.title("Plate Maker")

    main = MainWindow(myapp)
    myapp.mainloop()


if __name__ == "__main__":
    main()
