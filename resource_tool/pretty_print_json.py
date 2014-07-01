# -*- coding: utf-8 -*-
import json
import sys


if __name__ == '__main__':
    filename = sys.argv[1]
    w = open('tmp', 'w')
    w.write(open(filename, 'r').read())
    w.close()
    jj = json.load(open(filename, 'r'))
    s = json.dumps(jj, indent=4, sort_keys=True, ensure_ascii=False)
    with open(filename, "w") as w:
        w.write(s.encode('utf-8'))
