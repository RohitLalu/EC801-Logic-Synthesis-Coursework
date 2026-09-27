#developing in PCN notation
from math import fabs
import tree_node


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

def cofactor_single(var: str,pcn_list: list):
    org = []
    comp = []
    if pcn_list == [1]:
        return [1],[0]
    elif pcn_list == [0]:
        return [0],[1]
    else:
        for be in pcn_list:
            if be[var] == 1:
                be.pop(var)
                if len(be)>0:
                    org.append(be)
                else:
                    org.append(1)
            elif be[var] == 2:
                be.pop(var)
                if len(be)>0:
                    comp.append(be)
                else:
                    comp.append(1)
            else:
                be.pop(var)
                if len(be)>0:
                    org.append(be)
                    comp.append(be)
                else:
                    org.append(1)
                    comp.append(1)
            
    if 1 in org:
        org =[1]
    if 1 in comp:
        comp = [1]

    return org,comp
        

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

def var_find(be_list:list):
    n = 0
    exp = ""
    for i in be_list:
        if len(i)>n:
            n = len(i)
            i = i.lower()
            i = list(i).sort()
            i = str(i)
            exp= i
    return exp

def list_to_pcn(be_list:list):
    exp=var_find(be_list)
    pcn_list =[]
    dict_cube = {}
    literal=""
    pcn_val = 3 # 1-> 01 (original),2-> 10 (complement),3-> 11 (not present)
    for i in be_list:
        dict_cube.clear()
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

#TODO: FIGURE ACTUALLY
def pcn_cube_to_bdd(pcn_cube:dict):
    for i in pcn_cube:
        pass


