#13A_plate.py
#import typing
from typing import NamedTuple
from epics import caget, caput
from time import sleep

class Point(NamedTuple):
    x: float
    y: float

class Plate:
    # well_list is a dictionary with key as the plate id i.e. A1
    def __init__(self,name=None,temperature=15,well_list=None,filename=None):
        
        self.name = name
        self.temperature = temperature
        self.filename = filename
        if well_list is None:
            self.well_list = {}
        else:
            self.well_list = well_list
        

    #def add_well(self,well):
    #    self.well_list[well.id] = well

    def remove_well(self,well):
        del self.well_list[well.ident]

    def save(self,filename):
        write_string = []
        for attr, value in self.__dict__.items():
            if attr != "well_list":
                print("plate", attr, value)
                write_string.append('plate '+ attr + ' ' + str(value))
            elif attr == "well_list":
                for key, value2  in self.well_list.items():
                    print(key)
                    write_string.append(key)
                    for attr3, value3 in self.well_list[key].__dict__.items():
                        print("well", key, attr3, value3)
                        write_string.append("well " + key + ' ' + attr3 + ' ' + str(value3))
            
        with open(self.filename,'w') as convert_file:
            for line in write_string:
                convert_file.write(line + '\n')
        convert_file.close()

    def read(self,filename):
        #self.plate = Plate() # create new plate ob
        with open(filename, 'r') as f:
            lines = f.readlines()
        f.close()

        for line in lines:
            words = line.split()  

            if len(line.split()) == 1: # make new well object
                self.well_list[words[0]] = Plate.Well()
                print("made well ident is ", words[:])
            elif len(line.split()) > 1:     
                if words[0] == 'plate':
                    attr = words[1]
                    val = words[2]    
                    if attr == 'name':
                        self.name = val
                    elif attr == 'temperature':
                        self.temperature = float(val)
                    elif attr == 'filename':
                        self.filename = val    
                    print(self.name, self.temperature, self.filename)
                elif words[0] == 'well':
                    if words[2] == 'ident':
                        self.well_list[words[1]].ident = words[3]
                    if words[2] == 'is_background':     
                        self.well_list[words[1]].is_background = words[3]
                    if words[2] == 'run_order':     
                        self.well_list[words[1]].run_order = words[3]
                    if words[2] == 'smp_name':     
                        self.well_list[words[1]].smp_name = words[3]

    class Well:
        def __init__(self,ident=None,is_background=None,run_order=None,smp_name='none'):
            #**kwargs
            self.ident = ident
            self.is_background = is_background
            self.run_order = run_order
            self.smp_name = smp_name
            self.well_space = 9

class AutoLoader():
    def __init__(
        self, 
        A1_pos = (0.0,0.0), 
        wash_pos = (-32.5,-38.9), 
        z_top = 0.0, 
        z_bottom = 0.0
        ):
        
        self.A1_pos = A1_pos
        self.wash_pos = wash_pos
        self.z_top = z_top
        self.z_bottom = z_bottom
    
    def get_xpos(self):
        return caget("13a:AutoSMP:X.VAL")

    def get_ypos(self):
        return caget("13a:AutoSMP:Y.VAL")
    
    def get_zpos(self):
        return caget("13a:AutoSMP:Z.VAL")

    def set_xpos(self,v):
        caput("13a:AutoSMP:X.VAL",v)

    def set_ypos(self, v):
        caput("13a:AutoSMP:Y.VAL",v)
    
    def set_zpos(self, v):
        caput("13a:AutoSMP:Z.VAL",v)

    def well_2_coord(self, ident):
        x  = self.A1_pos[0] + float(ident[1:]) * self.well_space
        y =  self.A1_pos[0] + (ord(ident[0])- 64) * self.well_space # ID must be capital
        return (x,y)

    def check_mv(self,v):
        f"Moving to x={v[0]}, y={v[1]}, z={v[2]}"
        moving = True
        while moving:
            if self.get_xpos == v[0] and \
                self.get_xpos == v[1] and \
                self.get_xpos == v[2]:
                moving=False
                f"Finished moving to x={v[0]}, y={v[1]}, z={v[2]}"
                return
            sleep(0.3)
            f"Current position: x={self.get_xpos}, y={self.get_xpos}, z={self.get_xpos}.\r"
                
    def mv_2_well(self, ident):
        pos = self.well_2_coord(ident)
        self.set_zpos(self.z_top) # set Z up
        self.check_mv((self.get_xpos, self.get_ypos, self.z_top)) 
        
        self.set_xpos(pos[0]) # move x
        self.check_mv((pos[0], self.get_ypos, self.z_top)) 
        
        self.set_ypos(pos[1]) # move y
        self.check_mv((pos[0], pos[1], self.z_top)) 
        
        self.set_zpos(self.z_top) # set Z down 
        self.check_mv((pos[0], pos[1], self.z_down)) 

def mv_2_wash(self):

        self.set_zpos(self.z_top) # set Z up
        self.check_mv((self.get_xpos, self.get_ypos, self.z_top)) 
        
        self.set_xpos(self.wash_pos[0]) # move x
        self.check_mv((self.wash_pos[0], self.get_ypos, self.z_top)) 
        
        self.set_ypos(self.wash_pos[1]) # move y
        self.check_mv((self.wash_pos[0], self.wash_pos[1], self.z_top)) 
        
        self.set_zpos(self.z_top) # set Z down 
        self.check_mv((self.wash_pos[0], self.wash_pos[1], self.z_down)) 
    

