# -*- coding: utf-8 -*-
import sys
from collections import Counter

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "ERROR: ひとつファイル名を入れて下さい"
        exit(1)
    d = sys.argv[1]
    vocab = set([v.rstrip() for v in open(d + "all.vocab")])
    with open(d + "all.vocab.t", "w") as v:
        for w in vocab:
            v.write("{}\n".format(w))
    count = Counter()
    for line in open(d + "all.freq"):
        w, c = tuple(line.rstrip().split("\t"))
        count[w] += int(c)
    with open(d + "all.freq.t", "w") as v:
        for w, c in count.items():
            v.write("{}\t{}\n".format(w, c))
