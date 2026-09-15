# Search Problems

> Week 02 · Module 02

Source: `03-Search-Problems.pptx.pdf`, user's pasted Canvas transcripts for Module 2 introduction, Task Environments, Search Problem Introduction, Search Problem Formulation, Basic Search Algorithms, Uninformed Search Strategies, Review of BFS and DFS, and Why Do We Care About Search.

This note treats the attached course materials as source material only. It records the lecture logic for learning and review.

## 00 · Quick Review First

### Read With These Questions

1. 什么情况下 reflex agent 不够，需要 problem-solving agent？
2. A search problem 的五个核心成分是什么？
3. state 和 node 的区别是什么？为什么同一个 state 可以出现在多个 node 里？
4. frontier 存的是什么？explored set / visited set 存的是什么？
5. tree search 为什么会重复走回头路？graph search 用什么避免 repeated states？
6. BFS 为什么 complete？它的 optimality 需要什么假设？
7. DFS 为什么省 memory？它为什么可能不 complete / not optimal？
8. Depth-limited search 的 limit `l` 小于、等于、大于 `d` 时分别会发生什么？
9. Iterative deepening search 为什么重复展开浅层节点，但时间复杂度仍然是 `O(b^d)`？
10. `b`、`d`、`m` 分别控制哪类复杂度？为什么不能混在一起？

### One-Minute Map

```text
rational agent needs planning
-> formulate a search problem
-> represent states, actions, transitions, goal test, and path cost
-> build a search tree over nodes
-> manage the frontier
-> choose an expansion order: BFS / DFS / DLS / IDS
-> evaluate by completeness, optimality, time, and space
```

一句话记忆：

> Search is not "finding a fact"; it is finding an action sequence from an initial state to a goal state.

### Professional Terms

| Term | 中文 | Quick Meaning |
| --- | --- | --- |
| Search Problem | 搜索问题 | 用状态、动作、转移、目标和代价描述 planning |
| State | 状态 | 世界在抽象层面的一个 configuration |
| Initial State | 初始状态 | search 开始的 state |
| Action | 动作 | 在某个 state 下可选择的 operation |
| Transition Model | 转移模型 | `Result(s, a)`，动作之后到哪个 state |
| Successor | 后继 | 从当前 state/action 产生的新 state |
| State Space | 状态空间 | 所有 reachable states 的集合 |
| Goal Test | 目标测试 | 判断当前 state 是否已经达到目标 |
| Path | 路径 | 从 start 到某个 node 的 action sequence |
| Path Cost | 路径代价 | 整条 path 的累计 cost |
| Search Tree | 搜索树 | algorithm 展开的 node 结构，不等于原始 state graph |
| Node | 节点 | 包含 state、parent、action、path cost、depth 的 search-tree record |
| Frontier | 边界队列 | 已生成但还没有展开的 nodes |
| Explored Set / Visited Set | 已访问集合 | graph search 用来避免重复 state |
| Tree Search | 树搜索 | 不记 visited，可能重复展开同一 state |
| Graph Search | 图搜索 | 记录 visited / best-known states，避免 repeated states |
| Uninformed Search | 无信息搜索 | 不用 goal 方向信息，只按 problem definition 搜 |
| Breadth-First Search (BFS) | 广度优先搜索 | FIFO frontier，按 depth 一层层展开 |
| Depth-First Search (DFS) | 深度优先搜索 | LIFO frontier，先沿一条 path 走深 |
| Depth-Limited Search (DLS) | 深度限制搜索 | DFS 加最大深度 limit `l` |
| Iterative Deepening Search (IDS) | 迭代加深搜索 | 从小到大反复跑 DLS |
| Branching Factor `b` | 分支因子 | 每个 node 最多 successors 数 |
| Shallowest Goal Depth `d` | 最浅目标深度 | 最近 solution 的 depth |
| Maximum Depth `m` | 最大深度 | search space 中最长 path 的深度，可能 infinite |

---

## 01 · Before

### Big Question

Module 2 的核心问题是：

> 如果 agent 不能只靠当前 percept 立刻决定 action，它如何 plan ahead（向前规划）？

课程把这个问题转成 search problem：

```text
current state
-> possible actions
-> successor states
-> many possible action sequences
-> choose a sequence that reaches a goal
-> prefer the sequence with lowest path cost
```

所以这一章不是在讲“互联网搜索”，而是在讲：

$$
\boxed{
\text{search = finding a sequence of actions from an initial state to a goal state}
}
$$

### Why This Comes After Rational Agents

Module 1 说 rational agent 要根据 percept sequence 选择 expected performance 最好的 action。

但很多时候：

- 当前 action 的好坏取决于后面能不能到达 goal；
- immediate reaction（即时反应）不够；
- agent 必须考虑 action sequence（动作序列）。

这时 agent 就变成 problem-solving agent（问题求解 agent）。

### Questions

