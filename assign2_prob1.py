import math

class state:
    def __init__(self, loc, board):
        self.loc = loc
        self.board = board

    def testGoal(self):
        return self.loc[0] == len(self.board) - 1 and self.loc[1] == len(self.board[0]) - 1

    def moveGen(self):
        directions = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        children = []
        for dr, dc in directions:
            nr, nc = dr + self.loc[0], dc + self.loc[1]
            if (0 <= nr < len(self.board) and 0 <= nc < len(self.board[0]) 
                and self.board[nr][nc] == 0): 
                new_loc = (nr, nc)
                children.append(state(new_loc, self.board))
        return children

    def heuristicValue(self):
        # Euclidean distance
        return math.sqrt((len(self.board)-1-self.loc[0])**2 + (len(self.board[0])-1-self.loc[1])**2)

    def min_node(self, open):
        min_val = float('inf')
        minNode = (None, None)
        for node_pair in open:
            if node_pair[0].heuristicValue() < min_val:
                minNode = node_pair
                min_val = node_pair[0].heuristicValue()
        return minNode

    def removeSeen(self, open, closed, children):
        open_nodes = [n for n, p in open]
        closed_nodes = [n for n, p in closed]
        return [child for child in children if child not in open_nodes and child not in closed_nodes]

    def reconstructpath(self, closed, goal_node_pair):
        path = []
        path_map = {node: parent for node, parent in closed}
        node = goal_node_pair[0]

        while node is not None:
            path.append(node)
            node = path_map.get(node)

        path.reverse()
        return path

    def BestFirstSearch(self):
        open = [(self, None)]
        closed = []

        while open:
            node_pair = self.min_node(open)
            N, parent = node_pair
            open.remove(node_pair)  

            if N.testGoal():
                return self.reconstructpath(closed, node_pair)

            closed.append(node_pair)
            children = N.moveGen()
            children = self.removeSeen(open, closed, children)
            child_pairs = [(child, N) for child in children]
            open.extend(child_pairs)

        return None  

    def __str__(self):
        return str(self.loc)

    def __hash__(self):
        return hash(self.loc)

    def __eq__(self, other):
        return isinstance(other, state) and self.loc == other.loc


# Example grid (0 = free, 1 = blocked)
board = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 0]
]

loc = (0,0)
obj = state(loc, board)

path = obj.BestFirstSearch()
if path:
    print("Path found:")
    for node in path:
        print(node)
    print("Path length:", len(path))   
else:
    print("No path exists.")
    print("Path length: -1")           
