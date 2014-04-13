# -*- coding: utf-8 -*-

import shlex
import tree
import node
from collections import defaultdict
from subprocess import Popen, PIPE
import os
import ConfigParser


iniPath = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.ini")
)
inifile = ConfigParser.SafeConfigParser()
inifile.read(iniPath)
CHAPS_PATH = unicode(inifile.get(u"path", u"CHAPAS_PATH"))
CHAPS_CMD = "java -jar {path}/chapas.jar -I RAW".format(path=CHAPS_PATH)


def chapas(sentence, cmd=CHAPS_CMD):
    p2 = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE)
    out, err = p2.communicate(input=sentence)
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
    data = unicode(line, "UTF-8").rstrip().split(" ")
    inf['pos'] = int(data[1])
    inf['dependent'] = int(data[2][:-1])
    n = data[3].split('/')
    inf['subject'] = int(n[0])
    inf['funcword'] = int(n[1])
    return inf


def parse_cabocha_node(line):
    inf = defaultdict(lambda: None)
    data = unicode(line, "UTF-8").rstrip().split("\t")
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


splitter = lambda x: [tuple(rel.split("=")) for rel in x.split(' ')]


def setRelationFromPAS(tr):
    word_info = {}
    for pos in sorted(tr):
        for word in tr[pos]:
            if word.pas is not None:
                for k, v in splitter(word.pas):
                    if k == u'ID':
                        word_info[int(v[1:-1])] = tr[pos].position
                    elif k == u'ga' or k == u'o' or k == u'ni':
                        tr[pos].set_relation(k, word_info[int(v[1:-1])])


class PASParser(object):

    def __init__(self, parser=chapas):
        self.parser = parser

    def parse(self, sentences):
        # 解析結果をTreeのリストとして返す
        trees = []
        sentences = self.parser(sentences).split('EOS')[:-1]
        for sentence in sentences:
            tr = tree.Tree()
            for chunk in reversed(list(chunker(sentence.split('\n')))):
                info = parse_cabocha_header(chunk[0])
                nd = node.Node(
                    info['dependent'], info['subject'], info['fucword']
                )
                for word in chunk[1:]:
                    winfo = parse_cabocha_node(word)
                    word = node.Word(winfo)
                    nd.add_word(word)
                tr.insert_node(nd, position=info['pos'])
            setRelationFromPAS(tr)
            trees.append(tr)
        return trees


if __name__ == '__main__':
    pass
