# Homework 4 · Adversarial Games

> Week 04 · Programming Assignment

Source: `hw4/homework4.pdf` and `hw4/homework4.py`.

## Quick Review First

1. `vertical=True` 时，一个 move `(row, col)` 覆盖哪两格？[[#Board and Legal Moves|答案]]
2. 为什么 `successors` 必须复制棋盘？[[#Independent Successors|答案]]
3. `get_best_move` 的 value 从谁的角度计算？[[#Evaluation Perspective|答案]]
4. `limit=2` 为什么代表两次落子，而不是两轮双方各落一次？[[#Depth and Leaf Count|答案]]
5. MAX、MIN、alpha、beta 分别做什么？[[#Alpha-Beta Search|答案]]
6. 平分时为什么保留先遇到的 move？[[#Move Order and Ties|答案]]
7. 返回的 leaf count 包含被剪掉的分支吗？[[#Depth and Leaf Count|答案]]

## Board and Legal Moves

棋盘是二维布尔列表：`False` 为空，`True` 为占用。`vertical=True` 把骨牌放在 `(row, col)` 和 `(row+1, col)`；`vertical=False` 放在 `(row, col)` 和 `(row, col+1)`。两格都在棋盘内且未占用，move 才合法。

`legal_moves` 按 row-major 顺序产出所有合法左上角：先从上到下遍历行，再从左到右遍历列。`game_over(vertical)` 只看该玩家是否还有合法 move；另一方是否还能走不影响这个判断。

## Independent Successors

每个 successor 是 `(move, new_game)`。`new_game` 的棋盘必须深拷贝到行级别，否则一个分支落子会污染其他分支。二维布尔列表可用 `[row[:] for row in board]` 复制；仅复制外层列表仍会共享内部行。

## Evaluation Perspective

搜索根节点选择的玩家固定为 MAX，其评估函数是：

```text
value(board) = legal_moves(board, root_player)
             - legal_moves(board, opponent)
```

递归中的 `turn` 每层切换，评估视角却始终是 `root_player`。如果把它改成“当前轮到谁就算谁的可走步数减对手”，MIN 层会把分数反过来，结果不再是同一个 minimax 问题。

这个作业要求在深度限制或无合法 move 时使用上述评估值。它是非终局也能使用的 heuristic，并非胜负的 `+∞/-∞` utility。

## Alpha-Beta Search

MAX 选后继 value 的最大值，MIN 选最小值。`alpha` 是 MAX 沿路径已能保证的下界；`beta` 是 MIN 已能保证的上界。若 `alpha >= beta`，后续分支不能改变祖先的选择，可以停止展开。

```text
root: MAX(vertical argument)
    child: MIN(opposite orientation)
        child: MAX(root orientation)
            ...
```

剪枝不改变 minimax 最佳 value，但会减少实际访问的叶节点数。这里的 `vertical` 是搜索根玩家；递归传入的 `turn` 才表示当前落子方向。

## Move Order and Ties

题目规定按 row-major 顺序展开。只有 `value > best_value` 才替换最佳 move；若 value 相同，保留先找到的 move。排序改变后，最佳 value 可能相同，但最佳 move 或 leaf count 可能不同。

## Depth and Leaf Count

一次落子算一层。`limit=1` 评估根玩家落子后的棋盘；`limit=2` 还展开对手的一次应对。达到深度限制，或当前玩家无合法 move，都是一个被评估的 leaf。被 alpha-beta 剪掉的分支没有被评估，不计入 leaf count。

例如空 `3 x 3` 棋盘、纵向先手：

| Limit | Best move | Value | Evaluated leaves |
| ---: | --- | ---: | ---: |
| 1 | `(0, 1)` | 2 | 6 |
| 2 | `(0, 1)` | 3 | 10 |

这两个数是题目示例，也是核对剪枝顺序的好用基准。

## Common Confusions

- `vertical` 在 `get_best_move` 中同时指定根玩家方向；递归的 `turn` 会轮换。
- 评估 value 的正负始终针对根玩家，不要在 MIN 层反转公式。
- `copy()` 要复制每一行；否则搜索会改变原棋盘。
- `limit` 是 ply 数（单次落子数），不是完整回合数。
- 平分不需要特殊排序；保留 row-major 中先出现的 move。

## Self-Check

1. 在空 `2 x 2` 棋盘，纵向玩家有几个合法 move？横向玩家呢？
2. 如果 MIN 节点已经找到 value `-2`，而祖先 MAX 已保证 `alpha=0`，为什么可以停止搜索 MIN 的剩余子节点？
3. 在一个限深搜索里，为什么 leaf count 可能小于同深度完整 minimax 的 leaf count？
