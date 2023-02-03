import tkinter as tk
from tkinter import ttk
import time
from _13a_plate import Plate

start_time = time.time()
well_list = {}
row_list = ["A","B","C","D","E","F","G"]
for i in range(1,12):
    for j in row_list:
        well_list[j+str(i)] = Plate.Well(j+str(i), False, i)
        
        
p1 = Plate("test",25,well_list)

well = Plate.Well("H1",False, 10)
p1.add_well(well)

#for i in range(3):
#    print(p1.well_list[i].id)

#run_order_check = p1.check_order()
#id_check = p1.check_ids()
print(p1.well_list["H1"].is_background)
end_time = time.time()
run_time = end_time - start_time
print("run time is ", str(run_time))
#plate1 = Plate("brad's", 25, wells)