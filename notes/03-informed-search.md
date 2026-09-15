# Informed Search

> Week 03 · Module 03

Source: `04-Informed-Search.pptx.pdf`, user's pasted Canvas transcripts for Uniform Cost Search, Greedy Best-First Search, A* Search, and A* optimality / applications.

This note treats the attached course materials as source material only. It records the lecture logic for learning and review.

## 00 · Quick Review First

### Read With These Questions

1. [BFS 假设 unit step cost](#02--from-unit-cost-to-weighted-cost) 时合理；edge cost 不同的时候为什么要换成 UCS？
2. [UCS 的 priority](#03--uniform-cost-search) 是什么？为什么它要在 [goal 被 popped / selected for expansion](#ucs-vs-bfs-goal-test-timing) 时才停止？
3. [`g(n)`、`h(n)`、`f(n)`](#key-symbols) 分别代表什么？
4. [heuristic function](#05--heuristic-functions) 为什么只是 estimate，不是 true cost？
5. [Greedy best-first search](#06--greedy-best-first-search) 为什么可能很快，但不保证 optimal？
6. [A* 为什么把 `g(n)` 和 `h(n)` 加起来](#why-a-is-less-reckless-than-greedy)，而不是只看其中一个？
7. [admissible heuristic](#08--admissible-heuristics) 的核心不等式是什么？为什么不能 [overestimate](#why-overestimating-is-dangerous)？
8. 如果 [`h(n)=0`](#14--best-and-worst-admissible-heuristics)，A* 退化成什么？
9. 如果 [`h(n)=h*(n)`](#14--best-and-worst-admissible-heuristics)，A* 为什么几乎拥有 perfect guidance？
10. [relaxed problem](#12--relaxed-problems) 为什么常常能产生 admissible heuristic？
11. [Manhattan distance](#manhattan-distance) 为什么比 misplaced tiles 更 informative？
12. [A* 可以用于哪些真实系统](#16--a-applications)？它的 guarantee 依赖哪些前提？

### One-Minute Map

```text
different edge costs
-> Uniform Cost Search: f(n) = g(n)
-> add goal-distance estimate h(n)
-> Greedy Best-First: f(n) = h(n)
-> combine past cost and future estimate
-> A*: f(n) = g(n) + h(n)
-> admissible heuristic
-> optimal solution first
```

一句话记忆：

> Greedy asks "which node looks closest now?"; A* asks "which complete path looks cheapest if this estimate is trustworthy?"

### Professional Terms

| Term | 中文 | Quick Meaning |
| --- | --- | --- |
| Uniform Cost Search (UCS) | 一致代价搜索 | 按 accumulated path cost `g(n)` 从小到大展开 |
| Path Cost `g(n)` | 已走代价 | start 到 node `n` 的真实累计 cost |
| Heuristic Function `h(n)` | 启发函数 | 从 `n` 到 goal 的 remaining cost estimate |
| True Cost `h*(n)` | 真实剩余代价 | 从 `n` 到 goal 的最优真实 cost |
| Evaluation Function `f(n)` | 评价函数 | priority queue 用来排序 frontier 的值 |
| Informed Search | 有信息搜索 | 使用 problem-specific guidance 的 search |
| Best-First Search | 最佳优先搜索 | 每次展开 evaluation function 最好的 frontier node |
| Greedy Best-First Search | 贪心最佳优先搜索 | `f(n)=h(n)`，只看估计离 goal 多近 |
| A* Search | A 星搜索 | `f(n)=g(n)+h(n)`，平衡已付 cost 与估计剩余 cost |
| Priority Queue | 优先队列 | 每次取 priority 最小/最高的 frontier node |
| Straight-Line Distance | 直线距离 | 地图问题中常见的 admissible heuristic |
| Admissible Heuristic | 可采纳启发式 | 永远不 overestimate：`h(n) <= h*(n)` |
| Consistent Heuristic | 一致启发式 | 满足 triangle inequality，graph search 更稳定 |
| Relaxed Problem | 放松问题 | 去掉某些约束后得到 easier problem |
| Dominance | 支配关系 | 一个 admissible heuristic 总是更接近 `h*`，通常更少展开 nodes |
| Manhattan Distance | 曼哈顿距离 | grid / 8-puzzle 中横纵移动距离之和 |
| Misplaced Tiles | 错位 tile 数 | 8-puzzle 中不在目标位置的 tile 数 |

---

## 01 · Before

### Big Question

Uninformed search 只看 problem definition，不知道 goal 大概在哪个方向。

Week 3 的问题是：

> 如果我们有一些关于“离 goal 还多远”的估计，怎样把它放进 search algorithm 里？

这就是 informed search（有信息搜索）。

主线：

```text
BFS / DFS / IDS
-> assume simple or unit step costs
-> Uniform Cost Search handles weighted path cost g(n)
-> Greedy Best-First Search uses heuristic h(n)
-> A* combines g(n) + h(n)
-> admissible heuristic gives optimality for A* tree search
```

### Key Symbols

| Symbol | Meaning | 中文直觉 |
| --- | --- | --- |
| $g(n)$ | actual path cost from start to node $n$ | 已经花了多少 |
| $h(n)$ | heuristic estimate from $n$ to goal | 估计还差多少 |
| $f(n)$ | evaluation function used to rank frontier nodes | 用来排序的优先级 |
| $h^*(n)$ | true optimal cost from $n$ to goal | 真实还差多少 |

Memory:

```text
g = gone cost
h = hope / heuristic remaining cost
f = full estimated cost
```

---

## 02 · From Unit Cost to Weighted Cost

Before UCS, the simpler search algorithms often assume:

```text
each action cost = 1
```

Then path cost is just depth:

$$
g(n)=depth(n)
$$

This works for puzzles where every move has the same cost, such as simple 8-puzzle moves.

But map navigation is different:

```text
Arad -> Sibiu might cost 140
Arad -> Timisoara might cost 118
```

If edge weights differ, “fewest actions” is not necessarily “lowest cost.”

So we need a search strategy that cares about actual accumulated cost.

---

## 03 · Uniform Cost Search

Uniform Cost Search (UCS) is badly named.

The name sounds like:

> every action has uniform cost

But the lecture says it means almost the opposite:

> UCS is for weighted graphs where action costs may differ.

### Core Idea

UCS expands the node with the lowest actual path cost so far.

$$
f(n)=g(n)
$$

Implementation:

```text
frontier = priority queue ordered by g(n)
```

So UCS is like BFS generalized from:

```text
shallowest depth
```

to:

```text
lowest path cost
```

### Path Cost

If a path visits:

```text
N0 -> N1 -> N2 -> N3
```

and each edge cost is $C(i,j)$, then:

$$
g(N_3)=C(0,1)+C(1,2)+C(2,3)
$$

Path cost is additive.

The lecture assumes positive / nonnegative costs so that cost does not decrease as a path gets longer.

### UCS vs BFS Goal Test Timing

This is a subtle but important difference.

In BFS:

```text
test goal when child is generated / before insertion
```

Why? Because with unit costs, the first time you generate a goal at depth $d$, no shallower goal remains undiscovered.

In UCS:

```text
test goal when node is selected for expansion / popped from priority queue
```

Why?

Because a goal can be generated by a costly path while a cheaper path to the same goal is still waiting in the frontier.

So UCS:

- enqueues a node before checking goal；
- updates a node on the frontier if a better path to the same state is found；
- returns goal only when it is the lowest-cost node currently available。

### Shape of UCS Search

BFS expands in depth contours:

```text
depth 0
depth 1
depth 2
```

UCS expands in cost contours:

```text
g(n) < 100
g(n) < 200
g(n) < 300
```

中文直觉：

> UCS 不是一圈一圈按步数扩张，而是一圈一圈按累计 cost 扩张。

Problem:

> UCS may still explore cheap paths that go in the wrong direction, because it does not know where the goal lies.

This motivates informed search.

---

## 04 · Informed Search and Best-First Search

Informed search adds problem-specific knowledge.

The new idea is:

```text
rank frontier nodes using an evaluation function f(n)
that may include an estimate of distance to the goal
```

Best-first search means:

> select the frontier node with minimal evaluation function $f(n)$.

Implementation:

```text
frontier = priority queue sorted by f(n)
```

Different choices of $f(n)$ give different algorithms:

| Algorithm | Evaluation Function | What It Prioritizes |
| --- | --- | --- |
| UCS | $f(n)=g(n)$ | lowest cost so far |
| Greedy best-first | $f(n)=h(n)$ | estimated closest to goal |
| A* | $f(n)=g(n)+h(n)$ | lowest estimated total cost |

---

## 05 · Heuristic Functions

A heuristic is:

> a rule of thumb, simplification, or educated guess.

The lecture connects the word heuristic to “Heureka / Eureka” and the Archimedes bathtub story:

```text
hard exact measurement
-> use a clever simplification
-> get a useful estimate
```

In search:

$$
h(n)=\text{estimated distance from node }n\text{ to the goal}
$$

Important:

> The heuristic is an estimate. If we already knew the true distance to goal everywhere, we would have almost solved the search problem.

### Straight-Line Distance

For map navigation, a common heuristic is straight-line distance.

English idiom:

```text
as the crow flies
```

The lecture jokes that for this class it could be:

```text
as the drone flies
```

Straight-line distance ignores roads and intermediate cities.

Example:

```text
Arad to Bucharest straight-line distance = 366 km
```

Why useful?

> It is usually an underestimate of actual road distance, because roads cannot always go perfectly straight.

So straight-line distance is a lower bound on real travel cost.

---

## 06 · Greedy Best-First Search

Greedy best-first search uses only the heuristic estimate:

$$
f(n)=h(n)
$$

It expands the node estimated to be closest to the goal.

It completely ignores:

$$
g(n)
$$

the cost already paid to reach the node.

Memory:

```text
Greedy = only looks forward
```

### Greedy on a Grid

In an open field, greedy can look excellent:

```text
start
-> keep moving toward smaller h(n)
-> reach goal quickly
```

But with obstacles, greedy may chase the goal direction and miss a shorter route that initially moves away.

### Greedy on Romania

From Arad, the frontier might include:

| City | Straight-line distance to Bucharest |
| --- | ---: |
| Sibiu | 253 |
| Timisoara | 329 |
| Zerind | 374 |

Greedy picks Sibiu because it has the smallest $h(n)$.

Then from Sibiu, it may pick Fagaras because:

```text
h(Fagaras) = 176
```

Then it reaches Bucharest:

```text
Arad -> Sibiu -> Fagaras -> Bucharest
```

Path cost:

```text
450 km
```

But the shorter path is:

```text
Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
```

Path cost:

```text
418 km
```

So greedy is not optimal.

### Greedy Properties

| Property | Greedy best-first search |
| --- | --- |
| Complete? | Not generally; can get stuck in loops |
| Optimal? | No |
| Frontier | priority queue ordered by $h(n)$ |

Example loop:

```text
Iasi -> Neamt -> Iasi -> Neamt -> ...
```

Takeaway:

> Greedy can be fast, but it trusts the heuristic too naively.

---

## 07 · A* Search

A* is the best-known form of best-first search.

Lecture story:

> A because algorithm, star because it is neat.

The actual idea:

> avoid expanding paths that are already expensive, but still expand promising paths first.

A* uses:

$$
f(n)=g(n)+h(n)
$$

where:

- $g(n)$ is actual cost so far；
- $h(n)$ is estimated remaining cost；
- $f(n)$ is estimated total cost through $n$。

Implementation:

```text
frontier = priority queue ordered by increasing f(n)
```

### Why A* Is Less Reckless Than Greedy

Greedy:

```text
f(n)=h(n)
```

Only asks:

> Which node looks closest to the goal?

A*:

```text
f(n)=g(n)+h(n)
```

Asks:

> Which node gives the best estimated total route from start to goal?

So A* hedges its bets（保守一点）:

```text
does not blindly rush toward the goal
does not ignore path cost already paid
```

---

## 08 · Admissible Heuristics

A heuristic is admissible if it never overestimates the true remaining cost.

Formal definition:

$$
0 \le h(n) \le h^*(n)
$$

where:

$$
h^*(n)=\text{true optimal cost from }n\text{ to a nearest goal}
$$

For any goal state $G$:

$$
h(G)=0
$$

Memory:

```text
admissible = optimistic
```

It may underestimate:

```text
"I think goal is closer than it really is"
```

But it cannot overestimate:

```text
"I think goal is farther than it really is"
```

### Why Overestimating Is Dangerous

If a heuristic is pessimistic / inadmissible, it can push a truly good path too far down the priority queue.

```text
best path has high overestimated h(n)
-> f(n) looks too expensive
-> another worse goal path may be expanded first
```

Admissible heuristics do the opposite:

> They slow down bad plans, but never outweigh the true cost of good plans.

### A* Optimality Condition

Lecture theorem:

> If $h(n)$ is admissible, A* using tree search is optimal.

For graph search, the standard stronger condition is consistency, covered in quiz notes and usually needed when repeated states are merged.

---

## 09 · A* on Romania

At Arad:

```text
g(Arad) = 0
h(Arad) = 366
f(Arad) = 366
```

After expanding Arad:

| Node | $g(n)$ | $h(n)$ | $f(n)$ |
| --- | ---: | ---: | ---: |
| Sibiu | 140 | 253 | 393 |
| Timisoara | 118 | 329 | 447 |
| Zerind | 75 | 374 | 449 |

A* expands Sibiu next because $393$ is smallest.

Later, A* may generate Bucharest through Fagaras:

```text
Arad -> Sibiu -> Fagaras -> Bucharest
cost = 450
```

But A* is not done just because it sees a goal.

Important rule:

> A* returns the goal only when the goal node is popped from the frontier as the lowest-$f$ node.

Why?

Because another frontier path might still lead to a cheaper goal.

Indeed, A* later finds:

```text
Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
cost = 418
```

Now Bucharest with cost 418 rises to the top of the priority queue, and A* returns it.

Core lesson:

```text
seeing a goal is not enough
expanding / popping the best goal is enough
```

---

## 10 · Sketch: Why A* Tree Search Is Optimal

This is a proof sketch, not a full formal proof.

Assume:

- $A$ is an optimal goal node；
- $B$ is a suboptimal goal node；
- $h$ is admissible。

Goal:

> Show that $A$ exits the frontier before $B$.

Imagine $B$ is already on the frontier.

There must be some ancestor $n$ of $A$ on the frontier too, possibly $A$ itself.

Because $n$ lies on the optimal path to $A$:

$$
f(n)=g(n)+h(n)\le g(A)
$$

Why?

The heuristic $h(n)$ is admissible, so it underestimates the remaining true cost from $n$ to $A$ / goal.

At a goal node:

$$
h(A)=0
$$

so:

$$
f(A)=g(A)
$$

Since $B$ is suboptimal:

$$
g(A)<g(B)
$$

and because $B$ is also a goal:

$$
h(B)=0
$$

so:

$$
f(B)=g(B)
$$

Therefore:

$$
f(n)\le f(A)<f(B)
$$

A* pops the lowest $f$ value first, so $n$ must be expanded before $B$.

This applies to every ancestor of $A$, including $A$ itself.

So:

```text
all ancestors of optimal goal A expand before suboptimal goal B
-> A exits frontier before B
-> A* tree search is optimal
```

---

## 11 · Heuristics for the 8-Puzzle

8-puzzle has:

- branching factor usually at most 3 after avoiding direct backtracking；
- average solution cost around 22 steps。

A good heuristic can reduce node expansions dramatically.

### Misplaced Tiles

Misplaced tile heuristic:

$$
h_{oop}(n)=\text{number of out-of-place numbered tiles}
$$

If 8 tiles are out of place:

```text
h_oop(n) = 8
```

This is admissible because each misplaced tile must move at least once.

### Manhattan Distance

Manhattan distance:

$$
h_{md}(n)=\sum_{\text{numbered tile }t}
\left(
|row_t-row_t^*|+|col_t-col_t^*|
\right)
$$

The blank tile is not counted.

Why admissible?

> Each tile must move at least its row/column distance to reach its goal position, and real puzzle constraints can only make it harder, not easier.

In the slide example:

```text
h_md(S) = 3 + 1 + 2 + 2 + 2 + 3 + 3 + 2 = 18
```

---

## 12 · Relaxed Problems

A relaxed problem removes one or more constraints from the original problem.

Key theorem-like idea:

> The optimal solution cost of a relaxed problem is an admissible heuristic for the original problem.

Why?

```text
remove constraints
-> problem becomes easier
-> optimal cost cannot increase
-> relaxed cost <= original true cost
-> no overestimate
```

For 8-puzzle, original rule:

```text
A tile can move from square A to square B
if A is adjacent to B
and B is blank.
```

Relaxed versions:

| Relaxed Rule | Heuristic |
| --- | --- |
| tile can move to any adjacent square | Manhattan distance |
| tile can move to any square | misplaced tiles |
| tile can move to a blank square | not very useful here |

This explains why both misplaced tiles and Manhattan distance are admissible.

---

## 13 · Dominance

Suppose $h_1$ and $h_2$ are both admissible.

$h_2$ dominates $h_1$ if:

$$
h_2(n)\ge h_1(n)
$$

for every node $n$.

中文直觉：

> 两个 heuristic 都不能超过真实 cost；在这个前提下，越接近真实 cost 越有信息量。

If $h_2$ dominates $h_1$, then $h_2$ is usually better for search.

For 8-puzzle:

```text
Manhattan distance dominates misplaced tiles
```

because a tile that is out of place is at least 1 Manhattan move away, and sometimes more.

### Typical Node Expansion Costs

Slide examples:

| Setting | Search | Average nodes expanded |
| --- | --- | ---: |
| $d=12$ | Iterative deepening | 3,644,035 |
| $d=12$ | A* with misplaced tiles | 227 |
| $d=12$ | A* with Manhattan distance | 73 |
| $d=24$ | A* with misplaced tiles | 39,135 |
| $d=24$ | A* with Manhattan distance | 1,641 |

Takeaway:

> Better heuristics reduce the number of nodes expanded.

---

## 14 · Best and Worst Admissible Heuristics

Best admissible heuristic:

$$
h^*(n)=\text{true cost from }n\text{ to goal}
$$

This is like an oracle. It dominates all other admissible heuristics.

But it is usually unachievable:

> If we already knew $h^*(n)$ everywhere, we would have solved much of the search problem.

Worst admissible heuristic:

$$
h(n)=0
$$

This is still admissible because it never overestimates.

But A* becomes:

$$
f(n)=g(n)+0=g(n)
$$

So A* with $h(n)=0$ becomes Uniform Cost Search.

Memory:

```text
h* = perfect but unavailable
h=0 = safe but useless
```

---

## 15 · UCS vs Greedy vs A*

| Algorithm | Priority | Uses Path Cost? | Uses Heuristic? | Main Behavior |
| --- | --- | --- | --- | --- |
| UCS | $g(n)$ | yes | no | expands cheapest cost-so-far |
| Greedy | $h(n)$ | no | yes | rushes toward estimated goal |
| A* | $g(n)+h(n)$ | yes | yes | balances spent cost and remaining estimate |

Contour intuition:

```text
UCS:
    expands cost contours equally outward
    can explore cheap wrong-direction paths

Greedy:
    stretches straight toward the goal
    can ignore expensive path already taken

A*:
    stretches toward the goal
    but hedges enough to preserve optimality with admissible h
```

---

## 16 · A* Applications

The lecture mentions A* in many practical settings:

- GPS / route finding；
- video game pathfinding；
- robot motion planning；
- resource planning and scheduling。

Why it appears everywhere:

```text
world can be represented as graph
actions have costs
goal is known
heuristic can estimate remaining distance
```

### Red Blob Games Implementation Idea

The lecture recommends Amit Patel's Red Blob Games A* tutorial.

Implementation pattern:

```text
frontier priority queue
came_from map
cost_so_far map
```

`came_from` can reconstruct the path:

```text
goal -> parent -> parent -> ... -> start
then reverse
```

Alternative implementation:

```text
store (node, path_so_far) directly in the queue
```

This is often simpler for homework, but can use more memory because many path lists are copied.

---

## 17 · Common Confusions

### Confusion 1: Uniform Cost Search Means Unit Cost

Incorrect:

> UCS means every action has the same cost.

Correct:

> UCS handles non-uniform / weighted step costs by expanding lowest $g(n)$.

### Confusion 2: Greedy Is Optimal If the Heuristic Looks Reasonable

Incorrect:

> Straight-line distance points toward the goal, so greedy should find shortest path.

Correct:

> Greedy ignores $g(n)$ and can return a longer route.

### Confusion 3: A* Stops When It First Sees a Goal

Incorrect:

> Once Bucharest appears in the frontier, return it.

Correct:

> A* returns the goal when the goal is popped as the lowest-$f$ frontier node.

### Confusion 4: Admissible Means Accurate

Incorrect:

> Admissible means the heuristic is close to the true cost.

Correct:

> Admissible means it never overestimates. It can be very weak, like $h(n)=0$.

### Confusion 5: Dominance Means Larger Sometimes

Incorrect:

> $h_2$ dominates $h_1$ if it is larger on most nodes.

Correct:

> Dominance must hold for every node, and both heuristics must be admissible.

### Confusion 6: Relaxing a Problem Makes the Heuristic Bigger

Incorrect:

> Removing constraints creates a larger cost.

Correct:

> Removing constraints makes the problem easier, so the relaxed optimal cost is a lower bound.

---

## 18 · Self-Check

Try answering without reading:

1. Why is Uniform Cost Search badly named?
2. What does $g(n)$ measure?
3. Why does UCS test for goal when a node is popped, not when generated?
4. What is the difference between cost contours and depth contours?
5. What does $h(n)$ estimate?
6. Why is straight-line distance usually admissible for road navigation?
7. Why can Greedy best-first search be fast but non-optimal?
8. In the Romania example, why is `Arad -> Sibiu -> Fagaras -> Bucharest` not optimal?
9. What does A* use as its priority?
10. Why does A* balance UCS and Greedy behavior?
11. What does admissible mean formally?
12. Why can an inadmissible heuristic break optimality?
13. In the A* proof sketch, why must an ancestor of the optimal goal be expanded before a suboptimal goal?
14. Why is Manhattan distance admissible for 8-puzzle?
15. What is a relaxed problem?
16. Why does Manhattan distance dominate misplaced tiles?
17. What happens when A* uses $h(n)=0$?
18. Why is $h^*(n)$ the best admissible heuristic but usually unavailable?

---

## 19 · Oral Exam Prompts

Question:

Explain the difference between UCS, Greedy best-first search, and A*.

My answer:


Verdict:


Missing:

Question:

Why does A* not return a goal as soon as the goal is generated?

My answer:


Verdict:


Missing:

Question:

What makes a heuristic admissible, and why does A* need that condition?

My answer:


Verdict:


Missing:

Question:

Explain how relaxed problems produce admissible heuristics for 8-puzzle.

My answer:


Verdict:


Missing:

Question:

Why does Manhattan distance dominate misplaced tiles?

My answer:


Verdict:


Missing:

---

## 20 · One Sentence

$$
\boxed{
\text{Informed search ranks frontier nodes using cost estimates: UCS uses } g(n), \text{ Greedy uses } h(n), \text{ and A* uses } g(n)+h(n) \text{ with admissible heuristics to preserve optimality.}
}
$$

---

## 21 · Connections

Uninformed Search

-> Uniform Cost Search
-> Path Cost $g(n)$
-> Heuristic $h(n)$
-> Best-First Search
-> Greedy Best-First Search
-> A*
-> Admissible Heuristic
-> Relaxed Problem
-> Dominance
-> 8-Puzzle Manhattan Distance
-> Practical Pathfinding
