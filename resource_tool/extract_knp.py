# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import glob
import sys
import os.path

home = os.getenv('HOME')
juman_path = '{}/local/bin/juman'.format(home)
knp_path = '{}/local/bin/knp -case -anaphora -tab'.format(home)


def getKNPResult(sentence):
    juman = Popen([juman_path], stdin=PIPE, stdout=PIPE)
    knp = Popen(knp_path.split(' '), stdin=juman.stdout, stdout=PIPE)
    juman.stdin.write(sentence)
    juman.stdin.close()
    juman.stdout.close()
    return knp.communicate()[0].rstrip()


def main():
    for filename in glob.iglob('[FS]V/my/*.xml.raw'):
        with open(filename.replace('raw', 'knp'), "w") as writer:
            for line in open(filename, "r"):
                sys.stdout.write(line.rstrip() + "\n")
                sys.stdout.flush()
                line = line.replace(' ', '　')
                items = line.rstrip().split("\t")
                if len(items) == 3:
                    s_id, s1, ans = items
                    writer.write("% ID:{} ans:{}\n".format(s_id, ans))
                    writer.write("% t1\n")
                    output = getKNPResult(s1)
                    writer.write(output + "\n")
                elif len(items) == 4:
                    s_id, s1, s2, ans = items
                    writer.write("% ID:{} ans:{}\n".format(s_id, ans))
                    writer.write("% t1\n")
                    output = getKNPResult(s1)
                    writer.write(output + "\n")
                    writer.write("% t2\n")
                    output = getKNPResult(s2)
                    writer.write(output + "\n")
                else:
                    s_id, s1, s2, ans, c = items
                    writer.write("% ID:{} ans:{} c:{}\n".format(s_id, ans, c))
                    writer.write("% t1\n")
                    output = getKNPResult(s1)
                    writer.write(output + "\n")
                    writer.write("% t2\n")
                    output = getKNPResult(s2)
                    writer.write(output + "\n")
                writer.flush()


if __name__ == '__main__':
    main()
