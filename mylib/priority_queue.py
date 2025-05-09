import heapq
from collections import deque
import itertools

class BiDirectionalPriorityQueue:

    def __init__(self):
        self._counter = itertools.count()
        self._min_heap = []      
        self._max_heap = []      
        self._deque = deque()    
        self._entry_finder = {}  

    def enqueue(self, item, priority):
        eid = next(self._counter)
        heapq.heappush(self._min_heap, (priority, eid, item, eid))
        heapq.heappush(self._max_heap, (-priority, eid, item, eid))
        self._deque.append((eid, item, eid))
        self._entry_finder[eid] = True

    def _pop_heap(self, heap, key_fn):
        while heap:
            prio, _, item, eid = heapq.heappop(heap)
            if self._entry_finder.pop(eid, False):
                return item, key_fn(prio)
        raise IndexError("pop from empty priority queue")

    def _peek_heap(self, heap, key_fn):
        for prio, _, item, eid in heap:
            if self._entry_finder.get(eid, False):
                return item, key_fn(prio)
        raise IndexError("peek from empty priority queue")

    def _pop_deque(self, left):
        while self._deque:
            eid, item, _ = self._deque[0] if left else self._deque[-1]
            if self._entry_finder.pop(eid, False):
                return item, None
            (self._deque.popleft() if left else self._deque.pop())
        raise IndexError("pop from empty queue")

    def _peek_deque(self, left):
        seq = self._deque if left else reversed(self._deque)
        for eid, item, _ in seq:
            if self._entry_finder.get(eid, False):
                return item, None
        raise IndexError("peek from empty queue")

    def dequeue(self, *, highest=False, lowest=False, oldest=False, newest=False):
        flags = [highest, lowest, oldest, newest]
        if sum(flags) != 1:
            raise ValueError("Exactly one flag must be True")
        if highest: return self._pop_heap(self._max_heap, lambda p: -p)
        if lowest:  return self._pop_heap(self._min_heap,  lambda p: p)
        if oldest:  return self._pop_deque(left=True)
        return self._pop_deque(left=False)

    def peek(self, *, highest=False, lowest=False, oldest=False, newest=False):
        flags = [highest, lowest, oldest, newest]
        if sum(flags) != 1:
            raise ValueError("Exactly one flag must be True")
        if highest: return self._peek_heap(self._max_heap, lambda p: -p)
        if lowest:  return self._peek_heap(self._min_heap,  lambda p: p)
        if oldest:  return self._peek_deque(left=True)
        return self._peek_deque(left=False)

    def __len__(self):
        return sum(self._entry_finder.values())