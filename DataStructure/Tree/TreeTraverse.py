from queue import Queue


def pre_order(root):
    if root:
        print(root.key)
        pre_order(root.left)
        pre_order(root.right)


def level_lorder(root):
    if not root:
        return
    q = Queue()
    q.put(root)
    last_node = root
    pre_node = None
    print_buf = []
    level_buf = []
    height = 1

    while not q.empty():
        node = q.get()
        level_buf.append(node)
        if node.left:
            q.put(node.left)
            pre_node = node.left
        if node.right:
            q.put(node.right)
            pre_node = node.right

        if node == last_node:
            height += 1
            last_node = pre_node
            print_buf.extend(level_buf)
            level_buf = []

    for node in print_buf:
        print(node.key)


def zig_zag_level_order(root):
    if not root: return
    q = Queue()
    q.put(root)
    last_node = root
    pre_node = None
    print_buf = []
    level_buf = []
    height = 1

    while not q.empty():
        node = q.get()
        level_buf.append(node.key)
        if node.left:
            q.put(node.left)
            pre_node = node.left
        if node.right:
            q.put(node.right)
            pre_node = node.right

        if node == last_node:
            if height % 2 == 0:
                level_buf.sort(reverse=True)

            print_buf.extend(level_buf)
            last_node = pre_node
            level_buf = []
            height += 1

    for key in print_buf:
        print(key)


def post_order(root):
    if root:
        post_order(root.left)
        post_order(root.right)
        print(root.key)

        
def in_order(root):
    if root:
        in_order(root.left)
        print(root.key)
        in_order(root.right)