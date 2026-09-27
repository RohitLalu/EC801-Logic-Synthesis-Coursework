#main file. 

# get functions imported from bool_func.py
import bool_func as bf
import tree_node as tn
import draw


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
            be_split = bf.in_order(be_split)

#start pre processing
var_order = bf.find_order(be_split)
pcn_list = bf.list_to_pcn(be_split)

T0 = tn.TreeNode("0", None, None); T0.id = 0
T1 = tn.TreeNode("1", None, None); T1.id = 1
UT = {v: {} for v in var_order}
CT = {v: {} for v in var_order}
counter = [2]

root = bf.build_robdd(pcn_list, var_order, 0, UT, CT, T0, T1, counter)

def show(n):
    return f"id={n.id} TERMINAL {n.literal}" if n.left is None else \
           f"id={n.id} var={n.literal} low={n.left.id} high={n.right.id}"

print("DFS:")
[print(show(n)) for n in root.dfs()]
print("BFS:")
[print(show(n)) for n in root.bfs()]

draw.draw_robdd(root, var_order)