# -*- coding: utf-8 -*-
import node


class NotFoundRelationError(Exception):

    def __init__(self, node_pos, parent_pos):
        self.node_pos = node_pos
        self.parent_pos = parent_pos

    def __str__(self):
        return repr("Not Found Relation between Node {} and Node {}".format(
            self.node_pos, self.parent_pos
        ))


class Tree(list):
    '''
    引数は未確定
    '''
    def __init__(self):
        list.__init__(self, )
        self.relations = {}   # (1, 3) -> subject ?

    def insert_node(self, newnode, parent_position):
        '''
        指定した親(self[parent_position]) の子として newnode を置きます
        newnode : 新しく挿入したいノード(dependanceはparent_positionになる)
        parent_position : newnodeの親ノードのposition(int)
        '''
        newnode.dependance = parent_position
        self.append(newnode)
        self.relations[(parent_position, len(self) - 1)] = None

    def move_subtree(self, node_position, after_parent_position):
        '''
        node_positonにあるノードをafter_parent_positionのノード配下に置きます
        node_postion : 移動させたいノードの位置(int)
        after_parent_position : 移動させたいノードの移動先ノードの位置(int)
        '''
        before_parent_position = self[node_position].dependance
        self[node_position].dependance = after_parent_position
        self.relations[(after_parent_position, node_position)] = None
        del self.relations[(before_parent_position, node_position)]

    def change_relation(self, node_pos, relation):
        '''
        ノードself[node_pos]と親ノードとの関係をrelationに変更します
        '''
        parent_pos = self[node_pos].dependance
        if not (parent_pos, node_pos) in self.relations:
            raise NotFoundRelationError(node_pos, parent_pos)
        self.relations[(parent_pos, node_pos)] = relation

    def flip_part_of_speech(self, node_pos, word_pos, after_pos):
        '''
        ノードnode_pos中の位置word_posのWordの品詞をafter_posに変えます
        '''
        self[node_pos][word_pos] = after_pos

    def cut_multiword(self, node_pos, removed_word_pos):
        '''
        ノードnode_posをマルチワードとしてremoved_word_posにあるWordを除きます
        '''
        self[node_pos].pop(removed_word_pos)

    def singleword_to_multiword(self, node_pos):
        '''
        ノードnode_posとひとつ後のノードを結合してマルチワードにします
        node_pos : 結合させたいノードの位置(int)
        '''
        node = self[node_pos].pop()
        after_node = self[node_pos].pop()
        newnode = node.Node(node + after_node)
        newnode.dependance = node.dependance
        newnode.subject = after_node.subject
        newnode.funcword = after_node.funcword
        self.insert(newnode, node_pos)


if __name__ == '__main__':
    tree = Tree()
    tree.append(node.Node([]))
    tree.append(node.Node([]))
    print tree
