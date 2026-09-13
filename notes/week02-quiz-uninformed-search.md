# CIS5210 Week 2 Quiz Notes · Uninformed Search

> Week 02 · Quiz Review

Source: user's Week 2 quiz summary and Module 2 search notes.

这份笔记是给 quiz 复习用的，不是作业代码说明。重点是能在 quiz / oral review 里快速解释：

```text
search strategy
-> frontier order
-> completeness / optimality
-> time complexity
-> space complexity
```

---

## 01 · Search Evaluation Criteria

评价一个 search strategy，通常看四件事：

| Criterion | Question | 中文理解 |
| --- | --- | --- |
| Completeness | Will it find a solution if one exists? | 有解时是否保证能找到 |
| Optimality | Will it find a lowest-cost solution? | 找到的解是否保证总代价最低 |
| Time complexity | How many nodes may be generated? | 最坏情况下要生成多少节点 |
| Space complexity | How many nodes may be stored? | 最坏情况下要同时存多少节点 |

注意：

> optimality 不是“能不能找到一个解”，而是“找到的第一个解是不是最低 path cost 的解”。

---

## 02 · Important Symbols: `b / d / m / C*`

| Symbol | Meaning | Quiz wording |
| --- | --- | --- |
| `b` | maximum branching factor | 每个 node 最多有多少 successors |
| `d` | depth of the shallowest goal node | 最浅 goal node 的深度 |
| `m` | maximum depth / maximum path length | search space 里最长 path 的深度，可能是 infinite |
| `C*` | cost of the optimal solution | 最优解的 path cost |

容易混的点：

```text
d is about the shallowest goal.
m is about the deepest possible path.
C* is about cost, not depth.
```

如果 every step cost = 1，那么：

$$
C^* = d
$$

但如果 step costs 不一样，最浅的 solution 不一定 cost 最低。

---

## 03 · State Space and Frontier

### State Space

State space 是从 initial state 出发，通过合法 actions 能到达的所有 states。

```text
initial state
-> successors
-> successors of successors
-> all reachable states
```

State space 可能很大，也可能是 infinite。

### Frontier

Frontier 是：

> generated but not yet expanded nodes.

也就是已经发现、但还没有拿出来展开的边界。

不同 algorithm 的关键差别通常就是：

```text
Which frontier node should be expanded next?
```

| Frontier behavior | Algorithm |
| --- | --- |
| FIFO queue | BFS |
| LIFO stack | DFS |
| Priority queue | informed / cost-based search |

---

## 04 · Breadth-First Search

### Core Idea

BFS expands the shallowest unexpanded node first.

```text
depth 0
depth 1
depth 2
...
```

它是 level by level（按层）搜索。

### Completeness

BFS is complete if `b` is finite.

原因：

```text
finite branching factor
-> each level has finite nodes
-> BFS eventually reaches depth d
-> if a solution exists at depth d, BFS will find it
```

如果 `b` 是 infinite，某一层本身可能永远展开不完。

### Optimality

BFS is optimal if every action has the same cost.

尤其当每步 cost = 1 时：

```text
lowest depth
= fewest actions
= lowest path cost
```

但如果 cost 不一样，BFS 不保证 optimal。

Example:

```text
Path A: 1 step, cost 100
Path B: 3 steps, cost 3
```

BFS 可能先找到 Path A，但 Path B 才是 lower-cost solution。

---

## 05 · BFS Time and Space Complexity

**Time complexity:** `O(b^d)`

**Space complexity:** `O(b^d)`

BFS searches the tree **level by level**. Before it reaches the shallowest goal at depth `d`, it may explore about:

```text
1 + b + b^2 + ... + b^d
```

The largest term is `b^d`, so the time complexity is:

```text
O(b^d)
```

BFS also keeps many nodes in memory at the same time, especially the whole **frontier** of one level.

At depth `d`, the frontier can contain about:

```text
b^d
```

nodes, so the space complexity is also:

```text
O(b^d)
```

For this quiz-style problem:

```ini
b = 4
d = 10
m = 200
```

The maximum depth `m = 200` is not the main factor for BFS, because BFS finds the **shallowest goal** first.

So:

```text
Time:  O(4^10)
Space: O(4^10)
```

One-paragraph quiz answer:

