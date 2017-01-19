#TODO: Find latency in frequent intervals.
from collections import deque
import time
from copy import deepcopy

class LagCompClass:
    def __init__(self):
        self.history = deque()
    def add_state(self, pos, mouse):
        self.history.append((time.time(), deepcopy(pos), deepcopy(mouse)))
    def remove_old_states(self):
        now = time.time()
        while len(self.history) > 0 and (now - self.history[0][0]) > 1:
            self.history.popleft()
    def get_approx_client_state(self):
        now = time.time()
        lag = 0.05 #Placeholder. Need to find latency from socketio
        then = now - lag
        state = min(self.history, key = lambda x: abs(x[0]-then))
        return state
