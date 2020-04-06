from itertools import chain

from BaseAI import BaseAI


class PlayerAI(BaseAI):

    __slots__ = ('_tiles', '_max_depth')

    def __init__(self):
        self._tiles = [2, 4]
        # http://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
        self._max_depth = 4

    def _terminal_test(self, grid=None):
        return not grid.canMove() or self._max_depth <= grid.depth

    def _maximize(self, grid=None, alpha=float('-Inf'), beta=float('Inf')):

        if self._terminal_test(grid):
            return (None, self._eval_function(grid))

        (max_child, max_utility) = (None, float('-Inf'))

        children = grid.getAvailableMoves()
        # for tile in self._tiles:
        for child in children:
            _grid = grid.clone()
            _grid.depth = grid.depth + 1
            _grid.move(child)
            (_, utility) = self._minimize(_grid, alpha=alpha, beta=beta)

            if utility > max_utility:
                (max_child, max_utility) = (child, utility)

            if beta <= max_utility:
                break
            alpha = max(max_utility, alpha)
        return (max_child, max_utility)

    def _minimize(self, grid, alpha=float('-Inf'), beta=float('Inf')):

        if self._terminal_test(grid):
            return (None, self._eval_function(grid))

        (min_child, min_utility) = (None, float('Inf'))

        children = grid.getAvailableCells()
        for tile in self._tiles:
            for child in children:
                _grid = grid.clone()
                _grid.depth = grid.depth + 1
                _grid.insertTile(child, tile)
                (_, utility) = self._maximize(_grid, alpha=alpha, beta=beta)

                if utility < min_utility:
                    (min_child, min_utility) = (_grid, utility)

                if min_utility <= alpha:
                    break
                beta = min(min_utility, beta)
        return (min_child, min_utility)

    def _eval_function(self, grid=None):
        # Simple strategy is to ensure higher number of empty cells after each move
        h1 = len(grid.getAvailableCells())/(grid.size**2)

        # Clustering Penalty
        penalty = 0
        total_sum = sum(chain.from_iterable(grid.map))
        # Adjacent cells are penalized heavily for being greater than current cell value
        for i in range(grid.size):
            for j in range(i, grid.size-1):
                penalty += abs(grid.map[i][j+1] - grid.map[i][j])

        for i in range(grid.size):
            for j in range(i, grid.size-1):
                penalty += abs(grid.map[j][i+1] - grid.map[j][i])

        h2 = penalty/(2*total_sum)
        return h1 - h2

    def getMove(self, grid=None):
        grid.depth = 0
        (move, _) = self._maximize(grid,
                                   alpha=float('-Inf'),
                                   beta=float('Inf'))

        return move
