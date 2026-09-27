

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

    def unvisit_all(self):
        self.visited = False
        if self.left == None and self.right == None:
            return True
        else:
            self.unvisit_all(self.left)
            self.unvisit_all(self.right)

        return True

    def dfs(self,id,verbose = False):
        if self.id == id:
            return self.id, self.head
        self.visited = True
        if verbose:
            print(self.id)
        if self.left == None and self.right == None:
            return None
        self.dfs(self.left,id)
        self.dfs(self.right,id)

    def bfs(self,id,verbose=False):
        if self.id == id:
            return self.id, self.head



    #runs like singly linked list        
class HashTable_node: #runs entirely on id of node
    def __init__(self,literal,id,left,right):
        self.literal = literal
        self.id = id
        #graph section
        self.left = left
        self.right = right
        #ll section
        self.next = None
        self.prev = None

class HashTable:
    def __init__(self):
        self.head = None

    def add(self,literal,id,left,right,next,prev):
        new_node = HashTable_node(literal,id,left,right,next,prev)
            

        #deletion not straightforward. dont simply delete from ll. rather need to remove the graph node instead.
        # def delete(self,id,count):
        #     i = 0
        #     while i<count:
        #         i+=1
        #         if self.id==id:
        #             if self.prev==None:
        #                 self.next.prev = None
        #                 self.next = None
        #             else:
        #                 self.prev.next = self.next
        #                 self.next.prev = self.prev
        #             break
        #     else:
        #         print("element to be deleted not found")
    
        def search(self,literal,check=True):
            if self.literal ==literal:
                return self.id
            elif self.next == None:
                if check:
                    return -1
                else:
                    return self.id #not found but return previous element id to create new element
            else:
                self.search(self.next,literal)
    
    
        def search_id(self,id,check=True):
            if self.id ==id:
                return self.literal
            elif self.next == None:
                if check:
                    return -1
                else:
                    return self.id 
            else:
                self.search_id(self.next,id)
    
        def actual_add(self,literal,left,right,count):
            check = self.search(literal)
            if check==-1:
                prev = self.search(literal,False)
                if left==right:
                    #no need to add this element. direct skip to next literal
                    #TODO: finish check
                    pass
                else:
                    count+=1
                    self.add(literal,count,left,right,prev)
            return count
    
            
    
    
    
    
    
    