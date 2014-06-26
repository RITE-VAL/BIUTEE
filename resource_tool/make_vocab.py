# -*- coding: utf-8 -*-
import sys
from collections import Counter

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "ERROR: ひとつファイル名を入れて下さい"
        exit(1)
    filename = sys.argv[1]
    count = Counter()
    vocab = set([])
    for surface, info in (tuple(line.split("\t")) for line
                          in sys.stdin if len(line.split("\t")) == 2):
        origin = info.split(",")[6]
        count[origin] += 1
        vocab.add(surface)
    f = open(filename.replace(".cab.bz2", "") + ".freq", "w")
    v = open(filename.replace(".cab.bz2", "") + ".vocab", "w")
    for w, c in count.items():
        f.write("{}\t{}\n".format(w, c))
    for w in vocab:
        v.write("{}\n".format(w))
    f.close()
    v.close()
