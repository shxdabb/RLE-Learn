from typing import List, Tuple

class GridWorldEnv:
    """Simple GridWorld environment for teaching reinforcement learning basics."""

    ACTIONS = ["up", "down", "left", "right"]

    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        start: Tuple[int, int] = (0, 0),
        goal: Tuple[int, int] = (4, 4),
        obstacles: List[Tuple[int, int]] = None,
    ):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.obstacles = obstacles or [(1, 1), (2, 2), (3, 1)]

        self.grid: List[List[str]] = []
        self.agent_pos = (0, 0)
        self.done = False
        self.reset()

    def reset(self) -> Tuple[int, int]:
        """Reset the environment to the initial state and return the start state."""
        self.grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        self.agent_pos = self.start
        self.done = False

        self.grid[self.start[1]][self.start[0]] = "S"
        self.grid[self.goal[1]][self.goal[0]] = "G"

        for obstacle in self.obstacles:
            if obstacle != self.start and obstacle != self.goal:
                self.grid[obstacle[1]][obstacle[0]] = "#"

        return self.agent_pos

    def step(self, action: int) -> Tuple[Tuple[int, int], int, bool]:
        """Apply an action and return (next_state, reward, done)."""
        if self.done:
            raise ValueError("Episode has ended. Call reset() before step().")

        if action < 0 or action >= len(self.ACTIONS):
            return self.agent_pos, -10, False

        move = self.ACTIONS[action]
        next_pos = self._apply_move(move)

        if not self._within_bounds(next_pos):
            return self.agent_pos, -10, False

        if next_pos in self.obstacles:
            return self.agent_pos, -10, False

        self.agent_pos = next_pos

        if self.agent_pos == self.goal:
            self.done = True
            return self.agent_pos, 10, True

        return self.agent_pos, -1, False

    def _apply_move(self, move: str) -> Tuple[int, int]:
        x, y = self.agent_pos
        if move == "up":
            return x, y - 1
        if move == "down":
            return x, y + 1
        if move == "left":
            return x - 1, y
        if move == "right":
            return x + 1, y
        return x, y

    def _within_bounds(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self) -> None:
        """Print the current grid with the agent position."""
        display_grid = [row[:] for row in self.grid]
        x, y = self.agent_pos

        display_grid[y][x] = "A"

        for row in display_grid:
            print(" ".join(row))
        print()

    def is_terminal(self) -> bool:
        """Return True when the goal state has been reached."""
        return self.done


if __name__ == "__main__":
    env = GridWorldEnv()
    env.reset()
    print("Initial GridWorld:")
    env.render()

    sample_actions = [3, 3, 1, 1, 3, 1, 3]
    for action in sample_actions:
        state, reward, done = env.step(action)
        print(f"Action={GridWorldEnv.ACTIONS[action]}, State={state}, Reward={reward}, Done={done}")
        env.render()
        if done:
            break
