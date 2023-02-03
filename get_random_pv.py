from epics import caget, caput, cainfo
from time import sleep
CA = "temperature:water"
i = 0
while True:
    print(caget(CA,i))
    i += 1
    sleep(1)
