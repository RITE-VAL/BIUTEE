# -*- coding: utf-8 -*-
import sys
import shlex
import CaboCha

import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE

CHAPS_PATH = "/home/mai-om/local/dist/chapas-0.742"
CHAPS_CMD = "java -jar {path}/chapas.jar -I RAW".format(path=CHAPS_PATH)


def cabocha(sentence):
    c = CaboCha.Parser("-n 1")
    return c.parse().toString(CaboCha.FORMAT_LATTICE)


def chapas(sentence, cmd=CHAPS_CMD):
    p2 = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE)
    out, err = p2.communicate(input=sentence)
    return out.rstrip()


def mywrite(text, f=sys.stdout, encoding='utf-8'):
    if isinstance(text, unicode):
        text = text.encode(encoding)
    f.write("{}\n".format(text))
    f.flush()


def make_pas(args):
    writer = open(args.target_file + '.pas', 'w')
    tree = ET.parse(args.target_file)
    root = tree.getroot()
    for pair in root:
        now_id = pair.attrib.get('id')
        ans = pair.attrib.get('label')
        cate = pair.attrib.get('category')
        text = u""
        for p in pair:
            text += u"# id:{}".format(now_id)
            if ans:
                text += u" label:{}".format(ans)
            if cate:
                text += u" category:{}".format(cate)
            text += " tag:{}\n".format(p.tag)
            text += chapas(p.text.encode("UTF-8")).decode("UTF-8") + u"\n"
        mywrite(text, f=writer)
    writer.close()


def make_raw(args):
    writer = open(args.target_file + '.raw', 'w')
    tree = ET.parse(args.target_file)
    root = tree.getroot()
    for pair in root:
        now_id = pair.attrib.get('id')
        ans = pair.attrib.get('label')
        cate = pair.attrib.get('category')
        text = u"{}\t{}".format(now_id, pair[0].text)
        if len(pair) > 1:
            text += u"\t{}".format(pair[1].text)
        if ans:
            text += u"\t{}".format(ans)
        if cate:
            text += u"\t{}".format(cate)
        mywrite(text, f=writer)
    writer.close()


def type_selector(string):
    try:
        return {
            "pas": make_pas, "raw": make_raw
        }[string]
    except:
        return string


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('target_file', metavar='FILE',
                        help='result file %(default)s')
    parser.add_argument('-t', '--type', dest='parse_type', metavar='TYPE',
                        help='select parse type %(default)s',
                        choices=[make_raw, make_pas],
                        type=type_selector,
                        default="raw")
    args = parser.parse_args()
    args.parse_type(args)


if __name__ == '__main__':
    main()
