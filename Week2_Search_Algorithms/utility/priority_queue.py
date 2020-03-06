
from heapq import heappush, heappop


class PriorityQueue:

    # Min Heap

    def __init__(self):
        self._queue = []
        self._index = 0

    def empty(self):
        return len(self._queue) == 0

    def push(self, key, priority):
        heappush(self._queue, (priority, self._index, key))
        self._index += 1

    def pop(self):
        return heappop(self._queue)

    def clear(self):
        self._queue.clear()
