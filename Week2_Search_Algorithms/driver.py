import sys
import time
from resource import getrusage, RUSAGE_SELF
import math

from utility.bfs import BFS
from utility.dfs import DFS
from utility.a_star import AStar
from utility.priority_queue import PriorityQueue


# The Class that Represents the Puzzle
class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):

        for i in range(self.n):
            line = []
            offset = i * self.n

            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):

        if self.blank_col == 0:
            return None

        blank_index = self.blank_row * self.n + self.blank_col
        target = blank_index - 1
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = (new_config[target],
                                                       new_config[blank_index])
        return PuzzleState(tuple(new_config), self.n, parent=self,
                           action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:
            return None

        blank_index = self.blank_row * self.n + self.blank_col
        target = blank_index + 1
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = (new_config[target],
                                                       new_config[blank_index])
        return PuzzleState(tuple(new_config), self.n, parent=self,
                           action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:
            return None

        blank_index = self.blank_row * self.n + self.blank_col
        target = blank_index - self.n
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = (new_config[target],
                                                       new_config[blank_index])
        return PuzzleState(tuple(new_config), self.n, parent=self,
                           action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:
            return None

        blank_index = self.blank_row * self.n + self.blank_col
        target = blank_index + self.n
        new_config = list(self.config)
        new_config[blank_index], new_config[target] = (new_config[target],
                                                       new_config[blank_index])
        return PuzzleState(tuple(new_config), self.n, parent=self,
                           action="Down", cost=self.cost + 1)

    def expand(self, change_order=False):
        """expand the node"""

        # add child nodes in order of ULDR
        if not change_order:
            if len(self.children) == 0:

                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)

                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
<<<<<<< HEAD

                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)

                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)

        else:
            if len(self.children) == 0:

                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)

                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)

                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)

=======

                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)

                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)

        else:
            if len(self.children) == 0:

                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)

                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)

                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)

>>>>>>> f61247b... Added an optimal order of expansion to PuzzleState.expand method, Refactored the bfs_search method and Added dfs_search method definition
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)

        return self.children

# Function that Writes to output.txt
# Students need to change the method to have the corresponding parameters
def writeOutput(file_prefix='', print_output=False, **kwargs):
    # Student Code Goes here
    output_lines = []
    output_lines.append(f'path_to_goal: {kwargs.get("path_to_goal", [])}')
    output_lines.append(f'cost_of_path: {kwargs.get("cost_of_path", 0)}')
    output_lines.append(f'nodes_expanded: {kwargs.get("nodes_expanded", 0)}')
    output_lines.append(f'search_depth: {kwargs.get("search_depth", 0)}')
    output_lines.append(f'max_search_depth: {kwargs.get("max_search_depth", 0)}')
    output_lines.append(f'running_time: {kwargs.get("running_time", float("Inf"))}')
    output_lines.append(f'max_ram_usage: {kwargs.get("max_ram_usage", float("Inf"))}')

    filename = f"{file_prefix}_output.txt" if file_prefix else "output.txt"

    with open(filename, 'w') as output_file:
        output_file.writelines('\n'.join(output_lines) + "\n")

    if print_output:
        print(f'Path to Goal: {kwargs.get("path_to_goal", [])}')
        print(f'Cost of Path: {kwargs.get("cost_of_path", 0)}')
        print(f'Nodes Expanded: {kwargs.get("nodes_expanded", 0)}')
        print(f'Search Depth: {kwargs.get("search_depth", 0)}')
        print(f'Max Search Depth: {kwargs.get("max_search_depth", 0)}')
        print(f'Running Time: {kwargs.get("running_time", float("Inf"))}')
        print(f'Max RAM Usage: {kwargs.get("max_ram_usage", float("Inf"))}')


