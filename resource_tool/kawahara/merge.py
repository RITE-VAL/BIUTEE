# -*- coding: utf-8 -*-
import json
from collections import Counter


def merge():
    files = ["tsubame{:02d}.kototoi.org/".format(n) for n in range(0, 15)]
    vocab = set([])
    count = Counter()
    for d in files:
        with open(d + "all.freq") as f:
            for line in f:
                w, c = tuple(line.rstrip().split("\t"))
                count[w] += int(c)
        with open(d + "all.vocab") as f:
            for line in f:
                vocab.add(line.rstrip())
    with open("all_freq.json", "w") as v:
        v.write(
            json.dumps(count, separators=(',', ':'))
        )
    with open("all.vocab.json", "w") as v:
        v.write(
            json.dumps(list(vocab), separators=(',', ':'))
        )


if __name__ == '__main__':
    merge()
