"""
    Breadth First Search
"""
from collections import deque

class BFS:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.current_state = start_state
        self.goal_state = goal_state
        self.max_search_depth = 0
        self.queue = deque([(start_state, 0)])

    def _expand_current_node(self, current_depth=0):
        children = self.current_state.expand()
        for child in children:
            self.max_search_depth = max(self.max_search_depth, current_depth+1)
            self.queue.append((child, current_depth+1))

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

        visited_nodes = set()
        search_depth = 0
        goal_found = False
        nodes_expanded = 0
        while self.queue:
            current_state, current_depth = self.queue.popleft()
            if current_state.config not in visited_nodes:
                nodes_expanded += 1
                self.current_state = current_state
                if self.is_goal():
                    search_depth = current_depth
                    goal_found = True
                    break
                visited_nodes.add(current_state.config)
                self._expand_current_node(current_depth=current_depth)

        self.queue.clear() # Empty the Queue
        path_to_goal = self._path_to_goal(display=display_path)


        if not goal_found:
            return False, [], -1, nodes_expanded
        return True, path_to_goal, self.current_state.cost, nodes_expanded-1, search_depth, self.max_search_depth
