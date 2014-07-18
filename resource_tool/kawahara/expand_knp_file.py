# -*- coding: utf-8 -*-
import sys


def main():
    tmp_string = ""
    with sys.stdin as stdin:
        for line in stdin:
            line = unicode(line.rstrip(), "UTF-8")
            if line.startswith("# "):
                continue
            if line.startswith("+ "):
                continue
            if line.startswith("* "):
                continue
            if line.startswith("- "):
                continue
            if line.startswith("EOS"):
                sys.stdout.write(tmp_string.encode("UTF-8") + "\n")
                tmp_string = ""
                continue
            tmp_string += line.split(' ')[0]
        if tmp_string != "":
            sys.stdout.write(tmp_string.encode("UTF-8") + "\n")


if __name__ == '__main__':
    main()
