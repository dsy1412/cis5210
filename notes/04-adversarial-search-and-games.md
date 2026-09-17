# Adversarial Search and Games

> Week 04 · Module 05

Source: `Module 5 - Resources/05-Adversarial-Search.pptx.pdf`, `Module 5 - Resources/05-Alpha-Beta.pptx.pdf`, `Module 5 - Resources/05-Expectimax-and-Utilities.pptx.pdf`, the user's pasted Canvas transcripts, and the user's PPT summary Markdown for games, minimax, alpha-beta pruning, and expectimax.

This note treats the attached course materials as source material only. It records the lecture logic for learning and review.

## 00 · Quick Review First

### Read With These Questions

1. 为什么 games 比普通 single-agent search 更难？ [[#01 · Why Games Need Adversarial Search|答案]]
2. 最简单的 game environment 有哪些假设？ [[#02 · Simplest Game Environment|答案]]
3. 游戏如何 formalize 成 search problem？initial state、successor function、terminal test、utility function 分别是什么？ [[#03 · Formal Game Setup|答案]]
4. MAX node 和 MIN node 分别是什么意思？为什么这是 egocentric view？ [[#04 · MAX and MIN Nodes|答案]]
5. game tree 里的 node、edge、root、ply 分别是什么？ [[#05 · Game Trees and Ply|答案]]
6. evaluation function `f(n)` 和 terminal utility 有什么区别？ [[#06 · Evaluation Functions|答案]]
7. minimax 的核心规则是什么？为什么叫 “do not play hope chess”？ [[#07 · Minimax Rule|答案]]
8. minimax 的 backed-up value 怎么从 leaf 往 root 传？ [[#08 · Minimax Procedure|答案]]
9. alpha-beta pruning 为什么可以剪枝但不改变 minimax 结果？ [[#09 · Alpha-Beta Pruning|答案]]
10. `alpha` 和 `beta` 分别表示什么？什么时候可以 cut off？ [[#10 · Alpha and Beta Meaning|答案]]
11. expectimax 和 minimax 的区别是什么？chance node 如何计算 value？ [[#11 · Expectimax Search|答案]]
12. expected utility 为什么比 “best possible outcome” 更适合有随机性的决策？ [[#12 · Expected Utility|答案]]

### One-Minute Map

```text
single-agent search
-> choose best action sequence in a fixed problem
games
-> another agent chooses actions too
-> represent turns as MAX and MIN levels in a game tree
-> terminal states have utilities
-> nonterminal states need evaluation functions
-> minimax assumes rational adversary
-> alpha-beta prunes branches that cannot affect minimax choice
-> expectimax replaces adversary with chance / uncertainty
```

一句话记忆：

> Minimax plans against the best possible opponent; expectimax plans under average-case uncertainty.

### Professional Terms

| Term | 中文 | Quick Meaning |
| --- | --- | --- |
| Game | 游戏 | Multiagent decision problem with rules, legal moves, and outcomes |
| Adversarial Search | 对抗搜索 | Search where another agent tries to make your outcome worse |
| MAX | 最大化玩家 | The player whose utility we are computing and trying to maximize |
| MIN | 最小化玩家 | MAX's opponent, modeled as minimizing MAX's utility |
| Zero-Sum | 零和 | One player's gain is the other's loss |
| Game Tree | 游戏树 | Tree whose nodes are board positions and edges are legal moves |
| Ply | 半步 / 一层 | One player's turn in the game tree |
| Terminal State | 终局状态 | A state where the game is over |
| Utility Function | 效用函数 | Assigns numerical values to terminal states |
| Evaluation Function | 评估函数 | Estimates how good a nonterminal board position is |
| Backed-Up Value | 回传值 | Value propagated from child nodes to parent nodes |
| Minimax | 极小极大 | Choose the move with best guaranteed outcome against optimal opponent |
| Alpha-Beta Pruning | Alpha-Beta 剪枝 | Skip branches that cannot change the minimax decision |
| Alpha `alpha` | 下界 | MAX's best already guaranteed value on path to root |
| Beta `beta` | 上界 | MIN's best already guaranteed limit on path to root |
| Chance Node | 机会节点 | A node where outcome is random or uncertain |
| Expectimax | 期望最大搜索 | Like minimax, but chance nodes take expected values |
| Expected Utility | 期望效用 | Probability-weighted average utility |

---

## 01 · Why Games Need Adversarial Search

普通 search problem 里，agent 通常只需要回答：

```text
If I take this action, what state comes next?
```

Games 不一样，因为下一步不只由自己决定，还由 opponent 决定。

所以问题变成：

```text
If I move here,
what will my opponent do next,
assuming they also choose intelligently?
```

这就是 adversarial search（对抗搜索）。

核心变化：

| Single-agent search | Game search |
| --- | --- |
| environment follows transition model | opponent chooses actions |
| agent tries to reach goal | agent tries to win / maximize utility |
| path cost is central | strategic response is central |
| solution is action sequence | solution is a strategy |

一个 game-playing agent 不能只想：

> What move looks good for me now?

它还必须想：

> If I make this move, what is the best response my opponent can make?

---

## 02 · Simplest Game Environment

课程先从最简单的 game setting 开始：

- **multiagent**: 有两个玩家；
- **static**: agent 思考时 board 不会自己变化；
- **discrete**: states 和 actions 是有限、离散的；
- **fully observable**: board state 完全可见；
- **strategic**: next state 由我方 action 和对手 action 共同决定。

典型例子：

- chess;
- checkers;
- Go;
- Mancala;
- tic-tac-toe;
- Othello;
- Hexapawn.

这些游戏通常还有四个共同点：

1. Two players alternate moves.
2. Zero-sum: one player's gain is the other's loss.
3. Legal moves are clearly defined.
4. Outcomes are well-defined: win, lose, draw, or numerical score.

Hexapawn intuition:

```text
3 x 3 board
each side has pawns
pawns move forward into empty squares
pawns capture diagonally forward
```

A player wins if:

- one of their pawns reaches the opposite side;
- the opponent has no legal move;
- the opponent has no pawns left.

Hexapawn is useful because it is small enough to draw as a game tree, but still forces you to reason about the opponent's reply.

更复杂的 game 会打破这些假设：

| Complication | Example | Why harder |
| --- | --- | --- |
| stochastic outcome | dice, card games | outcome is not fully controlled by actions |
| imperfect information | poker, bridge | some state information is hidden |
| continuous / real-time | RTS games | no clean turn boundary |
| cooperative games | team games | goals may partially align |

---

## 03 · Formal Game Setup

课程用 MAX 和 MIN formalize game：

```text
MAX moves first
MAX and MIN alternate turns
game ends at terminal state
terminal state receives utility
MAX chooses move by searching the game tree
```

Game as search:

| Component | Meaning | Example |
| --- | --- | --- |
| Initial state | starting board configuration | starting chess board |
| Successor function | legal `(move, state)` pairs | legal chess moves |
| Terminal test | whether game is over | checkmate / draw / no legal move |
| Utility function | numerical value of terminal state | win = +1, loss = -1, draw = 0 |

Important distinction:

```text
normal search: find a path to a goal
game search: choose a move under opponent response
```

In games, a "solution" is not just a path. It is closer to a strategy:

```text
If opponent does A, respond with B.
If opponent does C, respond with D.
```

---

## 04 · MAX and MIN Nodes

The game tree is computed from MAX's point of view.

| Node type | Whose turn | What value is chosen |
| --- | --- | --- |
| MAX node | MAX moves | maximum child value |
| MIN node | opponent moves | minimum child value |

Why MIN takes minimum:

> MIN is not trying to minimize their own score directly in our notation; MIN is modeled as minimizing MAX's utility.

This is why the view is egocentric:

```text
all utilities are measured for MAX
MAX wants large values
MIN wants small values
```

If MAX moves first:

```text
depth 0: MAX
depth 1: MIN
depth 2: MAX
depth 3: MIN
...
```

Each level is a **ply**.

---

## 05 · Game Trees and Ply

A game tree represents possible future plays.

| Tree part | Game meaning |
| --- | --- |
| root | current board position |
| node | board position |
| edge | legal move |
| child | board after one legal move |
| leaf | either terminal state or depth-limited cutoff state |

For small games like tic-tac-toe or Hexapawn, it may be possible to draw a large part of the tree.

For games like chess, the full tree is impossible to search:

```text
branching factor is large
depth is large
full game tree explodes
```

So practical game search usually:

1. expands a fixed number of ply;
2. stops before actual terminal states;
3. uses an evaluation function on cutoff leaves;
4. backs up those values to choose a move.

---

## 06 · Evaluation Functions

A utility function gives values to terminal states.

An evaluation function estimates values for nonterminal positions.

| Function | Used when | Meaning |
| --- | --- | --- |
| utility function | terminal state | true final value |
| evaluation function `f(n)` | nonterminal / cutoff state | estimated goodness of board |

Evaluation function properties:

- based on static features of the board;
- does not care about path cost;
- returns real-number score;
- positive means good for MAX;
- negative means good for MIN;
- zero means roughly tied.

For a zero-sum game:

```text
f(n) > 0: MAX is winning
f(n) = 0: roughly tied
f(n) < 0: MIN is winning
```

Tic-tac-toe style example:

```text
f(n) =
number of open 3-lines for MAX
- number of open 3-lines for MIN
```

Chess style example:

```text
f(n) = sum(MAX piece values) - sum(MIN piece values)
```

Simple piece values often used:

| Piece | Value |
| --- | ---: |
| pawn | 1 |
| knight | 3 |
| bishop | 3.25 |
| rook | 5 |
| queen | 9 |

More advanced chess systems use many positional features:

- control of center;
- rook on open file;
- developed pieces;
- isolated pawns;
- pinned pieces;
- king safety.

Key idea:

> A good-looking board is not enough if the opponent has a strong reply.

That is exactly why minimax is needed.

Do not confuse this `f(n)` with A* search:

```text
A*: f(n) = g(n) + h(n)
    estimates total path cost through node n

game evaluation: f(n)
    estimates how good a board position is for MAX
```

They share the symbol `f(n)`, but they answer different questions.

---

## 07 · Minimax Rule

Minimax says:

> Choose the move that gives MAX the best outcome assuming MIN always replies optimally.

The lecture phrase is:

> Do not play hope chess.

Meaning:

```text
bad reasoning:
I hope my opponent misses the best response.

minimax reasoning:
Assume my opponent finds the best response.
Choose the move that survives that assumption.
```

At each node:

```text
MAX node value = max(child values)
MIN node value = min(child values)
```

So minimax computes:

```text
best achievable utility
against a rational optimal adversary
```

---

## 08 · Minimax Procedure

The minimax procedure:

1. Start with current position as a MAX node.
2. Expand game tree for a fixed number of ply.
3. Apply evaluation function to leaf positions.
4. Back up values bottom-up.
5. Choose the root move with the best backed-up value.
6. Wait for MIN to respond.
7. Repeat from the new board state.

Recursive form:

```text
max-value(state):
    if state is terminal:
        return utility(state)
    v = -infinity
    for successor in successors(state):
        v = max(v, min-value(successor))
    return v

min-value(state):
    if state is terminal:
        return utility(state)
    v = +infinity
    for successor in successors(state):
        v = min(v, max-value(successor))
    return v
```

The backed-up value is not always the best leaf under that node.

It is:

```text
what MAX can guarantee
if MIN responds optimally
```

This is the big conceptual difference between greedy game play and minimax.

---

## 09 · Alpha-Beta Pruning

Alpha-beta pruning is an optimization of minimax.

It does **not** change the minimax answer.

It only avoids evaluating branches that cannot affect the final choice.

Intuition:

```text
If MAX already has a move worth at least 3,
and another branch can be forced by MIN to be at most 2,
MAX will never choose that branch.
Stop searching it.
```

Pruning is safe because once a branch is provably irrelevant to the root decision, its exact value no longer matters.

The important promise:

```text
alpha-beta returns the same move as minimax
with fewer node evaluations
```

---

## 10 · Alpha and Beta Meaning

Alpha and beta summarize what is already known on the path to the root.

| Symbol | Intuition | Meaning |
| --- | --- | --- |
| `alpha` | "at least" | MAX's current best guaranteed lower bound |
| `beta` | "at most" | MIN's current best upper bound on MAX's outcome |

Common memory:

```text
alpha = MAX's best option so far
beta = MIN's best option so far
```

Cutoff rule:

```text
if alpha >= beta:
    prune
```

Why?

- MAX already has an option at least as good as `alpha`.
- MIN can force this branch to be no better than `beta`.
- If `beta <= alpha`, this branch cannot improve MAX's root choice.

Alpha-beta is most effective when good moves are searched first.

Best ordering:

```text
near O(b^(d/2)) effective behavior
```

Worst ordering:

```text
same as minimax: O(b^d)
```

The course emphasis here is conceptual:

> Pruning removes work, not correctness.

---

## 11 · Expectimax Search

Minimax assumes the next non-MAX actor is adversarial and optimal.

Expectimax handles uncertainty.

Uncertainty can come from:

- explicit randomness, such as dice;
- unpredictable opponents;
- actions that can fail;
- stochastic environment effects.

Node types:

| Node type | Backup rule |
| --- | --- |
| MAX node | maximum child value |
| chance node / EXP node | probability-weighted average of child values |

Recursive idea:

```text
value(state):
    if terminal:
        return utility(state)
    if next agent is MAX:
        return max-value(state)
    if next agent is EXP:
        return exp-value(state)

exp-value(state):
    v = 0
    for successor in successors(state):
        p = probability(successor)
        v += p * value(successor)
    return v
```

Example:

```text
successor utilities: 8, 24, -12
probabilities:       1/2, 1/3, 1/6

expected value =
(1/2) * 8 + (1/3) * 24 + (1/6) * (-12)
= 4 + 8 - 2
= 10
```

Expectimax values average-case outcomes.

Minimax values worst-case adversarial outcomes.

Same leaves, different meaning:

```text
if children are MIN choices:
    MIN picks -12

if children are chance outcomes with the probabilities above:
    chance node returns 10
```

The difference is not arithmetic style. It is a modeling assumption about who or what determines the next state.

---

## 12 · Expected Utility

Expected utility says:

```text
choose the action with the highest probability-weighted utility
```

Formula:

$$
EU(a)=\sum_s P(s \mid a)U(s)
$$

where:

| Symbol | Meaning |
| --- | --- |
| `a` | action |
| `s` | possible outcome state |
| `P(s given a)` | probability of outcome `s` after action `a` |
| `U(s)` | utility of outcome `s` |

Why expected utility matters:

```text
best possible outcome can be misleading
worst possible outcome can be too conservative
expected value accounts for probability
```

This connects AI game search to everyday decisions:

- risk;
- uncertainty;
- partial information;
- actions with probabilistic outcomes.

---

## 13 · Minimax vs Expectimax

| Question | Minimax | Expectimax |
| --- | --- | --- |
| What is the non-MAX node? | rational adversary | chance / uncertainty |
| Backup rule | min child value | weighted average |
| Assumption | opponent chooses worst for MAX | outcomes follow probabilities |
| Good for | chess-like adversarial games | dice, stochastic actions, random ghosts |
| Risk attitude | pessimistic / worst-case | average-case |

Do not use expectimax when:

```text
the opponent is truly adversarial and optimal
```

Do not use minimax when:

```text
the next event is random rather than strategic
```

---

## 14 · Common Confusions

### Confusion 1 - Evaluation Function vs Utility Function

Utility is for terminal states.

Evaluation is for nonterminal states when search is cut off.

### Confusion 2 - MIN Has Negative Utility

In this setup, utilities are measured from MAX's viewpoint.

MIN chooses the child that minimizes MAX's value.

### Confusion 3 - Minimax Predicts What Opponent Will Actually Do

Minimax does not predict human psychology.

It assumes rational optimal play and chooses a robust move under that assumption.

### Confusion 4 - Alpha-Beta Changes the Answer

Alpha-beta pruning does not change the minimax value.

It only avoids computing irrelevant branches.

### Confusion 5 - Expectimax Is Just Minimax with Different Name

Expectimax changes the backup rule at uncertainty nodes:

```text
minimax MIN node: minimum
expectimax chance node: expected value
```

### Confusion 6 - Highest Possible Reward Is Best

Not under uncertainty.

A huge reward with tiny probability may have lower expected utility than a moderate reward with high probability.

---

## 15 · Self-Check

1. In a game tree, label depths 0 through 5 as MAX or MIN if MAX moves first.
2. Given leaf values `3, 8, 2` under a MIN node, what value backs up?
3. Given child values `2, 5, 1` under a MAX node, what value backs up?
4. Explain why minimax is more conservative than greedy evaluation.
5. Explain why alpha-beta can prune a branch whose exact value is unknown.
6. In your own words, explain `alpha` as "at least" and `beta` as "at most."
7. Compute the expected value of outcomes `10, 0, -6` with probabilities `0.2, 0.5, 0.3`.
8. Give one game where minimax is appropriate and one where expectimax is more appropriate.

---

## 16 · Oral Exam Prompts

Question:

How do games differ from ordinary search problems?

Question:

Why does minimax assume the opponent will make the move that is worst for MAX?

Question:

What is a backed-up value in a minimax tree?

Question:

What is the difference between a utility function and an evaluation function?

Question:

Why does alpha-beta pruning preserve the minimax result?

Question:

What do `alpha` and `beta` mean?

Question:

When should expectimax be used instead of minimax?

Question:

How does expected utility combine probability and value?

---

## 17 · One Sentence

Adversarial search models games as turn-taking search trees where MAX chooses moves under assumptions about MIN, alpha-beta removes branches that cannot affect the minimax decision, and expectimax replaces adversarial choice with probability-weighted uncertainty.

---

## 18 · Connections

- Builds on [[02-search-problems|Search Problems]]: state, action, successor, terminal test.
- Builds on [[03-informed-search|Informed Search]]: evaluation functions guide search when full search is impossible.
- Prepares for future decision-making topics: uncertainty, utility, expected value, and Markov Decision Processes.
- Important bridge: minimax / alpha-beta still search trees; expectimax starts moving toward probabilistic decision-making.
