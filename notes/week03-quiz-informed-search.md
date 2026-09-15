# CIS5210 Week 3 Quiz Notes · Informed Search

> Week 03 · Quiz Review

Source: user's Week 3 quiz summary.

这份笔记是给 Week 3 quiz 复习用的。核心问题是：

> Uninformed search 不知道哪个 frontier node 更接近 goal；informed search 用 heuristic function 给 frontier 排优先级。

主线：

```text
heuristic h(n)
-> Greedy best-first search: f(n) = h(n)
-> A* search: f(n) = g(n) + h(n)
-> admissible / consistent heuristics
-> dominance and relaxed problems
-> Manhattan distance for 8-puzzle
```

## 00 · Quick Review First

### Read With These Questions

1. [heuristic function `h(n)`](#01--heuristic-function) 估计的是哪一段 cost？
2. [`g(n)` 和 `h(n)`](#04--gn-is-actual-cost-so-far) 为什么不能混？`f(n)` 是怎么来的？
3. [Greedy best-first search](#02--greedy-best-first-search) 的 `f(n)` 是什么？它为什么可能 not optimal？
4. [A*](#03--a-search) 的 `f(n)` 是什么？它为什么比 greedy 更谨慎？
5. [admissible heuristic](#06--admissible-heuristic) 的不等式是什么？
6. [consistent heuristic 和 admissible heuristic](#08--consistency-vs-admissibility) 的关系是什么？
7. [dominant heuristic](#10--dominant-heuristic) 为什么通常能减少 node expansions？
8. [relaxed problem](#11--relaxed-problem) 为什么能给出 lower bound？
9. [Manhattan distance](#12--manhattan-distance-for-the-8-puzzle) 在 8-puzzle 中怎么算？为什么比 misplaced tiles 更强？
10. 写 [A* 代码](#13--practical-a-implementation-idea) 时，priority queue 里存什么？visited / best-known cost 怎么处理？

### One-Minute Map

```text
estimate remaining cost
-> h(n)
-> Greedy: choose smallest h(n)
-> A*: choose smallest g(n) + h(n)
-> admissible / consistent heuristic
-> optimality guarantee and fewer expansions
```

一句话记忆：

> A* is UCS plus a safe estimate of the remaining cost.

### Professional Terms

| Term | 中文 | Quick Meaning |
| --- | --- | --- |
| Heuristic | 启发式 | rule of thumb / educated estimate |
| `g(n)` | 已走真实代价 | start 到 `n` 的 actual path cost |
| `h(n)` | 估计剩余代价 | `n` 到 goal 的 estimated cost |
| `f(n)` | 排序分数 | frontier priority value |
| Greedy Best-First Search | 贪心最佳优先 | `f(n)=h(n)` |
| A* Search | A 星搜索 | `f(n)=g(n)+h(n)` |
| Admissible | 可采纳 | never overestimates true remaining cost |
| Consistent | 一致 | obeys triangle inequality along every edge |
| Dominant Heuristic | 支配启发式 | always at least as informative while still admissible |
| Relaxed Problem | 放松问题 | remove constraints to compute a lower bound |
| Manhattan Distance | 曼哈顿距离 | row distance plus column distance |
| Priority Queue | 优先队列 | returns frontier node with best priority |
| Best Known Cost | 当前最优已知代价 | graph search 中记录到某 state 的 lowest `g` |
| Stale Entry | 过期队列项 | priority queue 里 cost 已被更好 path 超过的旧 entry |

---

## 01 · Heuristic Function

A heuristic function estimates the remaining cost from a state / node to a goal.

$$
h(n)=\text{estimated cost from node }n\text{ to the nearest goal}
$$

中文直觉：

> heuristic 是“还差多远”的估计，不是已经走了多远。

它用于 informed search，让 algorithm 可以判断：

```text
which frontier node looks more promising?
```

### Important Distinction

| Term | Meaning |
| --- | --- |
| Informed search | search strategy that uses extra problem-specific knowledge |
| Heuristic function | the function that provides the extra estimate |

不要混：

```text
informed search = algorithm family / strategy
heuristic = ranking signal
```

---

## 02 · Greedy Best-First Search

Greedy best-first search chooses the node with the smallest heuristic value.

$$
f(n)=h(n)
$$

It ignores the cost already spent to reach the current node.

Memory:

```text
Greedy = only looks forward
```

中文解释：

> Greedy 只问“现在看起来离 goal 最近的是谁？”，不问“为了走到这里已经花了多少 cost？”

这可能让它很快，但不保证 optimal。

Example risk:

```text
Node A: already spent cost 100, h=1
Node B: already spent cost 2, h=5
```

Greedy prefers A because `h(A) < h(B)`，但 A 的 total path 可能更差。

---

## 03 · A* Search

A* combines:

- actual path cost so far；
- estimated remaining cost。

The evaluation function is:

$$
f(n)=g(n)+h(n)
$$

where:

| Symbol | Meaning |
| --- | --- |
| $g(n)$ | actual cost from start to node $n$ |
| $h(n)$ | estimated cost from node $n$ to a goal |
| $f(n)$ | estimated total cost of a solution path through $n$ |

中文直觉：

```text
g(n) = past cost
h(n) = future estimate
f(n) = estimated total cost
```

A* expands the node with the smallest $f(n)$.

### Example

If:

| Node | $g(n)$ | $h(n)$ | $f(n)=g(n)+h(n)$ |
| --- | ---: | ---: | ---: |
| A | 4 | 1 | 5 |
| B | 9 | 5 | 14 |
| C | 15 | 1 | 16 |
| D | 11 | 5 | 16 |

A* expands A next because it has the smallest $f(n)$.

---

## 04 · `g(n)` Is Actual Cost So Far

$g(n)$ is the actual path cost from the start node to node $n$.

Example:

```text
Start --3--> A --4--> B
```

Then:

$$
g(A)=3
$$

$$
g(B)=3+4=7
$$

Do not confuse:

```text
g(n) = actual cost so far
h(n) = estimated cost remaining
f(n) = estimated total cost
```

Quiz trap:

> If a question gives path edge costs already traveled, that belongs to `g(n)`, not `h(n)`.

---

## 05 · Greedy vs A*

The most important contrast:

| Algorithm | Formula | What It Asks |
| --- | --- | --- |
| Greedy best-first search | $f(n)=h(n)$ | Which node looks closest to the goal? |
| A* search | $f(n)=g(n)+h(n)$ | Which node gives the best estimated total path cost? |

Greedy:

```text
future estimate only
```

A*:

```text
past cost + future estimate
```

中文一句话：

> Greedy 看“前面还剩多少”；A* 同时看“已经花了多少”和“估计还剩多少”。

---

## 06 · Admissible Heuristic

A heuristic is admissible if it never overestimates the true remaining cost.

$$
h(n)\le h^*(n)
$$

where:

$$
h^*(n)=\text{true optimal cost from }n\text{ to the goal}
$$

So admissibility means:

```text
heuristic estimate <= true remaining cost
```

Memory trick:

```text
Admissible = optimistic
```

It may underestimate, but it should not overestimate.

Why this matters:

> If the heuristic overestimates, A* may wrongly avoid a path that is actually optimal.

---

## 07 · Consistent Heuristic

A heuristic is consistent if it satisfies a triangle-inequality-like condition.

For an edge from $n$ to $n'$ with cost $c(n,n')$:

$$
h(n)\le c(n,n')+h(n')
$$

中文直觉：

> 走一步之后，heuristic 不能突然下降得超过这一步的真实 cost。

Equivalent intuition:

```text
estimated distance from n to goal
<=
cost from n to n' + estimated distance from n' to goal
```

This is like saying:

> Going through a neighbor should not make the heuristic violate the triangle inequality.

---

## 08 · Consistency vs Admissibility

Key relationship:

$$
\boxed{\text{consistent} \Rightarrow \text{admissible}}
$$

But:

$$
\boxed{\text{admissible} \nRightarrow \text{consistent}}
$$

So consistency is stronger.

Quiz wording:

```text
Every consistent heuristic is admissible.
Not every admissible heuristic is consistent.
```

Why consistency matters for graph search:

> In graph search, states can be revisited through different paths. Consistency helps preserve the standard optimality guarantee without needing messy reopen behavior.

---

## 09 · A* Optimality

For tree search:

> A* is optimal with an admissible heuristic.

For graph search:

> A* generally requires a consistent heuristic for the standard optimality guarantee.

Important:

```text
tree search:
    no repeated-state merging
    admissible is enough

graph search:
    repeated states / visited set matter
    consistency is the safer standard condition
```

This is why quizzes often ask whether the setting is tree search or graph search.

---

## 10 · Dominant Heuristic

Suppose $h_1$ and $h_2$ are both admissible.

$h_1$ dominates $h_2$ if:

$$
h_1(n)\ge h_2(n)
$$

for every node $n$.

Because both are admissible, the larger estimate is usually more informative.

### Important Condition

Dominance must hold at all nodes.

Example:

| Node | $h_1$ | $h_2$ |
| --- | ---: | ---: |
| A | 10 | 2 |
| B | 4 | 8 |
| C | 6 | 2 |
| D | 3 | 4 |
| E | 4 | 1 |

Here:

```text
h1 > h2 at A, C, E
h2 > h1 at B, D
```

Therefore:

> Neither heuristic dominates the other.

Common mistake:

> “h1 is larger most of the time” is not dominance. It must be larger or equal everywhere.

---

## 11 · Relaxed Problem

A relaxed problem is a simpler version of the original problem where one or more constraints are removed.

Its optimal solution cost can be used as an admissible heuristic for the original problem.

Idea:

```text
original problem
-> remove constraints
-> easier relaxed problem
-> optimal relaxed cost
-> heuristic estimate
```

Why admissible?

```text
relaxed problem is easier
-> optimal relaxed cost cannot be larger than original optimal cost
-> heuristic does not overestimate
```

中文直觉：

> 放宽规则后，解题不会更难，所以 relaxed solution cost 是真实 cost 的下界。

---

## 12 · Manhattan Distance for the 8-Puzzle

For the 8-puzzle, Manhattan distance is a common heuristic.

For each numbered tile:

$$
\text{distance}
= |\text{current row}-\text{goal row}|
+ |\text{current col}-\text{goal col}|
$$

Then add the distances for all numbered tiles.

The blank tile is not counted.

Why not count the blank?

> The goal is about placing numbered tiles correctly; the blank is a space that enables movement, not a numbered tile that must contribute to the sum.

### Quiz Example

Goal:

```text
1 2 3
4 5 6
7 8 _
```

Current:

```text
1 8 6
3 5 2
_ 4 7
```

Tile distances:

| Tile | Manhattan distance |
| --- | ---: |
| 1 | 0 |
| 2 | 2 |
| 3 | 3 |
| 4 | 2 |
| 5 | 0 |
| 6 | 1 |
| 7 | 2 |
| 8 | 2 |

Total:

$$
h(n)=0+2+3+2+0+1+2+2=12
$$

So the Manhattan heuristic for this state is:

```text
12
```

---

## 13 · Practical A* Implementation Idea

A typical A* implementation uses a priority queue.

The priority is:

$$
f = g + h
$$

A useful queue item:

```python
(priority_f, current_g, node, path)
```

Conceptual algorithm:

```text
1. Put start in the priority queue.
2. Pop the node with smallest f.
3. If it is the goal, return the path.
4. For each neighbor:
       new_g = current_g + edge_cost
5. If this is a better path to the neighbor:
       update best known g
       push neighbor with priority new_g + h(neighbor)
```

Important implementation ideas:

- `h` may be stored as a dictionary lookup.
- weighted graph edges have costs.
- track the best known `g` value for each node.
- stale, worse queue entries can be skipped.

Why track best known `g`?

> The same state may be reached by multiple paths. A* should keep the cheaper path so far.

---

## 14 · Terms Summary

| Term | Meaning |
| --- | --- |
| Heuristic function | estimates remaining cost to goal |
| Greedy best-first search | expands smallest $h(n)$ |
| $g(n)$ | actual cost from start to current node |
| A* | expands smallest $g(n)+h(n)$ |
| Admissible heuristic | never overestimates true remaining cost |
| Consistent heuristic | satisfies $h(n)\le c(n,n')+h(n')$ |
| Dominant heuristic | larger than another admissible heuristic at every node |
| Relaxed problem | easier problem used to build admissible heuristics |
| Manhattan distance | sum of row/column tile distances |

---

## 15 · Core Week 3 Takeaways

```text
Heuristic h(n)
= estimate from current node to goal

Greedy
= h(n)

A*
= g(n) + h(n)

g(n)
= real cost from start

Admissible
= never overestimates

Consistent
= triangle-inequality-like condition

consistent => admissible

Dominance
= one admissible heuristic is >= another at every node

Manhattan distance
= sum of row/column distance for every numbered tile
```

---

## 16 · Quick Self-Test

1. What is the difference between $g(n)$ and $h(n)$?
2. Why does Greedy best-first search only use $h(n)$?
3. What formula does A* use?
4. What does admissible mean?
5. What does consistent mean?
6. Why is consistency stronger than admissibility?
7. What does it mean for one heuristic to dominate another?
8. If $h_1$ is larger at some nodes but smaller at others, does it dominate?
9. How is Manhattan distance computed in the 8-puzzle?
10. Why is the blank tile ignored in the Manhattan sum?
11. What is a relaxed problem?
12. Why can a relaxed problem produce an admissible heuristic?
13. Why does A* use a priority queue?
14. Why should A* track the best known $g$ for each node?

---

## 17 · One Sentence

$$
\boxed{
\text{Week 3 quiz 的核心是：heuristic } h(n) \text{ 给 search 排优先级，Greedy 只看未来估计，A* 用 } g(n)+h(n) \text{ 平衡已付成本和剩余估计。}
}
$$
