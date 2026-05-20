import random
import sys
from pathlib import Path
from typing import Dict, Tuple

# Ensure the project root is available when running this file directly.
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from env.gridworld import GridWorldEnv

State = Tuple[int, int]
Action = int


class QLearningAgent:
    """A simple Q-learning agent for the GridWorld environment."""

    def __init__(self, env: GridWorldEnv, alpha: float = 0.1, gamma: float = 0.99, epsilon: float = 0.2):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table: Dict[State, Dict[Action, float]] = {}

    def _ensure_state(self, state: State) -> None:
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in range(len(self.env.ACTIONS))}

    def choose_action(self, state: State) -> Action:
        self._ensure_state(state)
        if random.random() < self.epsilon:
            return random.choice(list(self.q_table[state].keys()))
        return max(self.q_table[state], key=self.q_table[state].get)

    def update(self, state: State, action: Action, reward: float, next_state: State) -> None:
        self._ensure_state(state)
        self._ensure_state(next_state)

        current_q = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())
        self.q_table[state][action] = current_q + self.alpha * (reward + self.gamma * next_max - current_q)

    def train(self, episodes: int = 100, max_steps: int = 100) -> None:
        for episode in range(1, episodes + 1):
            state = self.env.reset()
            total_reward = 0

            for _ in range(max_steps):
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update(state, action, reward, next_state)

                state = next_state
                total_reward += reward

                if done:
                    break

            if episode % 10 == 0 or episode == 1:
                print(f"Episode {episode}/{episodes} - Total Reward: {total_reward}")

    def run_episode(self, max_steps: int = 50) -> None:
        state = self.env.reset()
        self.env.render()

        for _ in range(max_steps):
            action = self.choose_action(state)
            state, reward, done = self.env.step(action)
            self.env.render()
            print(f"Action={self.env.ACTIONS[action]}, Reward={reward}, Done={done}\n")
            if done:
                break


if __name__ == "__main__":
    env = GridWorldEnv()
    agent = QLearningAgent(env)

    print("Training Q-learning agent...")
    agent.train(episodes=100)

    print("Running a learned episode:")
    agent.run_episode()
