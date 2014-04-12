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


class NotFoundNodePositionError(Exception):

    def __init__(self, node_pos):
        self.node_pos = node_pos

    def __str__(self):
        return repr("Not Found Position {} in the tree".format(
            self.node_pos
        ))


class Tree(dict):
    '''
    Tree(dict)
    root_pos: ルートノードのposition
    last_position: Tree中最大の数となるposition
    '''

    def __init__(self):
        dict.__init__(self)
        self.root_pos = None
        self.last_position = 0

    def __len__(self):
        return len(self.keys())

    def set_root(self, node_pos):
        self.root_pos = node_pos

    def get_node(self, position):
        if position in self:
            return self[position]
        raise NotFoundNodePositionError(position)

    def insert_node(self, newnode, position=None):
        '''
        newnode : 新しく挿入したいノード
        position : newnodeの親ノードのposition(int)
        '''
        if position is None:
            position = self.last_position + 1
        self[position] = newnode
        newnode.position = position
        if newnode.dependent == -1:
            self.set_root(position)
        else:
            self[newnode.dependent].add_child(position)
        self.last_position = max(self.last_position, position)

    def delete_node(self, node_pos):
        '''
        node_pos を Tree から消します
        親ノードからnode_posに関する情報も消します
        node_pos: 消したいノードのposision
        '''
        node = self[node_pos]
        del self[node_pos]
        self[node.dependent].remove_child(node_pos)

    def move_subtree(self, node_pos, after_parent_pos):
        '''
        node_posにあるノードをafter_parent_posのノード配下に置きます
        node_pos : 移動させたいノードの位置(int)
        after_parent_pos : 移動させたいノードの移動先ノードの位置(int)
        '''
        self[self[node_pos].dependent].remove_child(node_pos)
        self[node_pos].depenent = after_parent_pos
        self[after_parent_pos].add_child(node_pos)

    def change_relation(self, node_pos, relation):
        '''
        ノードself[node_pos]と親ノードとの関係をrelationに変更します
        '''
        pass

    def flip_part_of_speech(self, node_pos, word_pos, after_pos):
        '''
        ノードnode_pos中の位置word_posのWordの品詞をafter_posに変えます
        '''
        pass

    def cut_multiword(self, node_pos, removed_word_pos):
        '''
        ノードnode_posをマルチワードとしてremoved_word_posにあるWordを除きます
        '''
        pass

    def singleword_to_multiword(self, node_pos):
        '''
        ノードnode_posとひとつ後のノードを結合してマルチワードにします
        node_pos : 結合させたいノードの位置(int)
        '''
        pass

if __name__ == '__main__':
    tree = Tree()
    tree.append(node.Node([]))
    tree.append(node.Node([]))
    print tree
