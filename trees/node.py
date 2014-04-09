# -*- coding: utf-8 -*-


class Node(list):

    def __init__(self, line, parser=None, isroot=False):
        list.__init__(self)
        if type(line) == list:
            for l in line:
                self.append(l)
        if parser is None:
            self.dependance = None
            self.subject = None
            self.funcword = None
            if isroot:
                self.append(Word(line="ROOT"))
        else:
            if type(line) != unicode:
                line = unicode(line, "UTF-8")
            node_info = parser(line)
            self.dependance = node_info['dependance']
            self.subject = node_info['subject']
            self.funcword = node_info['funcword']

    def get_surface(self):
        return "".join([w.get_string() for w in self])


class Word(object):

    def __init__(self, line=None, parser=None):
        if type(line) != unicode:
            line = unicode(line, "UTF-8")
        if parser is None:
            self.string = None
            self.ne = None
            self.pos = None
            self.subpos = None
            self.pas = None
        else:
            word_info = parser(line)
            self.string = word_info['string']
            self.ne = word_info['ne']
            self.pos = word_info['pos']
            self.subpos = word_info['subpos']
            self.pas = word_info['pas']

    def get_string(self):
        if self.string is not None:
            return self.string
        return ""

if __name__ == '__main__':
    pass
