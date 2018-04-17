# coding=utf-8

def get_height(node):
    return node.height if node else -1


def tree_minimum(node):
    temp_node = node
    while temp_node.left:
        temp_node = temp_node.left
    return temp_node


def tree_maximum(node):
    temp_node = node
    while temp_node.right:
        temp_node = temp_node.right
    return temp_node


def left_left_rotate(node):
    """
    AVL树的左左 其实跟红黑树的右旋没有区别 左左是两个节点均在左侧
    最后一行的赋值是保证旋转的父节点的指针指向正确(虽然不知道有没有用 但是先试试吧)
    :param node: 将要执行左左旋转的节点
    :return: 左子节点
    """
    node_left = node.left
    node.left = node_left.right
    node_left.right = node
    node.height = max(get_height(node.left), get_height(node.right)) + 1
    node_left.height = max(get_height(node_left.left), get_height(node_left.right)) + 1
    return node_left


def right_right_rotate(node):
    """
    AVL树的右右 其实跟红黑树的左旋没有区别 右右是两个节点均在右侧
    :param node: 将要执行右右旋转的节点
    :return: 右子节点
    """
    node_right = node.right
    node.right = node_right.left
    node_right.left = node
    node.height = max(get_height(node.left), get_height(node.right)) + 1
    node_right.height = max(get_height(node_right.left), get_height(node_right.right)) + 1
    return node_right


def left_right_rotate(node):
    """
    AVL树的左右 -> 先左旋再右旋(红黑树) -> 右右然后左左(AVL树)
    :param node: 出现高度异常的最高节点
    :return: None
    """
    node.left = right_right_rotate(node.left)
    return left_left_rotate(node)


def right_left_rotate(node):
    node.right = left_left_rotate(node.right)
    return right_right_rotate(node)


def preorder_tree_walk(node):
    if node:
        print(node.key)
        preorder_tree_walk(node.left)
        preorder_tree_walk(node.right)


class AVLTreeNode(object):
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key
        self.height = 0


class AVLTree(object):
    def __init__(self):
        self.root = None

    def find(self, key):
        if not self.root:
            return None
        else:
            return self._find(key)

    def _find(self, key):
        start = self.root
        while start:
            if key == start.key:
                return start
            elif key > start.key:
                start = start.right
            elif key < start.key:
                start = start.left
        return None

    def insert(self, node):
        if not self.root:
            self.root = node
        else:
            self.root = self._insert(self.root, node)

    def _insert(self, index, node):
        """
        AVL树插入操作的递归实现
        :param index: root
        :param node: 待插入节点
        :return: root
        """
        if not index:
            index = node
        elif node.key < index.key:
            index.left = self._insert(index.left, node)
            if get_height(index.left) - get_height(index.right) == 2:
                if node.key < index.left.key:
                    index = left_left_rotate(index)
                else:
                    index = left_right_rotate(index)
        elif node.key > index.key:
            index.right = self._insert(index.right, node)
            if get_height(index.right) - get_height(index.left) == 2:
                if node.key < index.right.key:
                    index = right_left_rotate(index)
                else:
                    index = right_right_rotate(index)
        index.height = max(get_height(index.left), get_height(index.right)) + 1
        return index

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, index, key):
        if not index:
            print("Error, key not in the tree")
            return
        elif key < index.key:
            index.left = self._delete(index.left, key)
            if get_height(index.right) - get_height(index.left) == 2:
                if get_height(index.right.right) > get_height(index.right.left):
                    index = right_right_rotate(index)
                else:
                    index = right_left_rotate(index)
            index.height = max(get_height(index.left), get_height(index.right))
        elif key > index.key:
            index.right = self._delete(index.right, key)
            if get_height(index.left) - get_height(index.right) == 2:
                if get_height(index.left.left) > get_height(index.left.right):
                    index = left_left_rotate(index)
                else:
                    index = left_right_rotate(index)
            index.height = max(get_height(index.left), get_height(index.right))
        elif index.left and index.right:
            if index.left.height <= index.right.height:
                node_min = tree_minimum(index.right)
                index.key = node_min.key
                index.right = self._delete(index.right, index.key)
            else:
                node_max = tree_maximum(index.left)
                index.key = node_max.key
                index.left = self._delete(index.left, index.key)
            index.height = max(get_height(index.left), get_height(index.right)) + 1
        else:
            if index.right:
                index = index.right
            else:
                index = index.left
        return index


def main():
    number_list = (7, 4, 1, 8, 5, 2, 9, 6, 3)
    tree = AVLTree()
    for number in number_list:
        node = AVLTreeNode(number)
        tree.insert(node)
    preorder_tree_walk(tree.root)
    tree.delete(4)
    print('==========')
    preorder_tree_walk(tree.root)


if __name__ == '__main__':
    main()