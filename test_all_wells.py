import auto_loader
from time import perf_counter

t1 = perf_counter()
al = auto_loader.AutoLoader()
cols = ["A","B", "C", "D", "E", "F", "G", "H"]
for col in cols:
    for row in range(1,13):
        al.mv_2_well(col+str(row))
        al.mv_2_wash()
        print("current run time is",perf_counter()-t1)
print("total run time was:", perf_counter()-t1)