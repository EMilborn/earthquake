#TODO: Find latency in frequent intervals.
from collections import deque
import time
from copy import deepcopy

class LagCompClass:
    def __init__(self):
        self.history = deque()
        self.latency = deque()


    def add_state(self, pos, mouse):
        self.history.append((time.time(), deepcopy(pos), deepcopy(mouse)))


    def remove_old_states(self):
        now = time.time()
        while len(self.history) > 0 and (now - self.history[0][0]) > 1:
            self.history.popleft()


    def get_approx_client_state(self):
        now = time.time()
        latency = self.get_avg_latency()
        then = now - latency/2
        print "LATENCY", latency
        state = min(self.history, key = lambda x: abs(x[0]-then))
        return state

    def add_latency(self, latency):
        now = time.time()
        while len(self.latency) > 0 and (now - self.latency[0][0]) > 2:
            self.latency.popleft()
        self.latency.append((time.time(), latency))


    def get_avg_latency(self):
        if len(self.latency) == 0:
            return 0
        return float(sum(self.latency))/len(self.latency)

