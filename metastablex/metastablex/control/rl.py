import numpy as np

class QLearningController:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.9):
        self.q = np.zeros((n_states, n_actions))
        self.alpha = alpha
        self.gamma = gamma

    def act(self, state):
        return np.argmax(self.q[state])

    def update(self, s, a, r, s_next):
        best_next = np.max(self.q[s_next])
        self.q[s, a] += self.alpha * (r + self.gamma * best_next - self.q[s, a])
