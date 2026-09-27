def find_order(be_list,verbose=False):
    counts = {}
    for term in be_list:
        for ch in term:
            v = ch.lower()
            counts[v] = counts.get(v, 0) + 1
    order = sorted(counts, key=lambda v: counts[v], reverse=True) #this already works right

    #trying to get linked variables to be grouped closer
    list_order =[order[0],]
    order_x =[]
    for n in range(1,len(order)):
        for term2 in order[n+1:]:
            if (counts[order[n]] < counts[term2]):
                if counts[order[n]] not in list_order:
                    list_order.append(order[n])
            elif (counts[order[n]]) == counts[term2]:
                x = {}
                for term in be_list:
                    for ch in term:
                        if order[n] in term:
                            v = ch.lower()
                            x[v] = x.get(v, 0) + 1
                order_x = sorted(x, key=lambda v: x[v], reverse=True)
                if len(order_x) !=0:
                    list_order.append(order_x[0])
                else:
                    list_order.append()

    if verbose:
        print("variable order = ", list_order)
    return list_order

be_list = ["ABC","Abc","bC","aBc"]

# be_list = ["ac","bc","ab"]



x = find_order(be_list,True)