import math

with open("small_parsimony_input.txt", "r") as file:
    tree = file.read().splitlines()



class TreeNode: 
    def __init__(self, node_id, is_leaf):
        self.node_id = node_id
        self.is_leaf = is_leaf
        self.tag = 0
        self.scores = []
        self.left_child = None
        self.right_child = None
        self.sequence = None

    
def clean_data(tree):
    treeNodes = [TreeNode(node_id=i, is_leaf=True) for i in range(int(tree[0]))]
    nodes_id_list = {}
    leaf_sequences = []
    for node in treeNodes:
        node.tag = 1
        nodes_id_list[node.node_id] = []
    for node in tree[1:]:
        node_num = node.split('->')
        node_sequence = node_num[1]
        leaf_sequences.append(node_sequence)
        node_num = int(node_num[0])
        if node_num not in nodes_id_list:
            nodes_id_list[node_num] = []
            nodes_id_list[node_num].append(node_sequence)
            new_node = TreeNode(node_id=node_num, is_leaf=False)
            treeNodes.append(new_node)
            new_node.left_child = leaf_sequences.index(node_sequence)
        elif node_num in nodes_id_list and treeNodes[node_num].right_child == None:
            nodes_id_list[node_num].append(node_sequence)
            update_node = treeNodes[node_num]
            update_node.right_child = leaf_sequences.index(node_sequence)
    for node in treeNodes:
        if node.is_leaf:
            node.sequence = leaf_sequences[node.node_id]
            for i in node.sequence:
                if i == 'A':
                    node.scores.append([0,1,1,1])
                elif i == 'C':
                    node.scores.append([1,0,1,1])
                elif i == 'G':
                    node.scores.append([1,1,0,1])
                elif i == 'T':
                    node.scores.append([1,1,1,0])
    len_sequence = len(treeNodes[0].sequence)
    for node in treeNodes:
        if not node.is_leaf:
            for i in range(len_sequence):
                node.scores.append([0,0,0,0])

    return treeNodes

def parsimony(tree: list[TreeNode]):
    options = ['A', 'C', 'G', 'T']
    for node in tree:
        if not node.is_leaf:
            right_child = tree[node.right_child].sequence
            left_child = tree[node.left_child].sequence
            for i in range(len(right_child)):
                for j in options:
                    update_scores(node,i,j,tree[node.right_child].scores[i])
                    update_scores(node,i,j,tree[node.left_child].scores[i])
                        
            node.sequence = ''
            for position in node.scores:
                pos = position.index(min(position))
                if pos == 0:
                    node.sequence += 'A'
                elif pos == 1:
                    node.sequence += 'C'
                elif pos == 2:
                    node.sequence += 'G'
                elif pos == 3:
                    node.sequence += 'T'           
    return tree

def update_scores(node: TreeNode, spot: int, value: str, children: list[int]):
    if value == 'A':
        node.scores[spot][0] += children[0]
    elif value == 'C':
        node.scores[spot][1] += children[1]
    elif value == 'G':
        node.scores[spot][2] += children[2]
    elif value == 'T':
        node.scores[spot][3] += children[3]


def hamming_distance(p: str, q: str) -> int:
    """Calculate the Hamming distance between two strings."""
    hamming = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            hamming += 1
    return hamming

def print_final(node,tree,f):
    if node.is_leaf:
        return
    print(f"{node.sequence}->{tree[node.right_child].sequence}:{hamming_distance(node.sequence,tree[node.right_child].sequence)}", file=f)
    print(f"{node.sequence}->{tree[node.left_child].sequence}:{hamming_distance(node.sequence,tree[node.left_child].sequence)}", file=f)
    print(f"{tree[node.right_child].sequence}->{node.sequence}:{hamming_distance(node.sequence,tree[node.right_child].sequence)}", file=f)
    print(f"{tree[node.left_child].sequence}->{node.sequence}:{hamming_distance(node.sequence,tree[node.left_child].sequence)}", file=f)
    print_final(tree[node.right_child],tree,f)
    print_final(tree[node.left_child],tree,f)

data = clean_data(tree)
data = parsimony(data)

parsimony_score = 0
for pos in data[-1].scores:
    parsimony_score += min(pos)

with open("small_parsimony_output_test.txt", 'w') as f:
    print(parsimony_score, file=f)
    print_final(data[-1],data,f)



