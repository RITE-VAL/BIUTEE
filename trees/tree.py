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

    def search_word(self, word):
        '''
        tree中のNodeの中からwordが含まれるNodeのpositionを返します
        なければNoneを返します
        '''
        for node_pos, node in self.items():
            if node.get_subject().string == word:
                return node_pos
        return None

    def insert_node(self, newnode, position=None):
        '''
        newnode : 新しく挿入したいノード
        position : newnodeの親ノードのposition(int)
        '''
        if position is None:
            position = self.last_position + 1
        self[position] = newnode
        newnode.position = position
        if newnode.parent == -1:
            self.set_root(position)
        else:
            if not newnode.parent in self:
                raise NotFoundNodePositionError(newnode.parent)
            self[newnode.parent].add_child(position)
        self.last_position = max(self.last_position, position)

    def delete_node(self, node_pos):
        '''
        node_pos を Tree から消します
        親ノードからnode_posに関する情報も消します
        node_pos: 消したいノードのposision
        '''
        if not node_pos in self:
            raise NotFoundNodePositionError(node_pos)
        node = self[node_pos]
        del self[node_pos]
        self[node.parent].remove_child(node_pos)

    def move_subtree(self, node_pos, after_parent_pos):
        '''
        node_posにあるノードをafter_parent_posのノード配下に置きます
        node_pos : 移動させたいノードの位置(int)
        after_parent_pos : 移動させたいノードの移動先ノードの位置(int)
        '''
        if not node_pos in self:
            raise NotFoundNodePositionError(node_pos)
        if not after_parent_pos in self:
            raise NotFoundNodePositionError(after_parent_pos)
        self[self[node_pos].parent].remove_child(node_pos)
        self[node_pos].parent = after_parent_pos
        self[after_parent_pos].add_child(node_pos)

    def change_relation(self, node_pos, relation):
        '''
        ノードself[node_pos]と親ノードとの関係をrelationに変更します
        ない場合はNotFoundRelationErrorをなげます
        '''
        if not node_pos in self:
            raise NotFoundNodePositionError(node_pos)
        parent = self[node_pos].parent
        if node_pos in self[parent].rel:
            raise NotFoundRelationError(node_pos, parent, relation)
        self[parent].rel[node_pos] = relation

    def flip_part_of_speech(self, node_position, after_POS):
        '''
        ノードnode_position中のWordの品詞を品詞after_POSに変えます
        変える単語は主辞(位置はsubject)の品詞です
        '''
        if not node_position in self:
            raise NotFoundNodePositionError(node_position)
        subject_pos = self[node_position].subject
        self[node_position][subject_pos].pos = after_POS

    def cut_multiword(self, node_pos, removed_word_pos):
        '''
        ノードnode_posのremoved_word_posの位置にあるWordを除きます
        Node(安全 運転 で) -> Node(運転 で) のようにします
        node_pos: 語を除きたいNodeの位置
        removed_word_pos: Node中で除きたい語の位置
                          上記なら安全は0番目にあるので 0 を指定
        返り値として 除いた Word object (上の例なら Word(安全)) が返ってきます
        '''
        if not node_pos in self:
            raise NotFoundNodePositionError(node_pos)
        return self[node_pos].remove_word(removed_word_pos)

    def singleword_to_multiword(self, node_pos, word, word_pos):
        '''
        ノードnode_posにwordを追加してマルチワードにします
        node_pos : 結合させたいノードの位置(int)
        word     : 追加したい語 (Word class)
        word_pos : node_posの中で追加したい位置
        '''
        if not node_pos in self:
            raise NotFoundNodePositionError(node_pos)
        return self[node_pos].insert_word(word_pos, word)

if __name__ == '__main__':
    tree = Tree()
    tree.append(node.Node([]))
    tree.append(node.Node([]))
    print tree
