import copy
import heapq


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def compute_h(state):
    h_val = 0
    puzzle = []
    for row in range(3):
        for col in range(3):
            puzzle.append([row, col])
    for tile in range(9):
        if state[tile] != 0:
            if state[tile] % 3 == 0:
                row = state[tile] // 3 - 1
                col = state[tile] % 3 + 2
            else:
                row = state[tile] // 3
                col = state[tile] % 3 - 1
            h_val += manhattan(puzzle[tile], [row, col])
    return h_val


def success(updated_puzzle):
    output = []
    for row in range(3):
        for col in range(3):
            output.append(updated_puzzle[row][col])
    return output


def successor_state(state):
    puzzle = [state[0:3], state[3:6], state[6:9]]
    for row in range(3):
        for col in range(3):
            if puzzle[row][col] == 0:
                empty_row = row
                empty_col = col
    successors = []
    if empty_row != 0:
        move_up = copy.deepcopy(puzzle)
        move_up[empty_row][empty_col] = move_up[empty_row - 1][empty_col]
        move_up[empty_row - 1][empty_col] = 0
        successors.append(success(move_up))
    if empty_row != 2:
        move_down = copy.deepcopy(puzzle)
        move_down[empty_row][empty_col] = move_down[empty_row + 1][empty_col]
        move_down[empty_row + 1][empty_col] = 0
        successors.append(success(move_down))
    if empty_col != 0:
        move_left = copy.deepcopy(puzzle)
        move_left[empty_row][empty_col] = move_left[empty_row][empty_col - 1]
        move_left[empty_row][empty_col - 1] = 0
        successors.append(success(move_left))
    if empty_col != 2:
        move_right = copy.deepcopy(puzzle)
        move_right[empty_row][empty_col] = move_right[empty_row][empty_col + 1]
        move_right[empty_row][empty_col + 1] = 0
        successors.append(success(move_right))
    return sorted(successors)


def print_succ(state):
    successors = successor_state(state)
    for i in range(len(successors)):
        h = compute_h(successors[i])
        print(successors[i], 'h={}'.format(h))
    return


def print_solution(state, path):
    solution = []
    solution.insert(0, state)
    parent = path[str(state)]
    while parent != -1:
        solution.insert(0, parent)
        parent = path[str(parent)]

    moves = 0
    for step in solution:
        board = str(step)[0:9] + "\n" + str(step)[9:18] + "\n" + str(step)[18:27]
        print(' Move: {}'.format(moves))
        print(board)
        moves += 1


def solve(state):
    open = []
    closed = {}
    h = compute_h(state)
    g = 0
    heapq.heappush(open, (g + h, state, (g, h, -1)))
    if len(open) == 0:
        return
    else:
        while True:
            pop = heapq.heappop(open)
            if str(pop[1]) in closed:
                continue
            closed[str(pop[1])] = pop[2][2]
            if pop[2][1] == 0:
                print_solution(pop[1], closed)
                return
            successors = successor_state(pop[1])
            g += 1
            for succ in successors:
                if str(succ) in closed:
                    continue
                h_succ = compute_h(succ)
                f = g + h_succ
                heapq.heappush(open, (f, succ, (g, h_succ, pop[1])))
