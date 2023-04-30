from time import sleep
import os


def load_maze(name):
    with open(name) as f:
        lines = list(map(str.strip, f.readlines()))
    m = []
    for i in lines:
        m2 = [j for j in list(i)]
        m.append(m2)
    return m


def make_maze(maze_):
    li = []
    for i in maze_:
        l = []
        for j in i:
            if j == "0":  # nothing
                j = " "
            elif j == "1":  # wall
                j = "\033[1;36;48m■\x1b[0m"
            elif j == "2":  # start
                j = "\033[1;32;48m■\x1b[0m"
            elif j == "3":  # end
                j = "\033[1;31;48m■\x1b[0m"
            elif j == "4":  # places went
                j = "\033[1;33;48m■\x1b[0m"
            elif j == "5":  # the way
                j = "\033[1;35;48m■\x1b[0m"
            l.append(j)
        li.append(l)
    return li


def draw_maze(maze_):
    for i in maze_:
        print(*i)


def maze_possible_ways(maze_: list, start: list):
    return_ = []
    if maze_[start[0][0] + 1][start[0][1]] != "1":
        return_.append([[start[0][0] + 1, start[0][1]], start[0]])
    if maze_[start[0][0] - 1][start[0][1]] != "1":
        return_.append([[start[0][0] - 1, start[0][1]], start[0]])
    if maze_[start[0][0]][start[0][1] + 1] != "1":
        return_.append([[start[0][0], start[0][1] + 1], start[0]])
    if maze_[start[0][0]][start[0][1] - 1] != "1":
        return_.append([[start[0][0], start[0][1] - 1], start[0]])
    return return_


def maze_solution_for_dfs_bfs(maze_: list, x_start, y_start, x_end, y_end, way_):
    stack_, went = [], []
    to_go = [[x_start, y_start]]
    a = "-"
    if way_ == 3:
        a = "+"
    while True:
        if [x_end, y_end] in to_go:
            return stack_, maze_
        if a == "+":
            left_to_go = [max(i[0], x_end) - min(i[0], x_end) + (max(i[1], y_end) - min(i[1], y_end)) + 2 for i in
                          to_go]
            way_ = left_to_go.index(min(left_to_go))
        point = [to_go[way_]]
        maze_ret = maze_possible_ways(maze_, point)
        went.append(to_go[way_])
        maze_[to_go[way_][0]][to_go[way_][1]] = "4"
        maze_colored = make_maze(maze_)
        draw_maze(maze_colored)
        print()
        sleep(0.3)
        os.system('cls')
        to_go.pop(way_)
        for i in maze_ret:
            if i[0] not in went and i[0] not in to_go:
                stack_.append(i)
                to_go.append(i[0])



def way_back(stack_, maze_, x_start, y_start, x_end, y_end):
    point = stack_[-1]
    parents = []
    child = []
    for i in stack_:
        child.append(i[0])
        parents.append(i[1])
    maze_[point[0][0]][point[0][1]] = "5"
    while point != stack_[0]:
        maze_[point[1][0]][point[1][1]] = "5"
        point = stack_[child.index(point[1])]
        maze_colored = make_maze(maze_)
        draw_maze(maze_colored)
        print()
        sleep(0.2)
        os.system('cls')
        maze_[x_start][y_start] = "2"
        maze_[x_end][y_end] = "3"


def run():
    way = int(input("1:DFS or 2:BFS or 3:A++ : "))
    if way == 1:
        way = 0
    elif way == 2:
        way = -1
    maze = load_maze('maze')
    # print(maze)
    for i in maze:
        if "2" in i:
            x_start = maze.index(i)
            y_start = i.index("2")
    for i in maze:
        if "3" in i:
            x_end = maze.index(i)
            y_end = i.index("3")
    stack, maze = maze_solution_for_dfs_bfs(maze, x_start, y_start, x_end, y_end, way)
    way_back(stack, maze, x_start, y_start, x_end, y_end)
    # sleep(3)
    # os.system('cls')


run()
