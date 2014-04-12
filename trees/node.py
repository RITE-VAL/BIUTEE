# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, *args):
        '''
        Node()
          空のNode
        Node(int dependent)
          depenent のみ
        Node(int dependent, list words)
          dependent と Word のリスト
        Node(int dependent, int subject, int fucword)
          dependent, subject, funcword
        '''
        self.words = []
        self.children = set([])
        self.rel = {}
        self.position = None
        if len(args) == 0:
            self.dependent = None
            self.subject = None
            self.funcword = None
        elif len(args) == 1:
            self.dependent = args[0]
            self.subject = None
            self.funcword = None
        elif len(args) == 2:
            self.dependent = args[0]
            self.words = args[1]
            self.subject = None
            self.funcword = None
        else:
            self.dependent = args[0]
            self.subject = args[1]
            self.funcword = args[2]

    def __iter__(self):
        return iter(self.words)

    def __len__(self):
        return len(self.words)

    def __eq__(self, other_node):
        '''
        見出し語(self) == 見出し語(other_node) => True
        '''
        return self.words[self.subject] == other_node.words[self.subject]

    def add_child(self, child):
        self.children.add(child)

    def remove_child(self, child):
        self.children.remove(child)

    def add_word(self, word):
        self.words.append(word)

    def set_relation(self, rel, pos):
        self.rel[pos] = rel

    def get_surface(self):
        return u"".join([w.get_string() for w in self])


class Word(object):

    def __init__(self, *args):
        '''
        Word()
           空のWord
        Word(dict word_info)
           word_info は keyにstring, ne, pos, subpos, pas を持っている
        '''
        if len(args) == 0:
            self.string = None
            self.ne = None
            self.pos = None
            self.subpos = None
            self.pas = None
        else:
            word_info = args[0]
            self.string = word_info['string']
            self.ne = word_info['ne']
            self.pos = word_info['pos']
            self.subpos = word_info['subpos']
            self.pas = word_info['pas']

    def get_string(self):
        if self.string is not None:
            return self.string
        return u""

if __name__ == '__main__':
    pass