def bfs_search(initial_state):
    """BFS search"""

    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    start_time = time.time()

    start_ram_usage = getrusage(RUSAGE_SELF).ru_maxrss
    bfs_tree = BFS(initial_state=initial_state,
                   goal_state=goal_state,
                   start_ram_usage=start_ram_usage)

    (goal_found, path_to_goal,
     path_cost, nodes_expanded,
     search_depth) = bfs_tree.search(display_path=False)

    running_time = time.time() - start_time
    max_search_depth = bfs_tree.get_max_search_depth()
    max_ram_usage = bfs_tree.get_max_ram_usage()/1024

    if not goal_found:
        print('Puzzle is not solvable')
        return

    writeOutput(file_prefix='',
                path_to_goal=path_to_goal,
                cost_of_path=path_cost,
                nodes_expanded=nodes_expanded,
                search_depth=search_depth,
                max_search_depth=max_search_depth,
                running_time=running_time,
                max_ram_usage=max_ram_usage)


def dfs_search(initial_state):
    """DFS search"""

    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    start_time = time.time()

<<<<<<< HEAD
=======
    ### STUDENT CODE GOES HERE ###
>>>>>>> f61247b... Added an optimal order of expansion to PuzzleState.expand method, Refactored the bfs_search method and Added dfs_search method definition
    start_ram_usage = getrusage(RUSAGE_SELF).ru_maxrss
    dfs_tree = DFS(initial_state=initial_state,
                   goal_state=goal_state,
                   start_ram_usage=start_ram_usage)

<<<<<<< HEAD
    (goal_found, path_to_goal,
     path_cost, nodes_expanded,
     search_depth) = dfs_tree.search(display_path=False)
=======
    goal_found, path_to_goal, \
    path_cost, nodes_expanded, \
    search_depth = dfs_tree.search(display_path=False)
>>>>>>> f61247b... Added an optimal order of expansion to PuzzleState.expand method, Refactored the bfs_search method and Added dfs_search method definition

    running_time = time.time() - start_time
    max_search_depth = dfs_tree.get_max_search_depth()
    max_ram_usage = dfs_tree.get_max_ram_usage()/1024

    if not goal_found:
        print('Puzzle is not solvable')
        return

    writeOutput(file_prefix='',
                path_to_goal=path_to_goal,
                cost_of_path=path_cost,
                nodes_expanded=nodes_expanded,
                search_depth=search_depth,
                max_search_depth=max_search_depth,
                running_time=running_time,
                max_ram_usage=max_ram_usage)


def A_star_search(initial_state):
    """A * search"""

    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    start_time = time.time()

    start_ram_usage = getrusage(RUSAGE_SELF).ru_maxrss
    astar_tree = AStar(initial_state=initial_state,
                       goal_state=goal_state,
                       start_ram_usage=start_ram_usage)

    (goal_found, path_to_goal,
     path_cost, nodes_expanded,
     search_depth) = astar_tree.search(display_path=False)

    running_time = time.time() - start_time
    max_search_depth = astar_tree.get_max_search_depth()
    max_ram_usage = astar_tree.get_max_ram_usage()/1024

    if not goal_found:
        print('Puzzle is not solvable')
        return

    writeOutput(file_prefix='',
                path_to_goal=path_to_goal,
                cost_of_path=path_cost,
                nodes_expanded=nodes_expanded,
                search_depth=search_depth,
                max_search_depth=max_search_depth,
                running_time=running_time,
                max_ram_usage=max_ram_usage)


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    raise NotImplementedError("{}".format(__name__))


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    raise NotImplementedError("{}".format(__name__))


def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    raise NotImplementedError("{}".format(__name__))


# Main Function that reads in Input and Runs corresponding Algorithm
def main():

    if len(sys.argv) < 3:
        print()
        exit(1)

    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":
        bfs_search(hard_state)

    elif sm == "dfs":
        dfs_search(hard_state)

    elif sm == "ast":
        A_star_search(hard_state)

    else:
        print("Enter valid command arguments !")


if __name__ == '__main__':
    main()
