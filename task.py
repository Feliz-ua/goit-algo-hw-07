import matplotlib.pyplot as plt
import networkx as nx

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self, level=0, prefix="Root: "):
        r = "\t" * level + prefix + str(self.key) + "\n"
        if self.left:
            r += self.left.__str__(level + 1, "L--- ")
        if self.right:
            r += self.right.__str__(level + 1, "R--- ")
        return r

def get_height(node):
    if node is None:
        return 0
    return node.height

def get_balance(node):
    if node is None:
        return 0
    return get_height(node.left) - get_height(node.right)

def left_rotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2

    z.height = 1 + max(get_height(z.left), get_height(z.right))    
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y
    
def right_rotate(z):
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3

    z.height = 1 + max(get_height(z.left), get_height(z.right))    
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)
    
   # Left Left
    if balance > 1 and key < root.left.key:
        return right_rotate(root)

    # Right Right
    if balance < -1 and key > root.right.key:
        return left_rotate(root)

    # Left Right
    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)

    # Right Left
    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

def find_max(root):
    if root is None:
        return None
    current = root
    while current.right is not None:
        current = current.right
    return current.key

def find_min(root):
    if root is None:
        return None
    current = root
    while current.left is not None:
        current = current.left
    return current.key

def sum_values(root):
    if root is None:
        return 0
    return root.key + sum_values(root.left) + sum_values(root.right)
   
def add_edges(node, G, pos, x=0, y=0, dx=1.0):
    """Рекурсивно додає вузли та ребра в граф і задає координати."""
    if node is None:
        return

    G.add_node(node.key)
    pos[node.key] = (x, y)

    if node.left:
        G.add_edge(node.key, node.left.key)
        add_edges(node.left, G, pos, x - dx, y - 1, dx / 2)

    if node.right:
        G.add_edge(node.key, node.right.key)
        add_edges(node.right, G, pos, x + dx, y - 1, dx / 2)


def draw_tree(root):
    G = nx.DiGraph()
    pos = {}
    add_edges(root, G, pos)

    plt.figure(figsize=(5, 5))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1000,
        node_color="#4f7cff",
        font_color="white",
        arrows=False,
        linewidths=1.5,
        edge_color="black",
    )
    plt.axis("off")
    plt.show()
    
if __name__ == "__main__":
    root = None
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15]
    for key in keys:
        root = insert(root, key)

    print(root)
    print("Максимальне значення:", find_max(root))
    print("Мінімальне значення:", find_min(root))
    print("Сума всіх значень:", sum_values(root))
    draw_tree(root)
    