1. State（状态）和 node（搜索树节点）为什么不是同一个东西？
2. 为什么 fully observable + deterministic + known environment 里可以用 fixed action sequence？
3. 为什么 repeated states 会让简单 tree search 爆炸？
4. BFS 为什么 complete，但 space 很差？
5. DFS 为什么省内存，但不保证 complete / optimal？
6. Iterative deepening 为什么重复搜索很多层还仍然是 $O(b^d)$？

---

## 02 · Notes

### Reflex Agent vs Problem-Solving Agent

Simple reflex agent（简单反射 agent）只看 current percept（当前感知）：

```text
current percept -> rule -> action
```

例子：

```text
ultrasonic sensor sees wall ahead
-> stop
-> turn left
-> if wall remains, turn around
```

它的问题是：

> It reacts, but it does not plan.

Problem-solving agent（问题求解 agent）有一个 goal，并且要找一串 actions：

```text
initial state
-> action 1
-> action 2
-> ...
-> goal state
```

这串 actions 叫 solution（解）。

### What Search Means Here

日常里的 search 常常指“查资料”：

```text
query -> documents / webpages
```

AI 里的 search 指：

```text
problem state
-> possible next states
-> possible paths
-> goal state
```

更准确地说：

$$
\boxed{
\text{Search is planning through a space of possible action sequences.}
}
$$

如果有很多条 path 都能到 goal，我们还要问：

> Which solution is optimal?

Optimal solution（最优解）通常指 path cost 最低的 solution。

---

## 03 · Task Environment Determines the Solution Type

Search 不是在任何环境下都直接返回同一种东西。

如果 environment 是：

- fully observable（完全可观测）；
- deterministic（确定性）；
- known（转移规则已知）。

那么 solution 可以是 fixed sequence of actions（固定动作序列）：

```text
do A
then do B
then do C
```

原因是 agent 已经知道：

```text
current state + chosen action -> exact next state
```

如果 environment 是：

- partially observable（部分可观测）；或
- nondeterministic（非确定性）。

那么 fixed sequence 不够，solution 需要像 contingency plan（条件计划）：

```text
do A
if percept says outcome 1 -> do B
if percept says outcome 2 -> do C
```

也就是 branching strategy（分支策略）。

这章先限制在比较简单的环境：

$$
\boxed{
\text{static, fully observable, deterministic, discrete search problems}
}
$$

这样做不是因为真实世界都这么简单，而是因为要先把 search 的数学骨架学清楚。

---

## 04 · Formal Definition of a Search Problem

课件里给的 formal definition 很重要。一个 problem 由这些部分组成：

| Component | Meaning | 中文直觉 |
| --- | --- | --- |
| States $S$ | all possible states | 问题可能处在哪些状态 |
| Initial state $s_i \in S$ | where the agent starts | 起点 |
| Actions $A$ | possible actions | 在某状态能做什么 |
| Transition model | `Result(s, a) -> s'` | 做动作之后到哪里 |
| Path cost | additive cost of a path | 一整条路径的总代价 |
| Goal test | `Goal(s)` | 判断是否到达目标 |

Transcript 里强调：这 6 件事合起来不是算法本身，而是 problem representation（问题表示）。

```text
problem representation
-> tells the search algorithm what states exist
-> tells it how actions change states
-> tells it how to recognize success
-> tells it how to compare different successful paths
```

如果 formulation 写错，后面的 BFS / DFS 再正确也只是在错误的问题上认真搜索。

### States

State（状态）是对 world 的表示。

好的 state representation 应该只保留和问题有关的信息。

例子：

- 8-puzzle：9 个格子里 tile 和 blank 的排列。
- Romania route finding：当前所在 city。
- Vacuum world：agent 在哪个 cell，以及每个 cell 是否 dirty。

### Initial State

Initial state 是 search 开始的地方。

写成数学符号：

$$
s_i \in S
$$

意思是：

> 初始状态也是所有可能状态集合 $S$ 里的一个状态。

### Actions

不是每个 action 在每个 state 都合法。

所以更准确地写：

$$
Actions(s)
$$

表示：

> 在状态 $s$ 中可以执行的 action 集合。

8-puzzle 里 blank 在中间时，可以 up/down/left/right；在角落时只能两个方向。

所以 `Actions(s)` 不是一个固定列表，而是 state-dependent（依赖状态的）函数。

```text
blank in center -> 4 legal actions
blank in corner -> 2 legal actions
```

### Transition Model

Transition model 描述 action 的结果：

$$
Result(s,a) \to s_r
$$

其中：

- $s$ 是当前 state；
- $a$ 是 action；
- $s_r$ 是 resulting state / successor state。

如果 $s_r = Result(s,a)$，那么 $s_r$ 是 $s$ 的 successor（后继状态）。

这章先假设 deterministic transition：

```text
state + action -> one resulting state
```

