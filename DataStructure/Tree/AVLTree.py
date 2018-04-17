from TreeTraverse import *


class AVLNode(object):
    def __init__(self, key):
        self.key = key
        self.height = 0
        self.left = None
        self.right = None


def get_height(root):
    return root.height if root else -1


def get_maximun(root):
    return get_maximun(root.right) if root.right else root


def get_minimun(root):
    return get_minimun(root.left) if root.left else root


def llrotate(root):
    root_new = root.left
    root.left = root_new.right
    root_new.right = root
    root.height = max(get_height(root.left), get_height(root.right)) + 1
    root_new.height = max(get_height(root_new.left), get_height(root_new.right)) + 1
    return root_new


def rrrotate(root):
    root_new = root.right
    root.right = root_new.left
    root_new.left = root
    root.height = max(get_height(root.left), get_height(root.right)) + 1
    root_new.height = max(get_height(root_new.left), get_height(root_new.right)) + 1
    return root_new


def lrrotate(root):
    root.left = rrrotate(root.left)
    return llrotate(root)


def rlrotate(root):
    root.right = llrotate(root.right)
    return rrrotate(root)


class AVLTree(object):
    def __init__(self):
        self.root = None

    def insert(self, node):
        if not self.root:
            self.root = node
        else:
            self.root = self._insert(self.root, node)

    def _insert(self, root, node):
        if not root:
            root = node
        elif root.key > node.key:
            root.left = self._insert(root.left, node)
            if get_height(root.left) - get_height(root.right) > 1:
                if node.key < root.left.key:
                    root = llrotate(root)
                else:
                    root = lrrotate(root)
        elif root.key < node.key:
            root.right = self._insert(root.right, node)
            if get_height(root.right) - get_height(root.left) > 1:
                if node.key > root.right.key:
                    root = rrrotate(root)
                else:
                    root = rlrotate(root)
        root.height = max(get_height(root.left), get_height(root.right)) + 1
        return root

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if not root:
            print("Key not in AVLTree")
            return
        else:
            if root.key > key:
                root.left = self._delete(root.left, key)
                if get_height(root.right) - get_height(root.left) > 1:
                    if get_height(root.right.left) > get_height(root.right.right):
                        root = rlrotate(root)
                    else:
                        root = rrrotate(root)
            elif root.key < key:
                root.right = self._delete(root.right, key)
                if get_height(root.left) - get_height(root.right) > 1:
                    if get_height(root.left.right) > get_height(root.left.left):
                        root = lrrotate(root)
                    else:
                        root = llrotate(root)
            else:
                if root.left and root.right:
                    if get_height(root.left) > get_height(root.right):
                        tmp_node = get_maximun(root.left)
                        root.key = tmp_node.key
                        root.left = self._delete(root.left, root.key)
                    else:
                        tmp_node = get_minimun(root.right)
                        root.key = tmp_node.key
                        root.right = self._delete(root.right, root.key)
                else:
                    root = root.left if root.left else root.right
            root.height = max(get_height(root.left), get_height(root.right)) + 1
        return root


def main():
    number_list = (7, 4, 1, 8, 5, 2, 9, 6, 3)
    tree = AVLTree()
    for number in number_list:
        node = AVLNode(number)
        tree.insert(node)
    pre_order(tree.root)
    tree.delete(4)
    print('==========')
    pre_order(tree.root)


if __name__ == '__main__':
    main()

