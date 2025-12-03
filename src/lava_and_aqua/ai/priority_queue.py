import heapq


class PriorityQueue:
    def __init__(self, items=()):
        self._heap = []
        for item in items:
            self.add(item)

    def add(self, items):
        heapq.heappush(self._heap, items)

    def pop(self):
        if not self._heap:
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self._heap)

    def top(self):
        if not self._heap:
            raise IndexError("peek from an empty priority queue")
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return bool(self._heap)