Transcript 预告后面会放松这个限制。到 stochastic environment 时，transition model 会变成 probabilistic：

```text
state + action -> distribution over possible resulting states
```

也就是说，搜索问题里的 transition model 和上一章的 task environment 分类是连着的。

### State Space

State space 是从 initial state 出发，通过任意 action sequence 能到达的所有状态。

课件写法：

$$
\{s_i\} \cup Successors(s_i)^*
$$

直觉解释：

```text
start at initial state
-> take 0 actions, 1 action, 2 actions, ...
-> collect every reachable state
```

注意：

> State space might be a proper subset of all configurations.

8-puzzle 有 $9!$ 种 tile arrangement，但只有约 $9!/2$ 是从某个给定状态可达的。

### Path Cost

Path cost 是整条 path 的总代价，必须 additive（可相加）。

如果一步从 $x$ 经 action $a$ 到 $y$，step cost 写作：

$$
c(x,a,y) \ge 0
$$

整条 path 的 cost 就是每一步 cost 的和。

这里的 minimization（最小化）和 Module 1 的 performance maximization 不是矛盾。

可以把它理解成：

```text
maximize performance
= minimize cost / loss / time / distance
```

课件假设 step cost nonnegative（非负）。如果有负 cost，很多 shortest-path / optimality 直觉会变得危险，因为绕圈可能让总代价越来越低。

例子：

- 8-puzzle：每移动一次 tile，cost = 1。
- Romania map：每条 road 的 distance / travel time 是 step cost。

### Goal Test

Goal test 是一个判断函数：

$$
Goal(s)
$$

如果为 true，$s$ 就是 goal state。

Goal test 可以是 explicit，也可以是 implicit。

例子：

- 8-puzzle：tiles 是否排成目标顺序。
- Chess：是否 checkmate。
- Route finding：当前 city 是否是 Bucharest。

Explicit goal test:

```text
current city == Bucharest
```

Implicit goal test:

```text
board is in a checkmate configuration
```

重点不是 goal 一定只有一个 state，而是我们有一个 test 能判断当前 state 是否满足目标条件。

---

## 05 · Example: 8-Puzzle

8-puzzle 是一个 $3 \times 3$ grid：

- 8 个 numbered tiles；
- 1 个 blank square；
- goal 是把 tiles 排成指定顺序。

Formulation:

| Part | 8-puzzle |
| --- | --- |
| States | configurations of 8 tiles plus blank |
| Initial state | given starting board |
| Actions | move blank up/down/left/right when legal |
| Transition model | swap blank with neighboring tile |
| Goal test | board equals goal configuration |
| Path cost | number of moves |

为什么 action 可以说是 “move a tile”，也可以说是 “move the blank”？

因为这两个描述对应同一个 transition：

```text
blank moves left
= tile on the left moves right into blank
```

通常写 blank 的移动更方便，因为 blank 的合法 moves 最多 4 个：

```text
up / down / left / right
```

### 8-Puzzle 的搜索难点

8-puzzle 看起来小，但 state space 很快变大。

全部排列数量：

$$
9!
$$

给定 parity 后可达状态大约：

$$
\frac{9!}{2} \approx 181{,}440
$$

这说明：

> 简单问题也可能需要系统化搜索，而不是靠眼睛随便试。

Transcript 还补充了 state representation 的选择：

```text
2D board representation
or
1D list / tuple read row by row
```

例如：

```text
[7, 2, 4, 5, blank, 6, 8, 3, 1]
```

两种 representation 都可以。关键是它必须让我们清楚定义：

- legal actions；
- transition model；
- goal test；
- path cost。

---

## 06 · Example: Holiday in Romania

问题故事：

```text
You are in Arad.
You need to get to Bucharest.
```

Formulation:

| Part | Romania route problem |
| --- | --- |
| States | cities |
| Initial state | Arad |
| Actions | drive from current city to connected city |
| Transition model | following an edge takes you to neighbor city |
| Goal test | current city is Bucharest |
| Path cost | distance or travel time |
| Solution | sequence of cities / roads |

Example path:

```text
Arad -> Sibiu -> Fagaras -> Bucharest
```

But shortest path in the common AIMA map is:

```text
Arad -> Sibiu -> Ramnicu Valcea -> Pitesti -> Bucharest
```

with cost:

$$
140 + 80 + 97 + 101 = 418
$$

这个例子重要是因为它把一个真实任务变成 graph shortest path：

```text
cities = nodes
roads = edges
road distance = edge weight
route = path
best route = lowest path cost
```

Google Maps 本质上也在做类似 search，只是它还要考虑 traffic、accidents、实时 road conditions，所以 edge cost 会动态变化。

---

## 07 · Example: Vacuum World

简单 two-cell vacuum world：

- agent 可以在任一 cell；
- 每个 cell 可以 dirty 或 clean。

状态数：

$$
2 \text{ positions} \times 2^2 \text{ dirt configurations} = 8
$$

