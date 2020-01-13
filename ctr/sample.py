import random
import numpy as np



file_path="/home/lili/data/train.txt"
percentage = 0.1
with open(file_path, "r") as file:
    line_count=0
    for line in file:
        line=line.strip()
        line_count+=1
        if line_count % 1000000 == 0:
            print("progress {}".format(line_count))

print("total {}".format(line_count))

valid_count=int(line_count*percentage)
print("valid_count {}".format(valid_count))

idx=np.arange(line_count)
random.shuffle(idx)
idx=set(idx[:valid_count])
print("idx size: {}".format(len(idx)))

train_file="/home/lili/data/ctr-train.txt"
dev_file="/home/lili/data/ctr-dev.txt"
with open(file_path, "r") as file,\
    open(train_file, "w") as t_f, \
    open(dev_file, "w") as d_f:


    line_count=0
    for line in file:
        if int(line_count) in idx:
            d_f.write(line)
        else:
            t_f.write(line)
        line_count+=1
