# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import glob
import sys
import os.path

home = os.getenv('HOME')
syncha_path = '{}/local/dist/syncha-0.3/syncha'.format(home)


def getSynchaResult(sentence):
    syncha = Popen(syncha_path.split(' '),
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
    syncha.stdin.write(sentence)
    return syncha.communicate()[0].rstrip()


def main():
    for filename in glob.iglob('[FS]V/my/*.xml.raw'):
        with open(filename.replace('raw', 'syncha'), "w") as writer:
            for line in open(filename, "r"):
                sys.stdout.write(line.rstrip() + "\n")
                sys.stdout.flush()
                line = line.replace(' ', '　')
                items = line.rstrip().split("\t")
                if len(items) == 3:
                    s_id, s1, ans = items
                    writer.write("% ID:{} ans:{}\n".format(s_id, ans))
                    writer.write("% t1\n")
                    output = getSynchaResult(s1)
                    writer.write(output + "\n")
                elif len(items) == 4:
                    s_id, s1, s2, ans = items
                    writer.write("% ID:{} ans:{}\n".format(s_id, ans))
                    writer.write("% t1\n")
                    output = getSynchaResult(s1)
                    writer.write(output + "\n")
                    writer.write("% t2\n")
                    output = getSynchaResult(s2)
                    writer.write(output + "\n")
                else:
                    s_id, s1, s2, ans, c = items
                    writer.write("% ID:{} ans:{} c:{}\n".format(s_id, ans, c))
                    writer.write("% t1\n")
                    output = getSynchaResult(s1)
                    writer.write(output + "\n")
                    writer.write("% t2\n")
                    output = getSynchaResult(s2)
                    writer.write(output + "\n")
                writer.flush()


if __name__ == '__main__':
    main()
