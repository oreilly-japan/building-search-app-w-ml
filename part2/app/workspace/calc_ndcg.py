#!/usr/bin/env python

from argparse import ArgumentParser
from sklearn.metrics import ndcg_score


parser = ArgumentParser()
parser.add_argument("-a", "--at", type=int, default=10)
parser.add_argument("input")
args = parser.parse_args()

scores = []
with open(args.input + ".group") as gf, open(args.input) as f:
    for gl in gf:
        group_size = int(gl)
        y_true = []
        for _ in range(group_size):
            label = int(f.readline())
            y_true.append(label)
        while len(y_true) < args.at:  # Padding
            y_true.append(0)
        score = ndcg_score([y_true], [[-i for i in range(len(y_true))]], k=args.at)
        scores.append(score)

print("Average nDCG Score:")
print(sum(scores) / len(scores))
