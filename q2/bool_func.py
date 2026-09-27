#developing in PCN notation
from math import fabs
import tree_node as tn


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
        node = tn.TreeNode(var, high, low)
        node.id = counter[0] 
        counter[0] += 1
        node.left, node.right = low, high
        UT[var][key] = node
    CT[var][sig] = node
    return node


