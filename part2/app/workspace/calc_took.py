#!/usr/bin/env python

from argparse import ArgumentParser
import numpy as np


parser = ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

x = np.loadtxt(args.input)
tooks = x[:, 1]  # 2列目にtook情報を保存している

print("Average Took:")
print(np.average(tooks))
for percent in [50, 95, 99, 99.9]:
    print(f"{percent}percentile Took:")
    print(np.percentile(tooks, percent))
