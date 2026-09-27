#main file. 

# get functions imported from bool_func.py
import bool_func as bf
import tree_node as tn
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

#creating UT and CT

#UT from var_order
#-10-> 0 id
#-100->1 id
UT = tn.HashTable()
cur = UT.head()
count = len(var_order)
for i in range(1,count+1):
    UT.add(var_order[i-1],i,-10,-100,i+1,cur)
    cur = i

CT = tn.HashTable()





if len(be_split)!=0:
    pass