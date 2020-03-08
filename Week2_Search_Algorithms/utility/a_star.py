
"""
    A* Search
"""

from utility.priority_queue import PriorityQueue
from resource import getrusage, RUSAGE_SELF


class AStar:

    __slots__ = ('initial_state', 'goal_state', 'start_ram_usage',
                 'nodes_expanded', 'max_ram_usage', 'max_search_depth',
                 'visited_nodes', 'current_state', 'frontier', 'frontier_map')

    def __init__(self, initial_state, goal_state, start_ram_usage):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.start_ram_usage = start_ram_usage
        self.nodes_expanded = 0
        self.max_ram_usage = 0
        self.max_search_depth = 0
        self.visited_nodes = set()
        self.frontier_map = dict()
        self.current_state = self.initial_state
        self.frontier = PriorityQueue()

    def _get_target_tile_position(self, tile):

        _tile_positions = {
            '1': (0, 1),
            '2': (0, 2),
            '3': (1, 0),
            '4': (1, 1),
            '5': (1, 2),
            '6': (2, 0),
            '7': (2, 1),
            '8': (2, 2)
        }
        return _tile_positions.get(tile, (-1, -1))

    def _calc_manhattan_distance(self, idx, value, n):
        """
            Calculates manhattan distance of a tile
        """
        t_row, t_col = self._get_target_tile_position(value)
        row_moves = abs((idx // n) - t_row)
        col_moves = abs((idx % n) - t_col)
        return row_moves + col_moves

    def _get_heuristic_cost(self, state):

        h_cost = 0
        n = state.n

        for idx, value in enumerate(state.config):
            _m_cost = self._calc_manhattan_distance(idx, value, n)
            h_cost += _m_cost
        return h_cost

    def _get_total_cost(self, state):
        return state.cost + self._get_heuristic_cost(state)

    def _misplaced_tiles(self):
        """
            Heuristic Function 2
        """
        pass

    def _expand_current_node(self):

        children = self.current_state.expand(change_order=True)

        self.nodes_expanded += 1
        for child in children:
            child_config = tuple(child.config)
            if child_config not in self.visited_nodes and \
                child_config not in self.frontier_map:
                self.frontier_map[child_config] = child
                _cost = self._get_total_cost(child)
                self.frontier.push(child, _cost)
                self.max_search_depth = max(self.max_search_depth,
                                            child.cost)

            elif child_config in self.frontier_map:
                current_cost = self._get_total_cost(child)
                _child_state = self.frontier_map.get(child_config)
                previous_cost = self._get_total_cost(_child_state)
                if current_cost < previous_cost:
                    self.frontier.push(child, current_cost)

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

    def search(self, display_path=False):

        initial_cost = self._get_total_cost(self.initial_state)
        self.frontier.push(self.initial_state, initial_cost)
        current_config = tuple(self.initial_state.config)
        self.frontier_map[current_config] = self.initial_state

        goal_found = False
        search_depth = 0

        while not self.frontier.empty():
            self.current_state = self.frontier.pop()
            current_config = tuple(self.current_state.config)
            self.visited_nodes.add(current_config)
            if self.is_goal():
                search_depth = self.current_state.cost
                goal_found = True
                break
            self._expand_current_node()
        self.frontier.clear()
        path_to_goal = self._path_to_goal(display=display_path)

        if not goal_found:
            return (False, [], self.current_state.cost,
                    self.nodes_expanded, search_depth)
        return (True, path_to_goal, self.current_state.cost,
                self.nodes_expanded-1, search_depth)

    def get_max_ram_usage(self):
        return self.max_ram_usage

    def get_max_search_depth(self):
        return self.max_search_depth
