class State:
    def __init__(self, position):
        self.position = position 

    def __eq__(self, other):
        return isinstance(other, State) and self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return f"State({self.position})"

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    open = set()
    closed = set()

    M = State(start) 
    goal_state = State(goal)

    open.add(M)

    g = {M: 0}  
    h = {M: abs(start[0]-goal[0]) + abs(start[1]-goal[1])}  
    f = {M: g[M] + h[M]}  # Total cost
    parent = {M: None}

    while open:
        # Select node M with lowest f
        M = min(open, key=lambda x: f[x])

        if M == goal_state:
            # Reconstruct path
            path = []
            while M:
                path.append(M.position)
                M = parent[M]
            path.reverse()
            return path, g[goal_state] 
        open.remove(M)
        closed.add(M)

        # Explore neighbors
        directions = [(0,1),(1,0),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1),(1,1)]
        for dr, dc in directions:
            new_r, new_c = M.position[0] + dr, M.position[1] + dc
            if 0 <= new_r < rows and 0 <= new_c < cols and grid[new_r][new_c] != 1:
                N = State((new_r, new_c))

                if N in closed:
                    continue

                tentative_g = g[M] + 1

                if N not in open or tentative_g < g.get(N, float("inf")):
                    parent[N] = M
                    g[N] = tentative_g
                    h[N] = abs(new_r - goal[0]) + abs(new_c - goal[1])
                    f[N] = g[N] + h[N]
                    open.add(N)

    return None, -1  

grid = [
    [0,0,0,1,0],
    [0,1,0,1,0],
    [0,1,0,0,0],
    [0,0,0,1,0],
    [1,1,0,0,0]
]
start = (0,0)
goal = (4,4)

path, cost = a_star(grid, start, goal)
if path:
    print("Path:", path)
    print("Path cost:", cost)
    print("Path length:", len(path)-1)
else:
    print("No path found, length = -1")

