# -*- coding: utf-8 -*-
import node


class Tree(list):
    '''
    引数は未確定
    '''
    def __init__(self):
        list.__init__(self, )
        self.relations = {}   # (1, 3) -> subject ?

    def insert_node(self, newnode=None, position=None):
        self.insert(position, newnode)

    def move_subtree(self, node=None, position=None):
        pass

    def change_relation(self, node_position=None, relation=None):
        pass

    def flip_part_of_speech(self):
        pass

    def cut_multiword(self):
        pass

    def singleword_to_multiword(self):
        pass


if __name__ == '__main__':
    tree = Tree()
    tree.append(node.Node())
    tree.append(node.Node())
    print tree
