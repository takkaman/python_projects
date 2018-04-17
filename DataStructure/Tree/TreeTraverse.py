from queue import Queue


def pre_order(root):
    if root:
        print(root.key)
        pre_order(root.left)
        pre_order(root.right)


def level_lorder(root):
    q = Queue()


def zig_zag_level_order(root):
    pass


def post_order(root):
    if root:
        post_order(root.left)
        post_order(root.right)
        print(root.key)