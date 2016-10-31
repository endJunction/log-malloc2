#!/bin/env python

import fileinput
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.DataFrame(columns=["Address", "Size", "Time", "LiveSpan"])

sizes = []
times = []
alloc_table = dict()
free_wo_alloc = []
for line in fileinput.input():
    split_line = line.split()
    op = split_line[0]
    size = int(split_line[1])
    if op == 'malloc' or op == 'calloc':
        addr = int(split_line[2], 16)
        sizes.append(size)
        if addr in alloc_table:
            print("Double allocation at", hex(addr))
            raise "DoubleAlloc"
        time = float(split_line[3])
        alloc_table[addr] = time
    if op == 'realloc' and split_line[2] == '(nil)':
        addr = int(split_line[3], 16)
        sizes.append(size)
        if addr in alloc_table:
            print("Double allocation at", hex(addr))
            raise "DoubleAlloc"
        alloc_table[addr] = time
    if op == 'realloc' and split_line[2] != '(nil)':
        # remove old pointer
        addr = int(split_line[2], 16)
        if addr not in alloc_table:
            free_wo_alloc.append(addr)
            continue
        time = float(split_line[4])
        times.append(time - alloc_table[addr])
        del alloc_table[addr]

        # add reallocated pointer
        addr = int(split_line[3], 16)
        sizes.append(size)
        if addr in alloc_table:
            print("Double allocation at", hex(addr))
            raise "DoubleAlloc"
        alloc_table[addr] = time

    if op == 'free':
        addr = int(split_line[2], 16)
        if addr not in alloc_table:
            free_wo_alloc.append(addr)
            continue
        time = float(split_line[3])
        times.append(time - alloc_table[addr])
        del alloc_table[addr]
fileinput.close()

print("Histogram of allocated sizes:")
maximum_size = max(sizes)
max_pow = 0;
while (maximum_size >> max_pow) != 1:
    max_pow+=1
print(np.histogram(sizes, bins=[2**i for i in np.arange(0, max_pow)]))

print("Histogram of live spans:")
print(np.histogram(times, bins=100))

print("Remaining allocations:")
print(alloc_table)

print("Frees w/o allocations:")
print(free_wo_alloc)
