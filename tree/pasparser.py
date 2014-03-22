# -*- coding: utf-8 -*-

import shlex
import tree
import node
import json
from collections import defaultdict
from subprocess import Popen, PIPE
import sys, os
import ConfigParser

iniPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.ini"))
inifile = ConfigParser.SafeConfigParser()
inifile.read(iniPath)
CHAPS_PATH = unicode(inifile.get(u"path", u"CHAPAS_PATH"))
CHAPS_CMD = "java -jar {path}/chapas.jar -I RAW".format(path=CHAPS_PATH)


def chapas(sentence, cmd=CHAPS_CMD):
    p1 = Popen(shlex.split('echo "' + sentence + '"'), stdout=PIPE)
    p2 = Popen(shlex.split(cmd), stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    out, err = p2.communicate()
    return out.rstrip()


def chunker(datas):
    datas = iter(datas)
    chunk = None
    try:
        while True:
            target = datas.next().rstrip()
            if target == '':
                continue
            elif target.startswith("* "):
                if chunk:
                    yield chunk
                chunk = [target]
            else:
                chunk.append(target)
    except StopIteration:
        yield chunk
        raise StopIteration


def parse_cabocha_header(line):
    inf = defaultdict(lambda: None)
    data = line.rstrip().split(" ")
    inf['dependance'] = int(data[2][:-1])
    n = data[3].split('/')
    inf['subject'] = int(n[0])
    inf['funcword'] = int(n[1])
    return inf


def parse_cabocha_node(line):
    inf = defaultdict(lambda: None)
    data = line.rstrip().split("\t")
    inf['string'] = data[0]
    tmp = data[1].split(',')
    inf['pos'] = tmp[0]
    inf['subpos'] = tmp[1]
    if data[2] == u'O':
        inf['ne'] = None
    else:
        inf['ne'] = data[2]
    if len(data) > 3:
        inf['pas'] = data[3]
    else:
        inf['pas'] = None
    return inf


class PASParser(object):

    def __init__(self, parser=chapas):
        self.parser = parser

    def parse(self, sentences):
        # 解析結果をTreeのリストとして返す
        trees = []
        sentences = self.parser(sentences).split('EOS')[:-1]
        for sentence in sentences:
            tr = tree.Tree()
            for chunk in chunker(sentence.split('\n')):
                nd = node.Node(line=chunk[0], parser=parse_cabocha_header)
                for word in chunk[1:]:
                    nd.append(node.Word(word, parser=parse_cabocha_node))
                tr.append(nd)
            tr.append(node.Node(line="ROOT", parser=None))
            trees.append(tr)
        return trees


if __name__ == '__main__':
    pass