如果有 $n$ 个 cells：

$$
n \cdot 2^n
$$

Formulation:

| Part | Vacuum world |
| --- | --- |
| States | agent position plus dirt status of each cell |
| Actions | suck, move left, move right, maybe up/down |
| Transition model | suck removes dirt; move changes position unless wall blocks it |
| Goal states | all cells clean |
| Action cost | each action costs 1 |

这个例子帮助记住：

> 状态不是只写 agent 的位置，还要写和目标有关的 world facts。

如果目标是 clean all dirt，那么 dirt status 必须进 state。

---

## 08 · The Art of Formulating a Search Problem

Formulation（问题形式化）不是机械填表，它会决定 search space 的大小。

课件强调：

> Formulation greatly affects combinatorics of search space and therefore speed of search.

Transcript 的说法更直接：

> A lot of search formulation is the process of creating a representation.

也就是说，AI 里很多难点不是“会不会 BFS”，而是：

```text
real-world task
-> choose what counts as a state
-> choose what counts as an action
-> remove irrelevant detail
-> keep enough structure to solve the real problem
```

### Abstraction

真实世界太复杂，所以 state space 必须 abstraction（抽象）。

例如：

```text
Arad -> Zerind
```

在真实世界里不是一个简单动作，它包含：

- 具体路线；
- 开车操作；
- 速度变化；
- 休息；
- 绕路；
- 路况。

但在 route search 里，我们把它抽象成一个 action。

换句话说，abstract state / abstract action 是 real-world states/actions 的 equivalence class（等价类）：

```text
many real driving details
-> one abstract action: drive from Arad to Zerind
```

### Valid Abstraction

抽象必须 valid：

> If the abstract path says a route exists, the corresponding real-world action should be achievable.

也就是说：

```text
abstract solution
-> can be refined into real action sequence
```

如果抽象太粗，算法找到的 solution 在现实中无法执行；如果抽象太细，state space 会大到搜不动。

这是 search formulation 的艺术：

$$
\boxed{
\text{keep enough detail to solve the task, remove detail that does not affect the goal}
}
$$

---

## 09 · Search Fundamentals

### State Space

State space 是所有 reachable states。

当每个 state 有多个 operators/actions 时，state space 会快速增长。

### Path

Path 是从一个 state 到另一个 state 的 action sequence。

可以写成 states：

```text
s0 -> s1 -> s2 -> goal
```

也可以写成 actions：

```text
a0, a1, a2, ...
```

### Frontier

Frontier（边界 / 待展开集合）是：

> states or nodes that have been generated but not expanded yet.

不同 search strategy 的核心差别通常就是：

```text
which frontier node do we expand next?
```

Transcript 对 strategy 的定义很实用：

> Search strategy = the order in which we expand nodes from the frontier.

实现上，这个 order 通常来自 frontier 的数据结构：

| Frontier data structure | Strategy |
| --- | --- |
| FIFO queue | breadth-first search |
| LIFO stack | depth-first search |
| priority queue | priority-based search |

所以很多 search algorithm 的差别不是 expand 逻辑完全不同，而是：

```text
same general search skeleton
different frontier discipline
different behavior
```

### Solution

Solution 是从 initial state 到 goal state 的 path。

Optimal solution 是没有其他 solution 有更低 path cost。

---

## 10 · State vs Node

这是 search 里最容易混的点之一。

### State

State 是 world configuration 的表示。

例子：

```text
[7, 2, 4, 5, blank, 6, 8, 3, 1]
```

它只说：

> 现在 puzzle 长什么样。

### Node

Node 是 search tree 里的数据结构。

一个 node 通常包括：

| Field | Meaning |
| --- | --- |
| state | this node represents which state |
| parent | previous node |
| action | action used to reach this node |
| path cost $g(n)$ | cost from initial node to here |
| depth | number of steps from root |

所以：

$$
\boxed{
\text{states do not have parents, depth, or path cost; nodes do.}
}
$$

同一个 state 可以通过不同 path 被生成多次，因此可能对应多个 different nodes。

这正是 repeated states 问题的来源。

---

## 11 · Tree Search

Tree search 的 general idea：

```text
start with initial node in frontier
repeat:
    if frontier is empty, fail
    choose one frontier node according to strategy
    if it is goal, return solution
    expand it
    add children to frontier
```

Strategy（策略）决定 search process：

```text
FIFO queue -> BFS
LIFO stack -> DFS
priority queue -> cost / heuristic based search
```

Tree search treats different paths to the same state as distinct.

这会导致 repeated states。

在 search tree 里，即使两个 nodes 里面的 state 一样，只要路径不同，tree search 也会把它们当成不同 nodes。

```text
same board configuration
different parent path
-> different search-tree node
```

这就是为什么 slide 上可以画出一棵 tree，即使原始问题本质上是 graph。

---

