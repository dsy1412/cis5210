# Homework 2 · Uninformed Search

> Week 02 · Programming Assignment

Source: CIS5210 Homework 2 (`hw2/homework2.pdf`) and the completed `hw2/homework2.py`.

这份作业把 Module 2 的 search concepts 变成代码：

```text
problem formulation
-> state representation
-> successor generation
-> frontier
-> explored set
-> optimal solution by BFS
```

核心不是背 BFS，而是知道：

> 一个 puzzle 要能被 search algorithm 解决，必须先把 state、actions、transition、goal test、path cost 表示清楚。

## 00 · Quick Review First

### Read With These Questions

1. N-Queens 为什么可以用 row-by-row representation，而不是存整个棋盘？[答案](#board-representation)
2. diagonal constraint 怎么用 row difference 和 column difference 判断？[答案](#validity-check)
3. DFS / backtracking 在 N-Queens 中什么时候 append partial board，什么时候回退？[答案](#dfs--backtracking)
4. Lights Out 的 state 为什么最好转成 hashable representation 再放进 visited set？[答案](#state-representation)
5. toggle 一个 cell 时，哪些 neighbor 会变化？边界如何处理？[答案](#move--transition)
6. BFS solver 里 frontier 存的是 state 还是 path？如何返回 move sequence？[答案](#bfs-solver)
7. identical disks 和 distinct disks 的 goal test 有什么不同？[答案](#04--linear-disk-movement)
8. disk movement 里 slide move 和 jump move 的合法条件是什么？[答案](#disk-successors)
9. 为什么这些 puzzle solver 用 BFS 能保证 shortest move sequence？[答案](#why-bfs)
10. state representation 选错会造成哪些 bug：重复 state、mutating visited、path 丢失？[答案](#05--common-mistakes)

### One-Minute Map

```text
formulate puzzle as search
-> choose compact state representation
-> generate legal successors
-> avoid repeated states
-> BFS returns shortest path for unit-cost puzzles
-> DFS/backtracking enumerates structured solutions
```

一句话记忆：

> HW2 is where search becomes code: correctness mostly depends on clean states and exact successor generation.

### Professional Terms

| Term | 中文 | Quick Meaning |
| --- | --- | --- |
| N-Queens | N 皇后 | place queens so none attack each other |
| Backtracking | 回溯 | DFS that undoes choices after exploring them |
| Partial Board | 部分棋盘 | only first few rows / placements assigned |
| Diagonal Constraint | 对角线约束 | queens conflict when row and column differences match |
| Lights Out | 灭灯游戏 | toggling cells to make all lights off |
| Toggle | 翻转 | change `True` to `False` or reverse |
| Successor Generation | 后继生成 | list all legal next states and moves |
| Deep Copy | 深拷贝 | copy nested structure before mutation |
| Hashable State | 可哈希状态 | immutable representation usable in visited set |
| BFS Graph Search | BFS 图搜索 | FIFO frontier plus visited set |
| Identical Disks | 相同圆盘 | disks have no individual labels |
| Distinct Disks | 不同圆盘 | disks have identities and target reversed order |
| Slide Move | 平移一步 | move disk into adjacent empty slot |
| Jump Move | 跳跃一步 | jump over one occupied slot into empty slot |
| Frontier | 边界队列 | states/paths waiting to be expanded |
| Optimal Solution | 最优解 | shortest move sequence under unit step cost |

---

## 01 · 作业结构

| Section | Main idea | Algorithm |
| --- | --- | --- |
| N-Queens | place queens row by row | DFS / backtracking |
| Lights Out | toggle lights to reach all-off board | BFS graph search |
| Identical disks | move indistinguishable disks to the end | BFS graph search |
| Distinct disks | move labeled disks to reversed target order | BFS graph search |

为什么有 DFS 也有 BFS？

- N-Queens 要 enumerate all valid solutions，所以 DFS/backtracking 很自然。
- Lights Out / disks 要 optimal solution（最短 moves），所以用 BFS。

---

## 02 · N-Queens

### Counting Placements

Without chess constraints, placing $n$ indistinguishable queens on an $n \times n$ board:

$$
\binom{n^2}{n}
$$

因为是在 $n^2$ 个格子里选 $n$ 个位置。

If each row must contain exactly one queen:

$$
n^n
$$

因为每一行有 $n$ 个 column choices，一共 $n$ 行。

这个 restriction 合理，是因为合法 N-Queens solution 本来就不可能有两只 queen 在同一 row。

<a id="board-representation"></a>

### Board Representation

作业用 list 表示 board：

```python
[1, 3, 5, 0, 2, 4]
```

含义：

```text
row 0 -> col 1
row 1 -> col 3
row 2 -> col 5
...
```

Partial board 也用同样表示：

```python
[0, 3, 1]
```

表示前 3 行已经放好 queen。

<a id="validity-check"></a>

### Validity Check

两只 queen 会互相攻击，如果：

- same column；
- same diagonal。

对于位置 `(row, col)`：

```text
down diagonal: row - col
up diagonal: row + col
```

所以检查时维护 3 个 set：

```python
seen_cols
seen_diag_down
seen_diag_up
```

如果新 queen 的 column 或 diagonal 已出现，就 invalid。

<a id="dfs--backtracking"></a>

### DFS / Backtracking

搜索方式：

```text
start with empty board
try every column in next row
keep candidate only if still valid
recurse
when length == n, yield complete solution
```

这就是 depth-first search，因为它先把一个 partial placement 继续往深处扩展。

---

## 03 · Lights Out

<a id="state-representation"></a>

### State Representation

Puzzle board 是 2D list of booleans：

```python
True  = light on
False = light off
```

但是 list 不能放进 set，所以 BFS duplicate checking 要转换成 tuple of tuples：

```python
tuple(tuple(row) for row in board)
```

这和 HW1 的 hashable concept 连在一起：

```text
mutable list -> not hashable
immutable tuple -> hashable if elements are hashable
```

<a id="move--transition"></a>

### Move / Transition

`perform_move(row, col)` toggles:

- selected cell；
- up neighbor；
- down neighbor；
- left neighbor；
- right neighbor。

边界外的 neighbor 直接忽略。

### Successors

每个 possible move 都生成一个 new puzzle：

```text
for every row, col:
    copy current puzzle
    perform move on copy
    yield ((row, col), new_puzzle)
```

必须用 copy，不能直接改当前 puzzle，否则 successor generation 会污染原状态。

<a id="bfs-solver"></a>

### BFS Solver

`find_solution` 用 BFS graph search：

```text
frontier = queue of (puzzle, path)
visited = set of board tuples

while frontier not empty:
    pop oldest puzzle
    for each successor:
        if not visited:
            if solved, return path + [move]
            add to visited and frontier
```

BFS 为什么能返回 optimal solution？

因为每个 move 的 cost 都是 1，所以最先到达 solved board 的 path 是最少 move 数。

如果 board 不可解，frontier 最后会空，返回 `None`。

---

<a id="04--linear-disk-movement"></a>

## 04 · Linear Disk Movement

### Rules

一排 `length` 个 cells，前 `n` 个有 disks。

每步可以：

- move to adjacent empty cell；
- jump two cells into empty cell if the intervening cell has a disk。

Moves can go both directions.

### Identical Disks

Identical disks 不区分编号。

Representation:

```python
1 = disk
0 = empty
```

Start:

```text
111000
```

Goal:

```text
000111
```

用 tuple 存 state，方便放进 visited set。

### Distinct Disks

Distinct disks 要保留 disk identity。

Representation:

```python
0, 1, 2, ... = labeled disks
-1 = empty
```

For `length = 5, n = 3`:

```text
start: (0, 1, 2, -1, -1)
goal:  (-1, -1, 2, 1, 0)
```

目标顺序是 reversed，因为第一个 disk 要去最右边，第二个去倒数第二个，以此类推。

<a id="disk-successors"></a>

### Disk Successors

对每个 disk，尝试 4 种 step：

```text
+1, -1, +2, -2
```

合法条件：

- target 在边界内；
- target 是 empty；
- 如果跳两格，中间 cell 必须有 disk。

每个合法 move 产生：

```text
((from, to), next_state)
```

<a id="why-bfs"></a>

### Why BFS

题目要求 optimal solution，也就是最少 moves。

每个 disk move 的 cost 都是 1，因此 BFS 第一次到达 goal 时就是 shortest solution。

---

<a id="05--common-mistakes"></a>

## 05 · Common Mistakes

1. N-Queens 忘记 diagonal，只检查 column。
2. 把 diagonal 写成 `abs(row - col)`，会把不同 diagonal 混在一起；应该用 `row - col` 和 `row + col`。
3. Lights Out successor 直接修改原 puzzle，导致后面的 successors 都不对。
4. 用 list board 放进 `visited`，会 `TypeError: unhashable type: 'list'`。
5. BFS 只检查 explored，不检查 frontier，可能把重复 state 加入队列。
6. Lights Out solved state 应该是 all `False`，不是 all `True`。
7. Disk puzzle 只允许向右移动，会错过 distinct disks 需要的反向 moves。
8. Disk jump 忘记检查 intervening cell 是否有 disk。
9. Distinct disks 的 goal 写成同顺序，而不是 reversed order。
10. 用 DFS 解 optimal shortest-path 问题，可能先返回非最短解。

---

## 06 · Complexity Intuition

### N-Queens

没有 row restriction：

$$
\binom{n^2}{n}
$$

有 one queen per row：

$$
n^n
$$

再加上 validity pruning，DFS 会提前剪掉很多 invalid partial boards。

### BFS Puzzles

BFS 的核心代价来自 state space：

```text
number of reachable states
times
cost to generate successors
```

Lights Out 的 board 有 $rows \times cols$ 个 boolean lights，所以理论配置数最多：

$$
2^{rows \cdot cols}
$$

Disk puzzles 的状态数也随 `length` 和 `n` 增长很快，所以 BFS 适合这些小 puzzle，但不适合无限扩大。

---

## 07 · Self-Check

不看代码，试着回答：

1. 为什么 `num_placements_all(n)` 是 $\binom{n^2}{n}$？
2. 为什么 one queen per row 后是 $n^n$？
3. N-Queens 里 `row - col` 和 `row + col` 分别表示什么？
4. Lights Out 为什么要把 board 转成 tuple of tuples？
5. `perform_move(0, 0)` 在角落会 toggle 哪几个 cells？
6. 为什么 `successors()` 必须返回 copy 后的新 puzzle？
7. BFS 里的 frontier 存 `(state, path)` 有什么好处？
8. Lights Out 不可解时为什么返回 `None`？
9. Identical disks 和 distinct disks 的 state representation 有什么区别？
10. Distinct disks 为什么目标是 reversed order？
11. 为什么 disk puzzle moves 必须允许左右两个方向？
12. 为什么这些 puzzle 的 optimal solver 用 BFS 而不是 DFS？

---

## 08 · One Sentence

$$
\boxed{
\text{HW2 的本质是：把每个 puzzle 变成 hashable state + legal successors，然后用 DFS 枚举或 BFS 找最短路径。}
}
$$
