# a* algorithm -> informed search algorithm
# f(n) = g(n) + h(n) 
# g(n) is the cost from the start node to the current node(n)
# h(n) is the heuristic cost(estimated cost) from the current node(n) to the goal node
# here diagonal movement is not allowed so we consider h(n) as the manhattan distance between the current node(n) and the goal node
# if we have to choose between two nodes with the same cost value then we will choose the node with the lowest h(n) value 
# we are going to use a Priority queue to store the nodes based on their f(n)

from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue  # importing priority queue from the module queue

# creating the heuristic function
def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

# now the A_star function
def aStar(m):  # argument is m since one maze
    start = (m.rows, m.cols)
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, (1, 1))

    # priority queue
    open = PriorityQueue()
    open.put((h(start, (1, 1)), h(start, (1, 1)), start))  # first is f(n), second is h(n), third is the cell
    aPath = {}  # stores child -> parent mappings (i.e., how we reached each cell)

    # check condition when queue is not empty and find child cells
    while not open.empty():
        currCell = open.get()[2]
        if currCell == (1, 1):
            break
        # finding the child cell in all four directions
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                if d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                if d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                if d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                # update weights after finding the child cell
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, (1, 1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell, (1, 1)), childCell))
                    aPath[childCell] = currCell  # store child -> parent for path reconstruction

    # -------------------------
    # Build FORWARD path (start -> goal):
    # trace from goal (1,1) back to start using aPath and flip to get parent -> child
    # -------------------------
    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[aPath[cell]] = cell  # parent -> child = forward direction
        cell = aPath[cell]

    # -------------------------
    # Build REVERSE path (goal -> start):
    # revPath[cell] = aPath[cell] means: from this cell, move to its parent (toward start)
    # -------------------------
    revPath = {}
    cell = (1, 1)
    while cell != start:
        revPath[cell] = aPath[cell]  # current cell -> parent = moving toward start
        cell = aPath[cell]

    return fwdPath, revPath

x = int(input("Enter the rows:"))
y = int(input("Enter the columns:"))
# create a random 5 by 5 maze
m = maze(x, y)
m.CreateMaze()

# run A* and get both forward and reverse paths
fwdPath, revPath = aStar(m)

# -------------------------
# Agent 1 (Yellow): Traces the REVERSE path (goal -> start)
# Goes FIRST — paints the yellow highlight across the solution path
# shape='square' + filled=True gives solid colored block look (like reference image)
# -------------------------
agentReverse = agent(
    m,
    1, 1,                    # start at goal cell (1,1)
    goal=(m.rows, m.cols),   # destination is the start cell
    footprints=True,
    color=COLOR.yellow,      # yellow highlight
    shape='square',          # solid square blocks, not arrows
    filled=True
)

# -------------------------
# Agent 2: Original forward agent (start -> goal)
# Goes SECOND — walks the correct A* path after the yellow path is fully drawn
# -------------------------
a = agent(m, footprints=True)  # original agent just like in your code

# -------------------------
# TWO SEPARATE tracePath calls to ensure sequence:
# 1st call: yellow reverse agent traces goal -> start (paints yellow first)
# 2nd call: original agent traces start -> goal (walks on top after yellow is done)
# delay=200ms slows it down so the animation is clearly visible
# -------------------------
m.tracePath({agentReverse: revPath}, delay=200)  # step 1: yellow reverse path first
m.tracePath({a: fwdPath}, delay=200)             # step 2: forward agent walks after

# display path length label (same as original)
l = textLabel(m, 'A Star Path Length', len(fwdPath) + 1)

print(m.grid)
m.run()