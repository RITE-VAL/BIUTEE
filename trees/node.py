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

    def insert_word(self, pos, word):
        self.words.insert(pos, word)
        return self.words

    def remove_word(self, word_pos):
        return self.words.pop(word_pos)

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
           string(必須): 文字列の表層
           pos         : 品詞，例えばCabocha Formatの1つ目の項目(e.g. 名詞，動詞)
           subpos      : サブの品詞 例えばCabocha Formatの2つ目の項目(e.g. サ変接続，自立)
           ne          : 固有名詞
           pas         : 述語項構造解析の結果 (e.g. ga="1" ni="2")
        '''
        self.string = None
        self.ne = None
        self.pos = None
        self.subpos = None
        self.pas = None
        if len(args) > 0:
            word_info = args[0]
            self.string = word_info['string']
            if 'pos' in word_info:
                self.pos = word_info['pos']
            if 'subpos' in word_info:
                self.subpos = word_info['subpos']
            if 'ne' in word_info:
                self.ne = word_info['ne']
            if 'pas' in word_info:
                self.pas = word_info['pas']

    def get_string(self):
        if self.string is not None:
            return self.string
        return u""

if __name__ == '__main__':
    pass
