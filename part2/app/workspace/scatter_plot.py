#!/usr/bin/env python

from argparse import ArgumentParser
import numpy as np
from matplotlib import pyplot


parser = ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

x = np.loadtxt(args.input)
hitss, tooks = x[:, 0], x[:, 1]

figure = pyplot.figure()
pyplot.scatter(hitss, tooks)
pyplot.xscale("log")
pyplot.xlabel("hits")
pyplot.xlim(1, 9999)
pyplot.yscale("log")
pyplot.ylabel("took")
pyplot.ylim(1, 100)
figure.savefig(args.output)