## 12 · Repeated States and Graph Search

Repeated states 是 search 里非常危险的问题。

课件里的核心警告：

> Failure to detect repeated states can turn a linear problem into an exponential one.

想象图里有 cycle：

```text
A -> B -> A -> B -> ...
```

Tree search 如果不记 visited，会不断把同一批 states 用不同路径重新生成。

8-puzzle 里的 backwards move 是直观例子：

```text
move blank left
then move blank right
-> returns to same state
-> path cost increased
```

在 nonnegative step cost 下，这种 loop 不可能帮助我们得到更低 path cost 的 solution。

### Graph Search

Graph search 在 tree search 基础上加 explored set（已探索集合）。

核心变化：

```text
before adding a child to frontier:
    check child.state not in explored
    and not already in frontier
```

更完整的 graph search rhythm：

```text
initialize frontier with initial node
initialize explored as empty set
repeat:
    if frontier is empty, fail
    pop node according to strategy
    if node is goal, return solution
    add node.state to explored
    expand node
    add child only if child.state is not explored and not in frontier
```

优点：

- 避免重复展开；
- 防止很多 cycles；
- 通常大幅减少时间。

代价：

- must keep track of visited states；
- can use a lot of memory。

这也是为什么 search implementation 里 state 要 hashable：

```python
explored = set()
explored.add(state)
```

如果 state 是 list，就不能直接放进 set；通常要用 tuple。

---

## 13 · Uninformed vs Informed Search

Uninformed search 也叫 blind search。

它只用 problem definition 里给的信息：

- initial state；
- actions；
- transition model；
- goal test；
- path cost。

它不使用额外的 domain-specific hint。

Romania map 的直觉：

```text
uninformed search ignores whether a city is geographically closer to Bucharest
```

也就是，即使某个 frontier node 看起来“方向更对”，blind search 也不会因为这个原因优先展开它。

直觉：

```text
uninformed search:
all non-goal frontier nodes look equally promising
```

Informed search 会使用 heuristic function：

$$
h(n)
$$

来估计某个 node 离 goal 有多近。

Transcript 的 queue 语言：

```text
informed search can push some non-goal nodes ahead in the queue
because heuristic information says they look more promising
```

这章主要讲 uninformed search；informed search 和 A* 是后面内容。

---

## 14 · How to Evaluate Search Strategies

一个 search strategy 通常从四个维度评价：

| Criterion | Question |
| --- | --- |
| Completeness | Will it find a solution if one exists? |
| Optimality | Will it find a lowest-cost solution? |
| Time complexity | How many nodes may be generated? |
| Space complexity | How many nodes may be kept in memory? |

常用变量：

| Symbol | Meaning |
| --- | --- |
| $b$ | maximum branching factor |
| $d$ | depth of the shallowest goal node |
| $m$ | maximum path length / maximum depth of state space |

Important:

- $d$ is about the first shallowest solution.
- $m$ can be much larger than $d$.
- $m$ may be infinite.

### Space Complexity

Transcript 里提醒：space complexity 和 time complexity 一样可以用 Big-O 分析。

单位不重要：

```text
bytes / KB / MB / fixed-size node count
```

Big-O 会忽略常数倍，所以我们关心的是随着 $b,d,m$ 增长，memory requirement 怎么增长。

对 search 来说，space 往往非常关键，因为 frontier、explored set、parent pointers 都要占内存。

---

## 15 · Breadth-First Search

BFS expands the shallowest unexpanded node first.

Implementation:

```text
frontier = FIFO queue
pop from front
insert successors at back
```

Python structure:

```python
from collections import deque

frontier = deque([start])
node = frontier.popleft()
frontier.append(child)
```

### BFS Intuition

BFS searches level by level:

```text
depth 0
depth 1
depth 2
...
```

所以如果 every step cost = 1，第一次找到 goal 时一定是最少步数。

Transcript 的直觉是 radiate outward（向外一层层扩散）：

```text
start
-> all nodes 1 step away
-> all nodes 2 steps away
-> all nodes 3 steps away
```

所以 BFS 的“短”指的是 depth / number of actions，不自动等于 lowest miles or lowest time。

### Subtle Point: Goal Test Timing

课件提到一个 subtle point：

> Node inserted into queue only after testing to see if it is a goal state.

也就是说，生成 child 后先 check goal；如果是 goal，直接返回 solution，不需要再把它塞进 frontier。

### BFS Properties

| Property | BFS |
| --- | --- |
| Complete? | Yes, if $b$ is finite |
| Optimal? | Yes if every step cost is 1 |
| Time | $O(b^d)$ |
| Space | $O(b^d)$ |

更展开地看，BFS 生成的节点数大约是：

$$
1 + b + b^2 + \cdots + b^d = O(b^d)
$$

为什么 space 也是 $O(b^d)$？

因为 BFS 要保留整层 frontier。到了 goal 所在深度附近，frontier 可能已经有指数级数量的 nodes。

