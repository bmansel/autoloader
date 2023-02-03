#13A_plate.py
import json
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
        del self.well_list[well.id]

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
                print("made well id is ", words[:])
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
                    if words[2] == 'id':
                        self.well_list[words[1]].id = words[3]
                    if words[2] == 'is_background':     
                        self.well_list[words[1]].is_background = words[3]
                    if words[2] == 'run_order':     
                        self.well_list[words[1]].run_order = words[3]
                    if words[2] == 'smp_name':     
                        self.well_list[words[1]].smp_name = words[3]

    class Well:
        def __init__(self,id=None,is_background=None,run_order=None,smp_name='none'):
            #**kwargs
            self.id = id
            self.is_background = is_background
            self.run_order = run_order
            self.smp_name = smp_name
