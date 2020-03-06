
from collections import deque
from resource import getrusage, RUSAGE_SELF


class UninformedSearch:

    __slots__ = ('intial_state', 'goal_state', 'start_ram_usage',
                 'nodes_expanded', 'max_ram_usage', 'max_search_depth',
                 'visited_nodes', 'unexplored_nodes', 'current_state')

    def __init__(self, intial_state, goal_state, start_ram_usage=0):
        self.initial_state = intial_state
        self.goal_state = goal_state
        self.start_ram_usage = start_ram_usage
        self.nodes_expanded = 0
        self.max_ram_usage = 0
        self.max_search_depth = 0
        self.visited_nodes = set()
        self.current_state = self.initial_state
        self.unexplored_nodes = deque([(self.initial_state, 0)])

    def _expand_current_node(self, current_depth=0, reversed=False):
        children = self.current_state.expand()

        if reversed:
            children.reverse()  # Reverse children in-place

        # Iterating the children keeps expanding the graph size in RAM
        self.nodes_expanded += 1
        for child in children:
            if tuple(child.config) not in self.visited_nodes:
                self.visited_nodes.add(tuple(child.config))
                self.max_search_depth = max(self.max_search_depth,
                                            current_depth+1)
                self.unexplored_nodes.append((child, current_depth + 1))
                _ram_usage = getrusage(RUSAGE_SELF).ru_maxrss
                current_ram_usage = _ram_usage - self.start_ram_usage
                self.max_ram_usage = max(self.max_ram_usage, current_ram_usage)

    def is_goal(self):
        return self.current_state.config == self.goal_state

    def _path_to_goal(self, display=False):
        actions_to_goal = [self.current_state.action]
        path_to_goal = [self.current_state]
        parent_node = self.current_state.parent
        while parent_node.parent:
            actions_to_goal.append(parent_node.action)
            path_to_goal.append(parent_node)
            parent_node = parent_node.parent

        if display:
            path_to_goal.reverse()
            print("Game Path: \n")
            for path in path_to_goal:
                path.display()
                print("\n")

        actions_to_goal.reverse()
        return actions_to_goal

    def get_max_ram_usage(self):
        return self.max_ram_usage

    def get_max_search_depth(self):
        return self.max_search_depth