### Main Weakness

BFS 最大问题通常不是算不动，而是内存爆掉。

课件给的直觉：

```text
b = 10
1M nodes/sec
1000 bytes/node
depth 8 -> about 100 GB
depth 10 -> about 10 TB
```

Transcript 还给了两个 takeaways：

- memory requirements can be worse than waiting time；
- exponential uninformed search only works for small instances。

所以：

$$
\boxed{
\text{BFS has nice guarantees, but exponential memory is painful.}
}
$$

---

## 16 · Depth-First Search

DFS expands the deepest unexpanded node first.

Implementation:

```text
frontier = LIFO stack
push successors
pop most recent successor
```

Python structure:

```python
frontier = [start]
node = frontier.pop()
frontier.append(child)
```

### DFS Intuition

DFS commits to one branch:

```text
go deeper
go deeper
go deeper
backtrack only when needed
```

这让它 memory-efficient，但也容易钻进错误的深分支。

Transcript 的比喻是 drill down as fast as possible（尽快往深处钻）：

```text
choose a successor
then its successor
then its successor
...
```

如果那条 branch 很深或者有 cycle，DFS 可能长期见不到浅层 goal。

### DFS Properties

| Property | DFS |
| --- | --- |
| Complete? | No in infinite-depth spaces or spaces with loops |
| Optimal? | No |
| Time | $O(b^m)$ |
| Space | $O(b \cdot m)$ |

如果 state space finite，并且 DFS 避免当前 path 上的 repeated states，它可以 complete。

但它仍然不 optimal，因为它可能先找到一条很深、很贵的 solution，而浅层更好的 solution 还没被探索。

注意 $m$ 和 $d$ 的区别：

```text
d = shallowest goal depth
m = maximum possible path depth
```

如果 $m \gg d$，DFS 的 $O(b^m)$ 会非常糟糕。

### When DFS Can Be Useful

Use DFS when:

- memory is restricted；
- there are many possible solutions；
- wrong paths terminate quickly；
- you do not need guaranteed optimality。

---

## 17 · BFS vs DFS

| Question | BFS | DFS |
| --- | --- | --- |
| Expansion order | shallowest first | deepest first |
| Frontier structure | FIFO queue | LIFO stack |
| Complete? | yes if finite branching | not generally |
| Optimal? | yes for unit step cost | no |
| Space | exponential $O(b^d)$ | linear-ish $O(b \cdot m)$ |
| Main risk | memory explosion | infinite branch / bad early path |

Memory trick:

```text
BFS = broad and safe but memory-heavy
DFS = deep and cheap but risky
```

---

## 18 · Depth-Limited Search

Depth-limited search 是 DFS with a depth limit $l$。

它的动机是：

```text
BFS:
    complete + unit-cost optimal
    but expensive memory

DFS:
    low memory
    but can disappear into infinite / very deep branches

Question:
    can we keep DFS memory while avoiding the infinite-depth trap?
```

规则：

```text
if node.depth == l:
    do not expand it
```

它解决 DFS 的 infinite path 问题，因为最多只走到 $l$ 层。

换句话说，depth limit $l$ 把搜索树剪断：

```text
depth 0
depth 1
...
depth l
stop expanding here
```

这不是说 depth $l$ 的 nodes 不存在，而是 algorithm 决定不再生成它们的 successors。

### Properties

| Case | Result |
| --- | --- |
| $l < d$ | incomplete, because goal is deeper than limit |
| $l = d$ | can find shallowest goal if lucky / appropriate order |
| $l > d$ | may find non-optimal deeper solution first |

这三种情况要会解释：

```text
l < d:
    cutoff happens before the shallowest goal
    -> algorithm reports failure / cutoff even though solution exists

l = d:
    cutoff exactly reaches shallowest goal depth
    -> can get the unit-depth optimal solution

l > d:
    DFS order may go below d before finding a shallower goal
    -> may return a deeper / higher-cost solution first
```

所以 DLS 的问题不是“limit 没用”，而是：

> A fixed limit is only good if we already know a good limit.

Complexity:

| Property | Depth-limited search |
| --- | --- |
| Time | $O(b^l)$ |
| Space | $O(b \cdot l)$ |

为什么 space 是 $O(b \cdot l)$？

因为它像 DFS 一样只保留当前 path 和每层少量 frontier siblings，而不是像 BFS 一样保留整层。

Depth-limited search by itself is not the final win. It is the building block for iterative deepening.

---

## 19 · Iterative Deepening Search

Iterative deepening search uses depth-limited search repeatedly:

```text
for limit = 0, 1, 2, 3, ...
    run depth-limited search with this limit
    if success, return solution
```

每一轮的意思是：

```text
limit 0: only test initial node
limit 1: search all paths of length at most 1
limit 2: search all paths of length at most 2
limit 3: search all paths of length at most 3
...
```