> BFS has a **time complexity of `O(b^d)`** and a **space complexity of `O(b^d)`**. BFS explores the search tree level by level. Before reaching the shallowest goal at depth `d`, it may generate about `1 + b + b^2 + ... + b^d` nodes, and the largest term is `b^d`, so the time complexity is `O(b^d)`. BFS also stores many frontier nodes in memory at the same time, especially nodes at the deepest explored level, so the space complexity is also `O(b^d)`. In this problem, `b = 4` and `d = 10`. The maximum depth `m = 200` is not the main factor for BFS because BFS searches for the shallowest goal first.

---

## 06 · Depth-First Search

### Core Idea

DFS expands the deepest unexpanded node first.

```text
go down one branch
then backtrack
then try another branch
```

### Properties

| Property | DFS |
| --- | --- |
| Complete? | No, not in infinite-depth spaces or spaces with loops |
| Optimal? | No |
| Time | `O(b^m)` |
| Space | `O(bm)` |

Why time depends on `m`:

> DFS may go all the way down to the maximum depth before finding a solution.

Why space is better than BFS:

> DFS mainly stores the current path plus remaining siblings, not the whole breadth of the tree.

Common quiz sentence:

> DFS has lower space complexity than BFS, but it is not generally complete or optimal.

---

## 07 · Depth-Limited Search

Depth-limited search is DFS with a fixed depth limit `l`.

```text
if node.depth == l:
    do not expand successors
```

### Cases

| Case | Result |
| --- | --- |
| `l < d` | incomplete, because cutoff happens before the shallowest goal |
| `l = d` | can find a shallowest solution |
| `l > d` | may find a deeper solution first because DFS order still applies |

### Complexity

| Property | DLS |
| --- | --- |
| Time | `O(b^l)` |
| Space | `O(bl)` |

Main idea:

> DLS fixes DFS's infinite-depth problem only if the limit is chosen well.

---

## 08 · Iterative Deepening Search

Iterative deepening search repeatedly runs depth-limited search with increasing limits.

```text
for l = 0, 1, 2, 3, ...
    run depth-limited search with limit l
    if solution found:
        return it
```

### Why It Works

IDS searches shallow depths before deeper depths, like BFS:

```text
all depth 0 nodes
all depth 1 nodes
all depth 2 nodes
...
```

But each depth-limited search uses DFS-style memory.

So IDS combines:

```text
BFS completeness / unit-cost optimality
+ DFS low memory
```

### Complexity

| Property | IDS |
| --- | --- |
| Complete? | Yes, if `b` is finite and a finite-depth solution exists |
| Optimal? | Yes, if every action cost is 1 |
| Time | `O(b^d)` |
| Space | `O(bd)` |

### Why Repeating Shallow Nodes Is Still `O(b^d)`

If the shallowest goal is at depth `d`, IDS constructs roughly:

```text
d*b + (d-1)*b^2 + (d-2)*b^3 + ... + 1*b^d
```

The deepest level dominates the growth:

```text
b^d
```

So total time is still:

```text
O(b^d)
```

Quiz intuition:

> IDS repeats cheap shallow work to avoid BFS's expensive memory.

---

## 09 · BFS / DFS / IDS Space Comparison

| Algorithm | Space | Why |
| --- | --- | --- |
| BFS | `O(b^d)` | keeps a large frontier near depth `d` |
| DFS | `O(bm)` | stores current path and siblings down to max depth `m` |
| DLS | `O(bl)` | DFS memory capped by limit `l` |
| IDS | `O(bd)` | DFS memory capped by the current limit, stopping at `d` |

Takeaway:

```text
BFS: strong guarantees, bad memory
DFS: good memory, weak guarantees
IDS: BFS-like guarantees, DFS-like memory for unit-cost search
```

---

## 10 · Quick Self-Test

1. What does `b` mean?
2. What does `d` mean?
3. What does `m` mean?
4. What does `C*` mean?
5. Why is BFS complete when `b` is finite?
6. Why is BFS optimal only when step costs are equal?
7. Why does BFS time complexity use `d`, not `m`?
8. Why is BFS space complexity also `O(b^d)`?
9. Why is DFS not complete in an infinite-depth search space?
10. Why is DFS not optimal?
11. What happens in depth-limited search when `l < d`?
12. Why does IDS still have `O(b^d)` time even though it repeats work?
13. Which algorithm would you choose when memory is limited but you still want BFS-like guarantees for unit-cost search?

---

## 11 · One Sentence

$$
\boxed{
\text{Week 2 quiz 的核心是：看懂 frontier expansion order，并能用 } b,d,m,C^* \text{ 解释 BFS, DFS, DLS, IDS 的 guarantees 和 complexity。}
}
$$
