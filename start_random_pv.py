from epics import caget, caput, cainfo
from time import sleep
import threading
from time import time

def set_val():
    CA = "temperature:water"
    i = 0   
    while True:
        caput(CA,i)
        i += 1
        sleep(1)

def get_val():
    CA = "13a:AutoSMP.X.VAL"
    i = 0   
    while True:
        print(caget(CA))
        print(time())
        sleep(0.5)


#x = threading.Thread(target=set_val)
#x.start()
y = threading.Thread(target=get_val)
y.start()        

# x.join()
y.join()