关键性质：

> IDS explores all nodes at shallow depth before it ever accepts a deeper solution.

这正好修复 DLS 的两个问题：

```text
fixed l too small
-> IDS will eventually increase l

fixed l too large
-> IDS already searched shallower depths first
-> it will not skip a shallower unit-cost solution
```

At first this seems wasteful because shallow nodes are regenerated many times.

But with exponential branching, most nodes are near the deepest searched level.

For first solution at depth $d$:

$$
d b + (d-1)b^2 + \cdots + 1 b^d = O(b^d)
$$

This has the same Big-O time as BFS.

### Why Repeating Work Is Still Okay

假设第一个 goal 在 depth 3，并且它是 depth 3 最后一个被找到的 node。

IDS 构造节点大致是：

```text
limit 1: b
limit 2: b + b^2
limit 3: b + b^2 + b^3
```

合起来：

$$
3b + 2b^2 + b^3
$$

更一般地：

$$
d b + (d-1)b^2 + \cdots + b^d
$$

为什么最后仍是 $O(b^d)$？

因为 Big-O 只看增长最快的主导项。对于 branching factor $b > 1$ 的 search tree，最深一层的 $b^d$ 通常支配前面那些较小层。

直觉：

```text
yes, IDS revisits shallow nodes
but shallow levels are cheap
the deepest level dominates the work
```

### Properties

| Property | Iterative deepening |
| --- | --- |
| Complete? | Yes, if $b$ is finite |
| Optimal? | Yes if every step cost is 1 |
| Time | $O(b^d)$ |
| Space | $O(b \cdot d)$ |

Transcript 里说 “complete because I can go to infinity”。更精确地说：

> IDS is complete when branching factor is finite and a finite-depth solution exists.

如果 $b$ 是 infinite，每一层本身都可能搜不完；如果没有 finite-depth solution，算法当然不会 magically terminate。

Main intuition:

```text
BFS gives completeness and unit-cost optimality.
DFS gives low memory.
Iterative deepening combines both for unit-cost problems.
```

This is why the lecture calls it:

> Depth-limited search + iteration = WIN.

### Choosing When to Use IDS

IDS 适合：

- action costs are uniform；
- solution depth is unknown；
- memory matters；
- we still want completeness and shallowest-depth optimality。

它不适合直接解决 arbitrary weighted shortest path，因为 “shallowest” 不一定等于 “lowest path cost”。

---

## 20 · Summary Table

| Criterion | BFS | DFS | Depth-Limited | Iterative Deepening |
| --- | --- | --- | --- | --- |
| Complete? | yes | no, not generally | no, if limit too small | yes |
| Time | $O(b^d)$ | $O(b^m)$ | $O(b^l)$ | $O(b^d)$ |
| Space | $O(b^d)$ | $O(b \cdot m)$ | $O(b \cdot l)$ | $O(b \cdot d)$ |
| Optimal? | yes, if unit cost | no | no, not generally | yes, if unit cost |

Common interpretation:

- BFS is safer but memory-heavy.
- DFS is memory-light but unreliable.
- Depth-limited search controls depth but needs a good limit.
- Iterative deepening is often best for unknown-depth, unit-cost search.

---

## 21 · Why Do We Care About Search If LLMs Exist?

The transcript makes an important point:

> Large language models are useful, but they are not naturally planning agents.

### How LLM Text Generation Works

An LLM receives a prompt and generates next tokens.

At each step it has a probability distribution over possible next words/tokens, then samples or chooses from that distribution.

This can produce fluent text, but it can also produce hallucination（幻觉）：

```text
confident sentence
-> sounds factual
-> fact may be wrong
```

The transcript's example:

- The model correctly associates Chris Callison-Burch with Penn CIS.
- It may also invent an incorrect institute/director role.

### Few-Shot and Instruction Following

LLMs can also do:

- few-shot prompting（少样本提示）：learn a pattern from examples in the prompt；
- in-context learning（上下文学习）：use the current prompt pattern；
- instruction following（遵循指令）：respond to commands like “write a biography”。

These are powerful abilities, but they are not the same as search guarantees.

### Romania Example

If we ask:

```text
What is the shortest path from Arad to Bucharest?
```

an LLM may answer correctly:

```text
Arad -> Sibiu -> Ramnicu Valcea -> Pitesti -> Bucharest
```

But the transcript emphasizes:

> It may get the right answer for the wrong reason.

Why?

Because this Romania map is famous and appears in many AI materials online. The model may have memorized the association rather than computed the shortest path.

If we rename the same graph using Star Wars planets while keeping the same edge weights, the model may fail or produce inconsistent answers.

### The Lesson

Classical search algorithms matter because they provide procedure and guarantees:

```text
given graph + costs
-> run algorithm
-> compute path
-> know when result is complete / optimal
```

An LLM can describe or assist, but by itself it does not guarantee shortest-path reasoning.

