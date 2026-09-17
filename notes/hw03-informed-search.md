# Homework 3 · Informed Search

> Week 03 · Programming Assignment

Source: CIS5210 Homework 3 (`hw3/homework3.pdf`) and the completed `hw3/homework3.py`.

这份作业把 Week 3 的 informed search 变成代码：

```text
search problem
-> state representation
-> successor generation
-> path cost g(n)
-> heuristic h(n)
-> priority f(n) = g(n) + h(n)
```

核心不是背 A* 模板，而是知道：

> A* 的 correctness 取决于两件事：successor / cost 是否定义正确，以及 heuristic 是否不会 overestimate。

## 00 · Quick Review First

### Read With These Questions

1. Tile Puzzle 的 state 为什么要转成 tuple of tuples？ [[#Tile State Representation|答案]]
2. `perform_move("up")` 表示谁向上移动？tile 还是 empty tile？ [[#Tile Moves|答案]]
3. IDDFS 为什么可以用很少 memory 找到 shortest solution？ [[#IDDFS for Tile Puzzle|答案]]
4. Manhattan distance 为什么适合作为 sliding tile puzzle 的 heuristic？ [[#Manhattan Heuristic|答案]]
5. A* 中 `g(n)`、`h(n)`、`f(n)` 分别是什么？ [[#A Star for Tile Puzzle|答案]]
6. Grid Navigation 为什么用 Euclidean distance 而不是 Manhattan distance？ [[#Grid Navigation Heuristic|答案]]
7. diagonal move 的 cost 为什么是 `sqrt(2)`？ [[#Grid Successors and Costs|答案]]
8. Distinct Disks 的 goal state 为什么是 reversed order？ [[#Distinct Disk State|答案]]
9. Disk heuristic 为什么不能随便把多个 lower bound 相加？ [[#Distinct Disk Heuristic|答案]]
10. A* 的 `best_cost` table 防止了什么 bug？ [[#04 · Best Cost Table|答案]]

### One-Minute Map

```text
HW2 BFS:
    all edges cost 1
    frontier ordered by depth

HW3 A*:
    frontier ordered by g(n) + h(n)
    h(n) estimates remaining cost
    admissible h(n) keeps optimality
```

一句话记忆：

> HW3 is HW2 plus heuristics: the search state is still the foundation, but the frontier is now prioritized by estimated total cost.

### Professional Terms

| Term | 中文 | Quick Meaning |
| --- | --- | --- |
| IDDFS | 迭代加深 DFS | run depth-limited DFS with increasing limits |
| A* Search | A 星搜索 | priority search using `f(n)=g(n)+h(n)` |
| `g(n)` | 已付成本 | cost from start to node `n` |
| `h(n)` | 启发式估计 | estimated remaining cost to goal |
| `f(n)` | 评估值 | estimated total solution cost through `n` |
| Admissible Heuristic | 可采纳启发式 | never overestimates true remaining cost |
| Manhattan Distance | 曼哈顿距离 | `abs(dr)+abs(dc)` |
| Euclidean Distance | 欧几里得距离 | straight-line distance |
| Priority Queue | 优先队列 | pops the lowest-priority item first |
| Best-Cost Table | 最佳成本表 | records cheapest known `g(n)` for each state |

---

## 01 · Tile Puzzle

### Tile State Representation

The mutable board is a list of lists:

```python
[[1, 2, 3],
 [4, 5, 6],
 [7, 8, 0]]
```

For search, the same board is converted to a hashable state:

```python
((1, 2, 3),
 (4, 5, 6),
 (7, 8, 0))
```

Why:

- `set` and `dict` keys must be hashable;
- mutable lists can change after being inserted;
- immutable tuples make visited / best-cost logic reliable.

### Tile Moves

In this assignment, `perform_move(direction)` moves the **empty tile**.

```text
"up"    means empty tile swaps with the tile above it
"down"  means empty tile swaps with the tile below it
"left"  means empty tile swaps with the tile on the left
"right" means empty tile swaps with the tile on the right
```

If the empty tile is at the boundary and the move would leave the board, the move is invalid and returns `False`.

### IDDFS for Tile Puzzle

IDDFS combines DFS memory usage with BFS-like optimality for unit-cost problems:

```text
limit = 0
limit = 1
limit = 2
...
stop when any solution is found at the current limit
```

Why it returns a shortest move sequence:

- all tile moves cost 1;
- depth equals number of moves;
- the first depth that contains a goal is the optimal depth.

Why it uses less memory than BFS:

- DFS only stores the current path and recursion stack;
- BFS stores a whole frontier level.

### Manhattan Heuristic

For each numbered tile:

```text
distance = abs(current_row - goal_row) + abs(current_col - goal_col)
```

Then sum this over all non-empty tiles.

Why admissible:

- one move changes one tile's Manhattan distance by at most 1;
- every misplaced tile must eventually move toward its goal;
- ignoring collisions and board constraints can only make the estimate too small, not too large.

### A Star for Tile Puzzle

For Tile Puzzle:

```text
g(n) = number of moves already made
h(n) = Manhattan distance of the board
f(n) = g(n) + h(n)
```

The priority queue always expands the board with the smallest `f(n)`.

This is more focused than BFS:

```text
BFS: expand by depth only
A*:  expand by depth + estimated remaining work
```

---

## 02 · Grid Navigation

### Grid State

The grid is a 2D scene:

```text
False = free cell
True  = blocked cell
```

A state is a point:

```python
(row, col)
```

The path returned by `find_path` includes both the start and the goal:

```python
[(start_row, start_col), ..., (goal_row, goal_col)]
```

### Grid Successors and Costs

The agent may move in 8 directions:

```text
up, down, left, right
four diagonals
```

Costs:

```text
orthogonal move: 1
diagonal move: sqrt(2)
```

The diagonal cost is `sqrt(2)` because moving from `(r, c)` to `(r+1, c+1)` is the hypotenuse of a 1-by-1 right triangle.

### Grid Navigation Heuristic

Use Euclidean distance:

```text
h(point) = straight-line distance from point to goal
```

Why not Manhattan distance?

- Manhattan assumes only 4-direction movement;
- this assignment allows diagonal movement;
- Euclidean distance is the true lower bound when diagonal movement is possible.

Why admissible:

- obstacles can only make the actual path longer;
- no legal path can be shorter than the straight-line distance.

---

## 03 · Distinct Disk Movement

### Distinct Disk State

Use `-1` for empty slots and numbered disks for distinct disks.

For `length = 5`, `n = 3`:

```text
start: (0, 1, 2, -1, -1)
goal:  (-1, -1, 2, 1, 0)
```

The goal is reversed because the distinct disks must end on the opposite side in the opposite order.

### Disk Successors

Each disk can:

- slide one step into an adjacent empty slot;
- jump two steps over one occupied slot into an empty slot.

Legal jump:

```text
disk occupied empty
  A      B      _

A may jump over B into _
```

Illegal jump:

```text
disk empty empty
  A    _     _

A cannot jump over an empty slot
```

### Distinct Disk Heuristic

The implementation uses a conservative heuristic:

```text
h(state) = max(distance lower bound, inversion lower bound)
```

Distance lower bound:

```text
each disk can move at most 2 cells per move
so disk i needs at least ceil(distance_to_goal / 2) moves
```

Inversion lower bound:

```text
start order: 0, 1, 2, ...
goal order:  ..., 2, 1, 0
```

Every pair in the wrong relative order must be swapped by some jump. Since one jump can change at most one pair's relative order, the number of wrong-order pairs is also a lower bound.

Why use `max`, not sum?

The same jump can both move a disk closer and fix a relative-order pair. Adding the bounds could double-count the same required move and accidentally overestimate. Taking `max` preserves admissibility.

---

## 04 · Best Cost Table

In A*, `best_cost[state]` stores the cheapest known `g(n)` for each state.

It prevents two common bugs:

1. expanding the same state many times through worse paths;
2. throwing away a newly discovered better path to an already-seen state.

Pattern:

```python
if next_state not in best_cost or next_cost < best_cost[next_state]:
    best_cost[next_state] = next_cost
    push next_state into priority queue
```

This is the A* version of the `visited` set from BFS, but it is slightly more careful because weighted costs may produce a better path later.

---

## 05 · Common Mistakes

### Mistake 1 - Mutating a State Already in the Frontier

If a list board is put into a queue and later changed, the queued state silently changes too.

Fix:

```text
use deep copy for puzzle objects
use tuple states for search keys
```

### Mistake 2 - Treating Tile Move Direction Backwards

The direction names refer to the empty tile, not the numbered tile.

### Mistake 3 - Using Manhattan Distance for 8-Direction Grid Movement

Manhattan can overestimate when diagonals are allowed.

Example:

```text
from (0, 0) to (1, 1)
Manhattan = 2
true diagonal cost = sqrt(2)
```

That would break admissibility.

### Mistake 4 - Adding Multiple Disk Lower Bounds

Two lower bounds may measure overlapping work.

```text
safe: max(bound1, bound2)
risky: bound1 + bound2
```

### Mistake 5 - Forgetting That A* Needs Actual Step Costs

Grid navigation is not unit cost:

```text
orthogonal = 1
diagonal = sqrt(2)
```

So `g(n)` must accumulate real path cost, not just number of moves.

---

## 06 · Self-Check

1. Why does IDDFS find an optimal solution for Tile Puzzle when each move costs 1?
2. Explain Manhattan distance admissibility in one sentence.
3. Why is Euclidean distance admissible for grid navigation with obstacles?
4. Give an example where Manhattan distance would overestimate in an 8-direction grid.
5. What is the difference between a `visited` set and a `best_cost` table?
6. In distinct disks, why does reversing order require jumps?
7. Why is `max(lower_bound_1, lower_bound_2)` usually safer than adding lower bounds?

---

## 07 · One Sentence

HW3 uses A* to focus search with admissible heuristics: Manhattan distance for sliding tiles, Euclidean distance for grid navigation, and conservative disk lower bounds for distinct disk movement.
