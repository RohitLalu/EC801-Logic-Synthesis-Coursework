

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