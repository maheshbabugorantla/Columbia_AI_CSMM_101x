"""
    Breadth First Search
"""
from utility.uninformed_search import UninformedSearch


class BFS(UninformedSearch):

    def __init__(self, initial_state, goal_state, start_ram_usage=0):
        super().__init__(initial_state, goal_state, start_ram_usage)

    def get_max_ram_usage(self):
        return self.max_ram_usage

    def get_max_search_depth(self):
        return self.max_search_depth

    def search(self, display_path=False):

        search_depth = 0
        goal_found = False

        while self.unexplored_nodes:
            current_state, current_depth = self.unexplored_nodes.popleft()
            self.current_state = current_state
            if self.is_goal():
                search_depth = current_depth
                goal_found = True
                break
            self._expand_current_node(current_depth=current_depth)
        self.unexplored_nodes.clear()  # Empty the Queue
        path_to_goal = self._path_to_goal(display=display_path)

        if not goal_found:
            return (False, [], self.current_state.cost,
                    self.nodes_expanded, search_depth)
        return (True, path_to_goal, self.current_state.cost,
                self.nodes_expanded-1, search_depth)
