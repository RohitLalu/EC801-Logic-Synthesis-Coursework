def in_order(be_list):   #sorting the variables in product terms alphabetically
    # input: Bac + cAb-> output: aBc + Abc
    out=[]
    for i in be_list:
        st = ""
        x = list(i)
        y = list(i.lower())     #convert all letters to lowercase
        y.sort()                #alphabetical sorting
        for j in y:             #preserve the case sensitivity
            if (j in x):
                st+=j
            elif (j.upper() in x):
                st+= j.upper()
        out.append(st)
    return out


#SOP form
#eg: list = ['ab','aB','AB'] represents ab + aB + AB
def list_to_exp(list_s,verbose=False):     #converts list of product terms in SOP form
    x=""
    if len(list_s)==0:
        x="0"
    else:  
        for i in list_s[:-1]:
            x+=i
            x+=" + "
        x+=list_s[-1]
    if verbose:
        print(x)
    return x


def cofactor_single(var,be_list,verbose=False):   #finding cofactor wrt one variable
    if var ==var.lower():
        var_b = var.upper()
    else:
        var_b = var.lower()
    cof_var = []
    cof_var_bar = []
    be_list = in_order(be_list)
    for i in be_list:
        if (var not in i) and (var_b not in i):      #if var and var_bar not there, term remains same
            cof_var.append(i)
            cof_var_bar.append(i)
        elif (var in i):                             #if the variable is there, remove it from the term 
            if len(i.replace(var,''))==0:
                cof_var.append('1')
            else:
                cof_var.append(i.replace(var,'')) 
        elif (var_b in i):                           #if variable_bar is there, remove the complemented version from the term 
            if len(i.replace(var_b,''))==0:
                cof_var_bar.append('1')
            else:
                cof_var_bar.append(i.replace(var_b,''))

    #simplification without bool_simplify    #A+1=1
    if "1" in cof_var:
        cof_var = ["1"]
    if "1" in cof_var_bar:
        cof_var_bar = ["1"]

    if verbose:
            print(f"f_var:{list_to_exp(cof_var)}")
            print()
            print(f"f_var_bar:{list_to_exp(cof_var_bar)}")
            print()
    return cof_var,cof_var_bar

def find_order(be_list,verbose=False):  #counts how many times each var appears and arranges from most to least frequent
    counts = {}
    for term in be_list:
        for ch in term:
            if ch.isalpha():
                v = ch.lower()
                counts[v] = counts.get(v, 0) + 1
    order = sorted(counts, key=lambda v: counts[v], reverse=True)
    if verbose:
        print("variable order = ", order)
    return order

def bool_simplify(be_list,order=None,verbose=False):    #simplification of boolean expression in SOP form
    out = list(set(be_list))  #remove duplicate terms
    if len(out) == 0:
        return []
    if "1" in out:            #if 1 is there, result=1
        return ["1"]

    # drop any term containing both a variable and its complement
    out = [t for t in out if not any(ch.isupper() and ch.lower() in t for ch in t)]
    if len(out) == 0:
        return []

    if order is None:
        order = find_order(out)
    if not order:
        return out

    var = order[0]
    f_v, f_v_bar = cofactor_single(var,out,verbose=False)   #finding cofactors 
    f_v     = bool_simplify(f_v,verbose=False)              #simplify recursively
    f_v_bar = bool_simplify(f_v_bar,verbose=False)

    if f_v == f_v_bar: # var doesn't matter (covers 0/0, 1/1, and any other tie)
        out = f_v
    elif f_v == []:
        out = [var.upper() if t == '1' else var.upper()+t for t in f_v_bar]
    elif f_v_bar == []:
        out = [var.lower() if t == '1' else var.lower()+t for t in f_v]
    else:
        out = [var.upper() if t == '1' else var.upper()+t for t in f_v_bar]
        out += [var.lower() if t == '1' else var.lower()+t for t in f_v]

    if verbose:
        print ("check simplified exp = ",out)
    return out


def boolean_diff_single(f_v,f_v_bar,verbose=False):  #function to find boolean difference (xor), checks if function changes when variable changes
    f_v     = bool_simplify(f_v)
    f_v_bar = bool_simplify(f_v_bar)
    if f_v == f_v_bar:
        f = []  #xor of identical functions is 0
    else:
        order = find_order(f_v + f_v_bar)
        if not order:   #both sides are constants and differ -> {},1 or 1,{}
            f = ['1']
        else:
            var = order[0]
            g1, g0 = cofactor_single(var, f_v)
            h1, h0 = cofactor_single(var, f_v_bar)
            x1 = boolean_diff_single(g1, h1)            #recursively find the difference 
            x0 = boolean_diff_single(g0, h0)
            if x1 == x0:
                f = x1
            else:
                f  = [var.upper() if t == '1' else var.upper()+t for t in x0]
                f += [var.lower() if t == '1' else var.lower()+t for t in x1]
                f  = bool_simplify(f)
    if verbose:
            print(f"f_bool_diff:{list_to_exp(f)}")
            print()
    return f

def and_sop(g,h):      #find AND of boolean functions 
    """AND of two SOP-form functions via recursive cofactor pattern"""
    g = bool_simplify(g)
    h = bool_simplify(h)
    if g == [] or h == []:
        return []
    if g == ["1"]:
        return h
    if h == ["1"]:
        return g
    order = find_order(g + h)
    if not order:
        return []
    var = order[0]
    g1, g0 = cofactor_single(var,g)
    h1, h0 = cofactor_single(var,h)
    a1 = and_sop(g1,h1)
    a0 = and_sop(g0,h0)
    if a1 == a0:
        return a1
    out  = [var.upper() if t == '1' else var.upper()+t for t in a0]
    out += [var.lower() if t == '1' else var.lower()+t for t in a1]
    return bool_simplify(out)