Future systems may combine:

```text
LLM interface / language reasoning
plus
classical search / planning algorithms
```

That is why this course starts with classical AI algorithms before returning to modern LLMs later.

---

## 22 · Preview: Informed Search

Uninformed search does not know which non-goal frontier node is closer to the goal.

Informed search adds domain-specific information through a heuristic function:

$$
h(n)
$$

Informally:

```text
h(n) estimates how close node n is to a goal
```

One famous informed search algorithm is A*.

The lecture connects A* historically to robot navigation and Shakey the robot at Stanford Research Institute.

For now, just remember:

```text
Module 2: uninformed search
Next: informed search with h(n)
```

---

## 23 · Common Confusions

### Confusion 1: State vs Node

Incorrect:

> A state has a parent and depth.

Correct:

> A node has parent/depth/path cost; a state is just the world configuration.

### Confusion 2: Goal Test vs Path Cost

Goal test asks:

```text
Have we reached a goal?
```

Path cost asks:

```text
Among paths that reach a goal, which is cheaper?
```

### Confusion 3: BFS Is Always Optimal

BFS is optimal only when all step costs are equal.

If one action costs 100 and another costs 1, “fewest steps” may not mean “lowest cost.”

### Confusion 4: DFS Saves Memory, So It Is Better

DFS saves memory, but it can fail in infinite-depth spaces and can return a bad solution first.

Memory efficiency is not the same as correctness guarantee.

### Confusion 5: Iterative Deepening Wastes Too Much Work

It repeats shallow levels, but shallow levels are small compared with the deepest level in an exponential tree.

That is why time remains:

$$
O(b^d)
$$

The useful sentence:

> IDS repeats cheap shallow work to avoid expensive BFS memory.

### Confusion 6: LLM Answering a Shortest Path Means It Planned

Not necessarily.

If the example is famous, the model may reproduce memorized text. To test planning, change labels or give a new graph and require exact path-cost computation.

### Confusion 7: Branching Factor Is the Same as Depth

Branching factor $b$ 是每个 state 最多能扩展出多少 successors。

Depth $d$ 是 shallowest goal 在 search tree 的层数。

Maximum depth $m$ 是 state space 中最长 path 的深度，可能远大于 $d$，也可能是 infinite。

### Confusion 8: Frontier Is the Same as Explored Set

Frontier:

```text
generated but not expanded yet
```

Explored set:

```text
already expanded
```

Graph search 需要两者都检查，避免把重复 state 再塞回 frontier。

---

## 24 · Self-Check

Try answering without reading:

1. Define a search problem using states, initial state, actions, transition model, goal test, and path cost.
2. For 8-puzzle, why are there about $9!/2$ reachable configurations rather than all $9!$?
3. In route finding, what are nodes, edges, actions, and path cost?
4. Why does graph search need an explored set?
5. What information is stored in a search node but not in a state?
6. Why is BFS complete if $b$ is finite?
7. Why is BFS space $O(b^d)$?
8. Give an example where DFS returns a non-optimal solution.
9. What goes wrong if the depth limit $l$ is smaller than $d$?
10. Why does iterative deepening have BFS-like guarantees with DFS-like space?
11. Why are LLMs not guaranteed shortest-path planners by default?
12. What does heuristic function $h(n)$ add in informed search?
13. What is the difference between $b$, $d$, and $m$?
14. Why can checking goal before queue insertion save one extra layer of BFS work?
15. In depth-limited search, what happens when $l<d$, $l=d$, and $l>d$?
16. Derive why iterative deepening constructs roughly $d b + (d-1)b^2 + \cdots + b^d$ nodes.

---

## 25 · Oral Exam Prompts

Question:

How would you formulate the 8-puzzle as a search problem?

My answer:


Verdict:


Missing:

Question:

Explain the difference between tree search and graph search.

My answer:


Verdict:


Missing:

Question:

Why does BFS find the shortest number-of-actions solution when every action has unit cost?

My answer:


Verdict:


Missing:

Question:

Why is DFS not complete in an infinite-depth state space?

My answer:


Verdict:


Missing:

Question:

Why is iterative deepening not as wasteful as it first appears?

My answer:


Verdict:


Missing:

Question:

Why might ChatGPT get the Romania shortest path right but still not be doing reliable planning?

My answer:


Verdict:


Missing:

---

## 26 · One Sentence

$$
\boxed{
\text{Search turns rational action into explicit planning: represent states/actions/costs, manage the frontier, avoid repeated states, and choose an expansion strategy with known guarantees.}
}
$$

---

## 27 · Connections

Rational Agents

-> Problem-Solving Agents
-> Search Problem Formulation
-> State Space
-> Frontier
-> Tree Search
-> Graph Search
-> BFS / DFS
-> Depth-Limited Search
-> Iterative Deepening
-> Informed Search / Heuristics
-> Planning Guarantees
