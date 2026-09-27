#developing in PCN notation
import networkx as nx
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, literal, cofactor, cofactor_bar):
        self.literal = literal
        self.cofactor = cofactor
        self.cofactor_bar = cofactor_bar
        self.id = 0
        self.visited = False

        #ids are shared not literal
        self.head = None
        self.left = None # convention: left 0 right 1
        self.right = None

    def dfs(self, order=None, seen=None):
        if order is None: 
            order = []
        if seen is None: 
            seen = set()
        if self.id in seen:
            return order
        seen.add(self.id)
        order.append(self)
        if self.left is not None: 
            self.left.dfs(order, seen)
        if self.right is not None: 
            self.right.dfs(order, seen)
        return order

    def bfs(self):
        from collections import deque
        seen, order, q = {self.id}, [self], deque([self])
        while q:
            node = q.popleft()
            for next in (node.left, node.right):
                if next is not None and next.id not in seen:
                    seen.add(next.id); order.append(next); q.append(next)
        return order

#helper functions

def in_order(be_list: list):
    # input: Bac + cAb-> output: aBc + Abc
    out=[]
    for i in be_list:
        st = ""
        x = list(i)
        y = list(i.lower())
        y.sort()
        for j in y:
            if (j in x):
                st+=j
            elif (j.upper() in x):
                st+= j.upper()
        out.append(st)
    return out

def cofactor_single(var: str, pcn_list: list):
    if pcn_list == [1]:
        return [1], [1]
    if pcn_list == [0]:
        return [0], [0]
    org, comp = [], []
    for be in pcn_list:
        val = be[var]
        nb = dict(be)
        nb.pop(var)
        if val == 1:
            org.append(nb if nb else 1)
        elif val == 2:
            comp.append(nb if nb else 1)
        else:
            org.append(nb if nb else 1)
            comp.append(nb if nb else 1)
    if 1 in org: org = [1]
    if 1 in comp: comp = [1]
    if not org: org = [0]
    if not comp: comp = [0]
    return org, comp
        

def find_order(be_list:list,verbose=False):
    counts = {}
    for term in be_list:
        for ch in term:
            v = ch.lower()
            counts[v] = counts.get(v, 0) + 1
    order = sorted(counts, key=lambda v: counts[v], reverse=True)
    if verbose:
        print("variable order = ", order)
    return order

def var_find(be_list: list):
    letters = set()
    for i in be_list:
        letters.update(i.lower())
    return "".join(sorted(letters))

def list_to_pcn(be_list:list):
    exp=var_find(be_list)
    pcn_list =[]
    literal=""
    pcn_val = 3 # 1-> 01 (original),2-> 10 (complement),3-> 11 (not present)
    for i in be_list:
        dict_cube={}
        for j in exp:
            literal = j
            if j in i:
                pcn_val = 1
            elif j.upper() in i:
                pcn_val = 2
            else:
                pcn_val = 3
            dict_cube[j] = pcn_val
        pcn_list.append(dict_cube)
    return pcn_list

def pcn_signature(pcn_list: list):
    if pcn_list == [0]: return 0
    if pcn_list == [1]: return 1
    cubes = [tuple(sorted((v, val) for v, val in be.items() if val != 3))
             for be in pcn_list]
    return tuple(sorted(cubes))

def build_robdd(pcn_list, var_order, id, UT, CT, T0, T1, counter):
    if pcn_list == [0]: 
        return T0
    if pcn_list == [1]: 
        return T1
    
    var = var_order[id]
    sig = pcn_signature(pcn_list)
    if sig in CT[var]:
        return CT[var][sig]
    org, comp = cofactor_single(var, pcn_list)
    low  = build_robdd(comp, var_order, id + 1, UT, CT, T0, T1, counter)
    high = build_robdd(org,  var_order, id + 1, UT, CT, T0, T1, counter)

    if low is high:
        CT[var][sig] = low
        return low
    key = (low.id, high.id)
    node = UT[var].get(key)
    
    if node is None:
        node = TreeNode(var, high, low)
        node.id = counter[0] 
        counter[0] += 1
        node.left, node.right = low, high
        UT[var][key] = node
    CT[var][sig] = node
    return node


#draw helper functions

def draw_robdd(root, var_order, out_file="robdd.png"):
    nodes = root.dfs()
    rank = {n.id: (len(var_order) if n.left is None else var_order.index(n.literal))
            for n in nodes}

    by_rank = {}
    for n in nodes:
        by_rank.setdefault(rank[n.id], []).append(n)

    pos, labels, var_nodes, term_nodes = {}, {}, [], []
    G = nx.DiGraph()
    for r, ns in by_rank.items():
        w = len(ns)
        for i, n in enumerate(ns):
            pos[n.id] = (i - (w - 1) / 2, -r)
            G.add_node(n.id)
            labels[n.id] = n.literal
            if n.left is None:
                term_nodes.append(n.id)
            else:
                var_nodes.append(n.id)
                G.add_edge(n.id, n.left.id, kind="low")
                G.add_edge(n.id, n.right.id, kind="high")

    low_edges  = [(u, v) for u, v, d in G.edges(data=True) if d["kind"] == "low"]
    high_edges = [(u, v) for u, v, d in G.edges(data=True) if d["kind"] == "high"]

    plt.figure(figsize=(1.6 * max(len(v) for v in by_rank.values()) + 2,
                         1.4 * len(by_rank) + 1))
    nx.draw_networkx_nodes(G, pos, nodelist=var_nodes, node_shape="o",
                            node_color="white", edgecolors="black", node_size=900)
    nx.draw_networkx_nodes(G, pos, nodelist=term_nodes, node_shape="s",
                            node_color="white", edgecolors="black", node_size=900)
    nx.draw_networkx_labels(G, pos, labels)
    nx.draw_networkx_edges(G, pos, edgelist=low_edges,  style="dashed",
                            connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edges(G, pos, edgelist=high_edges, style="solid",
                            connectionstyle="arc3,rad=0.1")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight")
    print(f"ROBDD written to {out_file}")



"""
assumptions:
1.file input -> one line of text -> one expression 
2. a ->a, A-> a'
3. seperation using + only and no brackets

representation: done in PCN 

"""

file_name = input("Enter test  file name: ")
exp_no = int(input("Enter which expression to convert to ROBDD: "))
be_split = []

with open(file_name, 'r') as f:
    for i, bool_exp in enumerate(f):
        if (i+1) == exp_no:
            bool_exp = bool_exp.strip()
            be_split = [t.strip() for t in bool_exp.split('+')]
            be_split = in_order(be_split)

#start pre processing
var_order = find_order(be_split)
pcn_list = list_to_pcn(be_split)

T0 = TreeNode("0", None, None); T0.id = 0
T1 = TreeNode("1", None, None); T1.id = 1
UT = {v: {} for v in var_order}
CT = {v: {} for v in var_order}
counter = [2]

root = build_robdd(pcn_list, var_order, 0, UT, CT, T0, T1, counter)

def show(n):
    return f"id={n.id} TERMINAL {n.literal}" if n.left is None else \
           f"id={n.id} var={n.literal} low={n.left.id} high={n.right.id}"

print("DFS:")
[print(show(n)) for n in root.dfs()]
print("BFS:")
[print(show(n)) for n in root.bfs()]

draw_robdd(root, var_order)