def boolean_consensus_single(f_v,f_v_bar,verbose=False):   #consensus (AND)
    f = and_sop(f_v,f_v_bar)
    if verbose:
        print(f"f_consensus:{list_to_exp(f)}")
        print()
    return f

def boolean_smoothing_single(f_v,f_v_bar,verbose=False):    #smoothing function (OR)
    f = f_v + f_v_bar
    f = list(set(f))
    f = bool_simplify(f,verbose=False)

    if verbose:
        print(f"f_smoothing:{list_to_exp(f)}")
        print()
    return f


#multi case

def cofactor_recursion(var_str,be_list):
    working_list = be_list
    for ch in var_str:
        f_v,f_v_bar = cofactor_single(ch,working_list,False)
        working_list = f_v
    return working_list

def cofactor_multi(var_str,be_list,verbose=False):      #finding cofactors of multiple variables using recursion 
    """Cofactor be_list at every corner of the hypercube spanned by the
    variables in var_str. Returns (f at var_str's own assignment, dict
    mapping every OTHER corner's signed string -> its cofactor)."""
    k = len(var_str)
    corners = {}
    for bits in range(2**k):
        signed = ''.join(
            var_str[i].lower() if (bits >> i) & 1 else var_str[i].upper()
            for i in range(k)
        )
        corners[signed] = cofactor_recursion(signed,be_list)
    f_v_final = corners.pop(var_str)
    if verbose:
        print(f"f_{var_str}:{list_to_exp(f_v_final)}")
        print()
        print(f"f = f_{var_str}({list_to_exp(f_v_final)})",end="")
        for s,f in corners.items():
            print(f" + f_{s}({list_to_exp(f)})",end="")
        print()
    return f_v_final,corners

def boolean_consensus_multi(var_str,be_list,verbose=False):   #consensus for multi variable cofactors
    """Universal quantification over var_str's variables = AND of all 2^k corners."""
    f_v, corners = cofactor_multi(var_str,be_list)
    f = f_v
    for c in corners.values():
        f = and_sop(f,c)
    if verbose:
        print(f"f_consensus_{var_str}:{list_to_exp(f)}")
        print()
    return f

def boolean_smoothing_multi(var_str,be_list,verbose=False):    #smoothing function for multi variable cofactors
    """Existential quantification over var_str's variables = OR of all 2^k corners."""
    f_v, corners = cofactor_multi(var_str,be_list)
    f = list(f_v)
    for c in corners.values():
        f = f + c
    f = bool_simplify(f)
    if verbose:
        print(f"f_smoothing_{var_str}:{list_to_exp(f)}")
        print()
    return f

def flip_vars(be_list,var_str):    #changes polarity of selected variable
    """Swap the polarity of every variable named in var_str throughout be_list."""
    flip_set = set(var_str.lower())
    out = []
    for term in be_list:
        if term == '1':
            out.append(term); continue
        new_term = ''.join(
            (ch.upper() if ch.islower() else ch.lower()) if ch.lower() in flip_set else ch
            for ch in term
        )
        out.append(new_term)
    return out

def boolean_diff_multi(var_str,be_list,verbose=False):    #boolean difference for multi variable cofactors
    f         = bool_simplify(be_list)
    f_flipped = bool_simplify(flip_vars(f,var_str))
    diff = boolean_diff_single(f,f_flipped)
    if verbose:
        print(f"f_bool_diff_{var_str}:{list_to_exp(diff)}")
        print()
    return diff


#main 

"""
assumptions:
1.file input -> one line of text -> one expression 
2. a ->a, A-> a'
3. seperation using + only and no brackets
"""

file_name = input("Enter test  file name: ")   #input file
exp_no = int(input("Enter which expression to eval: "))   

check = int(input("""Do you want to enter 
1. control variable? 
2. control variables?
Enter 1 or 2: """))

if check ==1:
    var = input("Enter control variable: ")
elif check==2:
    vars = input("Enter control variables (together no spaces in the order to be evaluated): ")
else:
    print("Invalid input. Please enter 1 or 2.")
    exit()

be_split = []

#open the input text file, perform operations onthe selected expression. 
with open(file_name, 'r') as f:
    for i, bool_exp in enumerate(f):
        if (i+1) == exp_no:
            bool_exp = bool_exp.strip()
            be_split = [t.strip() for t in bool_exp.split('+')]

#function calls to perform boolean operations 
if len(be_split)!=0:
    if check == 1:
        if var not in bool_exp.lower():
            print("Control variable not in expression. Cofactors are equal to each other and equal to the original expression.")
        f_v, f_v_bar = cofactor_single(var,be_split,verbose=True)
        f_v = bool_simplify(f_v)
        f_v_bar = bool_simplify(f_v_bar)
        f_diff = boolean_diff_single(f_v,f_v_bar,True)
        f_consensus = boolean_consensus_single(f_v,f_v_bar,True)
        f_smoothing = boolean_smoothing_single(f_v,f_v_bar,True)
    elif check == 2:
        if not all(v.lower() in bool_exp.lower() for v in vars):
            print("WARNING: Not all control variables are in the expression.")
        f_v_multi, other_corners = cofactor_multi(vars,be_split,verbose=True)
        f_diff = boolean_diff_multi(vars,be_split,True)
        f_consensus = boolean_consensus_multi(vars,be_split,True)
        f_smoothing = boolean_smoothing_multi(vars,be_split,True)
