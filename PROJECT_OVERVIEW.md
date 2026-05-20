# Project Overview — RLE-Learn

This document describes the purpose of the repository and explains what each file and package does. It's intended to help a new developer understand the project layout, the responsibilities of each module, and how to run the small learning examples included here.

---

## Project purpose

RLE-Learn is a minimal educational repository that demonstrates a simple GridWorld environment and a beginner-friendly Q-learning agent. The goal is to provide compact, readable code that can be used to teach reinforcement learning (RL) basics: environment dynamics, agent action selection, Q-table updates, and a simple training loop.

## Recommended Python version

- Python 3.8 or newer

There are no external runtime dependencies in the current code (no third-party imports). A `requirements.txt` path exists in the workspace but is a directory placeholder — see the Files section.

## How to run the examples

- Run the environment demo (prints a sample run and renders the grid):

```bash
python3 env/gridworld.py
```

- Train the Q-learning agent and run a learned episode:

```bash
python3 agent/train.py
```

Both scripts are self-contained and add the project root to `sys.path` when executed directly so they work when launched from the repository root.

---

## Files and folders (detailed)

- **[context.md](context.md#L1-L200)**
  - Session notes and a short summary of recent work performed in the repository. It documents what was added (GridWorld env, Q-learning trainer) and useful quick-check commands used during development. This is a human-oriented note file, not used by code.

- **[README.md](README.md#L1-L50)**
  - Project top-level README. Currently contains minimal content and a placeholder; you may want to expand it with usage instructions or link to this PROJECT_OVERVIEW.md.

- **agent/**
  - `__init__.py` — (package marker) makes `agent` a Python package. Contains no runtime code other than a package comment.
  - `train.py` — Q-learning demo and the main agent implementation. Key points:
    - `QLearningAgent` class: Implements a simple tabular Q-learning agent using a dictionary-based Q-table keyed by state tuples (x, y).
      - `__init__(env, alpha=0.1, gamma=0.99, epsilon=0.2)`: sets learning rate, discount, exploration.
      - `_ensure_state(state)`: ensures the Q-table contains an entry for a state.
      - `choose_action(state)`: epsilon-greedy action selection (random action with probability `epsilon`, else greedy).
      - `update(state, action, reward, next_state)`: standard Q-learning update rule.
      - `train(episodes=100, max_steps=100)`: runs a training loop, printing progress every 10 episodes.
      - `run_episode(max_steps=50)`: runs a single episode using the current Q-table and renders each step.
    - At module run (`if __name__ == "__main__"`) the script creates a `GridWorldEnv`, trains for 100 episodes, then runs one learned episode and prints progress.

- **env/**
  - `__init__.py` — (package marker) makes `env` a Python package.
  - `gridworld.py` — The GridWorld environment implementation. Key items:
    - `GridWorldEnv` class: a compact, educational grid environment that models a 2D grid with start and goal cells and optional obstacles.
      - Class constant: `ACTIONS = ["up", "down", "left", "right"]` — integer indices map to these moves.
      - `__init__(width=5, height=5, start=(0,0), goal=(4,4), obstacles=None)`: sets grid shape, start/goal, and default obstacles.
      - `reset() -> (x, y)`: resets grid state and returns the starting coordinate.
      - `step(action:int) -> (next_state, reward:int, done:bool)`: applies an action index, checks bounds and obstacles, returns reward and terminal flag. Reward scheme used by the environment:
        - Reaching the goal: +10 and sets `done` True.
        - Valid step (not goal): -1.
        - Invalid action / out of bounds / obstacle: -10 (agent remains in place).
      - `_apply_move(move:str)`: returns the candidate next position for a given move string.
      - `_within_bounds(pos)`: bounds checking helper.
      - `render()`: prints a textual representation of the grid with markers: `S` start, `G` goal, `#` obstacles, `A` agent position.
      - `is_terminal()`: returns whether the current episode is done.
    - The file also includes a small demo under `if __name__ == "__main__"` which resets the env, renders it, and steps through a sample action sequence.

- **mcp_Server/**
  - `server.py` — Present in the tree but currently empty. This appears to be intended as a placeholder for a server implementation (possibly for an MCP server integration). You can implement server logic here later; at the moment it does not affect other code.

- **requirements.txt/**
  - Note: In this workspace the `requirements.txt` path is a directory (placeholder) rather than a pip-style file. There are currently no third-party dependencies required by the code. If you add external packages, replace this with a file listing packages (for example, `numpy`, `gym`, etc.).

- **sandbox/**
  - `Dockerfile` — Present but empty. A placeholder Dockerfile exists; you can add instructions to containerize the project (install Python, copy sources, run examples) if desired.


## Suggested next steps / improvements

- Convert the `requirements.txt` placeholder to a real `requirements.txt` when third-party libraries are added.
- Implement a minimal server in `mcp_Server/server.py` if you plan to expose the environment over a socket/HTTP API.
- Expand `README.md` with quick start commands and link to `PROJECT_OVERVIEW.md`.
- Add unit tests for `env/gridworld.py` and `agent/train.py` to demonstrate deterministic behavior for specific seeds.

---

If you'd like, I can also:
- add a link to this file in the top-level `README.md` (small patch), or
- create a `requirements.txt` file listing common RL packages (e.g. `numpy`) and update the Dockerfile with a minimal build.
