# Homework 1 Python, Agents, and Search Review

> Week 01 · Homework / Quiz Review

Source: user's pasted homework review notes. This note is organized by concept, not by quiz question.

This is a practical review note. It focuses on Python details and early AI concepts that are likely to appear in homework, quizzes, or coding tasks.

## 00 · Quick Review First

### Read With These Questions

1. class、instance、attribute、method 之间是什么关系？[答案](#class-instance-attribute-method)
2. `==` 和 `is` 分别比较什么？aliasing 为什么会让 bug 难发现？[答案](#vs-is)
3. graph search 里为什么常用 `deque`、`heapq`、`set`、predecessor map？[答案](#06--data-structures-for-graph-search)
4. BFS / DFS / best-first search 的 frontier 数据结构分别是什么？[答案](#frontier-bfs-vs-dfs-vs-best-first)
5. table-driven agent 为什么理论上简单、实践上不可扩展？[答案](#table-driven-agent)
6. reflex / model-based / goal-based / utility-based / learning agent 的区别是什么？[答案](#reflex-goal-utility-and-learning-agents)
7. PEAS 四个字母分别设计什么？[答案](#peas)
8. fully observable、deterministic、episodic、static、discrete、single-agent 这些维度各自问的是什么？[答案](#09--environment-properties)
9. rationality 为什么不是 omniscience？坏结果一定说明 agent 不 rational 吗？[答案](#10--rationality-and-bad-outcomes)
10. mortgage approval AI 的 bias 和 transparency 问题，分别来自哪里？[答案](#11--ethics-mortgage-approval-ai)

### One-Minute Map

```text
Python objects and data structures
-> search implementation patterns
-> agent architecture
-> PEAS task environment
-> rationality under uncertainty
-> ethics of automated decisions
```

一句话记忆：

> This note connects Python mechanics to AI design: data representation choices become agent behavior choices.

### Professional Terms

| Term | 中文 | Quick Meaning |
| --- | --- | --- |
| Class | 类 | blueprint for objects |
| Instance | 实例 | concrete object created from a class |
| Attribute | 属性 | data stored on an object |
| Method | 方法 | function defined inside a class |
| Object Identity | 对象身份 | whether two names refer to the same object |
| Aliasing | 别名 | multiple references to one mutable object |
| `deque` | 双端队列 | efficient FIFO queue for BFS |
| `heapq` | 堆队列 | priority queue for best-first / A* |
| Visited Set | 已访问集合 | stores states already seen |
| Predecessor Map | 前驱映射 | reconstructs solution path |
| Table-Driven Agent | 查表 agent | maps percept sequences directly to actions |
| Model-Based Reflex Agent | 基于模型反射 agent | keeps internal state about the world |
| Goal-Based Agent | 目标型 agent | chooses actions to reach goals |
| Utility-Based Agent | 效用型 agent | compares how desirable outcomes are |
| Learning Agent | 学习型 agent | improves behavior from experience |
| PEAS | 性能/环境/执行器/传感器 | task-environment design framework |
| Rationality | 理性 | maximizes expected performance given available evidence |
| Omniscience | 全知 | knowing actual outcomes in advance |
| Bias | 偏见 | systematic unfairness in data or decisions |
| Transparency | 透明性 | ability to explain decision factors and process |

## 01 · Big Picture

这份作业补充把两条线连在一起：

```text
Python mechanics
-> data structures
-> graph search implementation
-> agent design
-> task environment
-> rationality and ethics
```

核心目标不是背术语，而是能回答：

> 如果我要实现一个 rational agent 或 graph search，我应该如何表示数据、选择数据结构、避免 Python 常见坑？

---

## 02 · Python Objects and Classes

<a name="class-instance-attribute-method"></a>

### Class, Instance, Attribute, Method

Simple explanation:

> class 是创建对象的 blueprint；instance 是由 class 创建出来的具体 object；attribute 是 object 里存的数据；method 是 class 里定义的 function，通常作用在 instance 上。

Example:

```python
class Dog:
    def bark(self):
        print("Woof")
```

Here:

- `Dog` is a class.
- A specific dog object is an instance.
- `bark` is a method.
- Data stored inside an object is an attribute.

Comparison:

| Term | Meaning |
| --- | --- |
| class | blueprint used to create objects |
| instance | object created from a class |
| attribute | data stored in an object |
| method | function defined inside a class |

### Dynamic Typing

Python is dynamically typed（动态类型）.

Example:

```python
x = "hello"
x = 7
print(x + 1)
```

Output:

```text
8
```

The variable name `x` can first refer to a string and later refer to an integer.

Important idea:

> The variable name is rebound to another object.

### Mutable vs Immutable

Mutable（可变）means an object can be changed in place.

Immutable（不可变）means an object cannot be changed in place.

| Type | Mutable? | Example |
| --- | --- | --- |
| list | yes | `xs.append(3)` changes the same list |
| dict | yes | `counts[word] = 1` changes the same dict |
| string | no | `s + char` creates a new string |
| int | no | assigning a new number rebinds the name |
| tuple | no | tuple contents cannot be changed in place |

### Aliasing

Aliasing（别名）means two variable names refer to the same object.

Example:

```python
x = [3, 11, 18, 29]
y = x
x.append(26)
```

After this:

```python
x == [3, 11, 18, 29, 26]
y == [3, 11, 18, 29, 26]
```

Why?

> `x` and `y` point to the same list object.

<a name="vs-is"></a>

### `==` vs `is`

This is a frequent Python confusion.

| Operator | Checks |
| --- | --- |
| `==` | value equality |
| `is` | object identity |

Example:

```python
a = [1, 2]
b = [1, 2]

a == b  # True
a is b  # False
```

The contents are equal, but they are two different list objects.

If:

```python
b = a
```

then:

```python
a == b  # True
a is b  # True
```

because both names refer to the same object.

---

## 03 · Python Sequences and Strings

### Slicing

Python slicing uses:

```python
sequence[start:stop:step]
```

Important rule:

> `start` is included, but `stop` is not included.

Example:

```python
xs = [28, 22, 4, 21, 25, 14]
xs[:3]
```

Result:

```python
[28, 22, 4]
```

It takes indices `0, 1, 2`, but not index `3`.

Memory:

$$
\boxed{\text{Python slices are left-closed, right-open intervals.}}
$$

For:

```python
xs[a:b]
```

the number of selected elements is usually:

$$
b-a
$$

### List Comprehension

General form:

```python
[expression for item in sequence if condition]
```

Example:

```python
nums = [3, 10, 7, 4, 2, 6]
result = [2 * x for x in nums if x > 5]
```

Step by step:

```text
filter: 10, 7, 6
multiply by 2: 20, 14, 12
```

So:

```python
result == [20, 14, 12]
```

### String Immutability and `join`

Python strings are immutable（不可变）.

If we repeatedly do:

```python
s = s + char
```

Python creates a new string each time and copies old content.

If the final string has length $n$, total copying is roughly:

$$
1+2+3+\cdots+n
$$

So repeated concatenation in a loop can be:

$$
O(n^2)
$$

Better pattern:

```python
pieces = []
for char in chars:
    pieces.append(char)

s = "".join(pieces)
```

---

## 04 · Dictionaries, Hashability, and Counting

### `dict.get`

Common counting pattern:

```python
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
```

Meaning:

```python
counts.get(word, 0)
```

returns:

- current value if `word` exists;
- otherwise `0`.

This avoids `KeyError`.

### Hashable Objects

Dictionary keys and set members must be hashable（可哈希）.

Common hashable objects:

- `int`
- `str`
- tuple of hashable values

Not hashable:

- list

For graph states, use:

```python
node = (2, 3)
```

instead of:

```python
node = [2, 3]
```

Why this matters:

> Graph search often stores nodes in `visited` sets and `pred` dictionaries.

### Tally Class

Goal:

> Create a class that counts how many times each item has been added.

Requirements:

- `count(item)` returns `0` if the item has never appeared.
- Different `Tally` instances keep separate data.
- Any hashable object can be used as an item.
- `total()` returns total number of added items.

Implementation:

```python
class Tally:
    def __init__(self):
        self.counts = {}
        self._total = 0

    def add(self, item):
        self.counts[item] = self.counts.get(item, 0) + 1
        self._total += 1

    def count(self, item):
        return self.counts.get(item, 0)

    def total(self):
        return self._total
```

Important:

> Do not leave `raise NotImplementedError` inside completed methods.

---

## 05 · Development Tools

IDE means Integrated Development Environment（集成开发环境）.

An IDE combines tools such as:

- code editor
- debugger
- syntax highlighting
- project navigation

Examples:

- VS Code
- PyCharm

Comparison:

| Tool | Meaning |
| --- | --- |
| `pip` | package manager |
| Jupyter Notebook | notebook environment |
| REPL | Read-Eval-Print Loop |
| IDE | complete development environment |

---

<a name="06--data-structures-for-graph-search"></a>

## 06 · Data Structures for Graph Search

A graph-search algorithm usually needs:

1. frontier（边界 / 待探索节点）
2. visited set（已访问集合）
3. predecessor map（前驱映射）

<a name="frontier-bfs-vs-dfs-vs-best-first"></a>

### Frontier: BFS vs DFS vs Best-First

| Search | Removes | Python Structure | Key Operations | Cost |
| --- | --- | --- | --- | --- |
| BFS | oldest node first | `collections.deque` | `append`, `popleft` | $O(1)$ |
| DFS | newest node first | `list` as stack | `append`, `pop` | $O(1)$ average |
| Best-first | lowest priority / cost | `heapq` with list | `heappush`, `heappop` | $O(\log n)$ |

BFS:

```python
from collections import deque

frontier = deque()
frontier.append(start)
node = frontier.popleft()
```

Why not use list with `pop(0)`?

> Removing the first element of a Python list shifts remaining elements, so it costs $O(n)$.

DFS:

```python
frontier = []
frontier.append(start)
node = frontier.pop()
```

Best-first search:

```python
import heapq

frontier = []
heapq.heappush(frontier, (priority, node))
priority, node = heapq.heappop(frontier)
```

A normal list is worse for best-first search because finding the minimum may require:

$$
O(n)
$$

### Visited Set

Use a `set`:

```python
visited = set()
visited.add(node)

if node in visited:
    ...
```

Average cost:

$$
O(1)
$$

Why not use a list?

> Checking membership in a list is $O(n)$, and graph search may do membership checks many times.

### Predecessor Map

Use a `dict`:

```python
pred[child] = parent
```

Dictionary lookup and insertion are:

$$
O(1)
$$

This helps rebuild the final path:

```text
goal -> parent -> parent -> ... -> start
```

---

## 07 · Agent Types

<a name="table-driven-agent"></a>

### Table-Driven Agent

A table-driven agent stores:

```text
entire percept sequence -> action
```

Important requirement:

> The complete percept sequence must match. A prefix is not enough.

Simple logic:

```python
def table_driven_agent(percept_history, table):
    for percept_sequence, action in table:
        if percept_sequence == percept_history:
            return action
    return None
```

Important characteristics:

- order matters;
- the whole history must match;
- empty history may match an empty sequence;
- do not modify `percept_history`;
- do not modify `table`.

Main problem:

> Table-driven agents do not scale because the table grows very quickly as percept history becomes longer.

<a name="reflex-goal-utility-and-learning-agents"></a>

### Reflex, Goal, Utility, and Learning Agents

| Agent Type | Simple Explanation | Example |
| --- | --- | --- |
| Simple Reflex Agent | acts only from current percept | `if dirty: suck` |
| Model-Based Reflex Agent | keeps internal state / model | remembers which rooms were cleaned |
| Goal-Based Agent | chooses actions that help reach a goal | plans route to loading dock |
| Utility-Based Agent | chooses the best option among possible goal-reaching actions | balances speed, battery, collision risk |
| Learning Agent | improves behavior using experience | delivery robot adjusts routes from travel-time data |

### Goal-Based vs Utility-Based

Goal-based:

> Can I reach the goal?

Utility-based:

> Which successful option is better?

Example:

```text
goal-based route choice:
Does this route reach the destination?

utility-based route choice:
Which route balances speed, safety, battery use, and comfort best?
```

### Learning Agent Components

Important components:

- performance element
- learning element
- critic

Example:

> A delivery robot records actual travel times and changes future route decisions based on experience.

---

## 08 · Rational Agent Design Process

Useful process:

1. Define the task environment using PEAS.
2. Identify environment properties.
3. Choose an appropriate agent type.
4. Implement the agent function.
5. Evaluate performance.
6. Improve the design based on evaluation.

Not every implementation detail belongs to the high-level design process.

For example:

- training a neural network;
- compiling code into a binary.

These may be implementation choices, but they are not the main abstract design steps.

<a name="peas"></a>

### PEAS

PEAS means:

$$
\boxed{
\text{Performance, Environment, Actuators, Sensors}
}
$$

For a self-driving taxi:

| Component | Examples |
| --- | --- |
| Performance | safe, fast, comfortable, legal |
| Environment | roads, traffic, pedestrians |
| Actuators | steering, brakes, accelerator |
| Sensors | cameras, GPS, LiDAR |

### Autonomous Taxi Design

Step 1: Define PEAS.

| Component | Examples |
| --- | --- |
| Performance | safe driving, timely arrival, passenger satisfaction |
| Environment | city roads, pedestrians, other vehicles |
| Actuators | steering, braking, acceleration |
| Sensors | cameras, GPS, LiDAR |

Step 2: Classify the environment.

Likely:

- partially observable;
- stochastic;
- sequential;
- dynamic;
- continuous;
- multi-agent.

Step 3: Choose an agent type.

> A Utility-Based Agent is useful because it must balance safety, travel time, and passenger comfort.

Step 4: Implement the agent function.

> Use sensor inputs and an internal model to choose driving actions.

Step 5: Evaluate performance.

Possible measures:

- safety record;
- average trip time;
- passenger ratings.

Step 6: Improve the design.

> Adjust utility weights and decision logic based on failure cases.

---

<a name="09--environment-properties"></a>

## 09 · Environment Properties

### Fully Observable vs Partially Observable

Fully observable:

> The agent has all important information needed to make a decision.

Example:

> Crossword puzzle with the whole grid and clues visible.

Partially observable:

> The agent cannot observe the complete state.

Example:

> A vacuum agent that only knows whether its current room is dirty. It cannot see the other room.

### Deterministic vs Stochastic

Deterministic:

> The result of an action is known and fixed.

Example:

> In a simple vacuum world, moving left always moves left.

Stochastic:

> An action may have uncertain outcomes.

Example:

> Real-world driving.

### Episodic vs Sequential

Episodic:

> Each decision is mostly independent of previous decisions.

Sequential:

> Current actions affect future states and future decisions.

Examples:

- Graph search is sequential.
- Driving is usually sequential.

### Static vs Dynamic vs Semidynamic

Static:

> The world does not change while the agent is deciding.

Dynamic:

> The world may change while the agent is thinking.

Semidynamic:

> The environment may stay the same, but performance changes with time.

Example:

> Chess with a clock.

### Discrete vs Continuous

Discrete:

> States or actions come from a finite or countable set.

Examples:

- crossword puzzle
- simple vacuum world

Continuous:

> Variables such as position, speed, or time can take continuous values.

Example:

> Real-world driving.

### Single-Agent vs Multi-Agent

Single-agent:

> Only one decision-making agent matters.

Example:

> Crossword puzzle.

Multi-agent:

> Other agents also make decisions and may have their own goals.

Example:

> Driving with other cars.

### Example Classifications

Crossword puzzle:

- fully observable;
- single-agent;
- deterministic;
- sequential;
- static;
- discrete.

Reason:

> The full puzzle is visible, only one solver acts, writing a letter has a predictable effect, earlier choices affect later choices, and the puzzle does not change by itself.

Simple vacuum world:

- partially observable;
- single-agent;
- deterministic;
- sequential;
- static;
- discrete.

Reason:

> The vacuum only sees the current room, only one agent exists, actions have fixed results, earlier actions affect later states, the environment does not change by itself, and states/actions are discrete.

---

<a name="10--rationality-and-bad-outcomes"></a>

## 10 · Rationality and Bad Outcomes

A rational agent is not the same as an omniscient agent.

Omniscience（全知）means:

> knowing the actual future outcome.

Rationality means:

> choosing the best action based on available information.

Therefore:

$$
\boxed{
\text{Rationality does not mean guaranteed success.}
}
$$

Example:

```text
autonomous car enters an intersection on green light
-> another car suddenly runs a red light
-> accident happens
```

If the autonomous car could not physically stop in time, entering the intersection may still have been rational based on the information available before the accident.

Important idea:

> A bad outcome does not automatically mean the earlier decision was irrational.

---

<a name="11--ethics-mortgage-approval-ai"></a>

## 11 · Ethics: Mortgage Approval AI

Scenario:

> A bank uses AI to automatically approve or deny mortgage applications using income, credit score, zip code, employment history, and 10 years of historical lending data.

Two major ethical concerns are bias（偏见）and transparency（透明度）.

### Bias

Historical data may contain unfair patterns from previous lending decisions.

The AI system can learn and repeat those patterns.

Zip code is especially risky because it may act as a proxy for demographic information.

Possible consequences:

- some neighborhoods receive lower approval rates;
- some demographic groups are unfairly disadvantaged;
- old discrimination is repeated by the model.

Mitigation:

- compare approval rates across groups;
- audit the model for bias;
- review features that may act as proxies for protected characteristics;
- remove or limit problematic features when necessary.

Stakeholders:

- applicants want fair access to loans;
- the bank wants accurate decisions and wants to avoid discrimination, lawsuits, and loss of trust;
- regulators need to make sure lending laws are followed.

### Transparency

A mortgage is an important financial decision.

If an applicant is denied, they should understand why.

A system that only says:

```text
denied
```

creates accountability problems.

Mitigation:

- give applicants the main reasons for the decision;
- explain which factors affected the result;
- provide a human appeal or review process;
- allow mistakes in the data or model decision to be challenged.

Stakeholders:

- applicants need explanations and a way to appeal;
- the bank needs an accountable decision process;
- regulators need enough transparency to check whether the system follows lending laws.

---

## 12 · Common Mistakes

### Python

- Confusing `==` with `is`.
- Forgetting that `y = x` does not copy a list.
- Using a list as a dictionary key or set member.
- Repeatedly concatenating strings in a loop and accidentally making an $O(n^2)$ algorithm.
- Using `pop(0)` on a list for BFS instead of `deque.popleft()`.
- Leaving `raise NotImplementedError` in completed code.
- Thinking `dict.get(key, default)` changes the dictionary by itself. It only returns a value.

### Search

- Treating BFS, DFS, and best-first as the same except for name.
- Forgetting that graph search needs `visited` to avoid repeated work.
- Storing predecessor links in the wrong direction. Use `pred[child] = parent`.
- Representing nodes as lists when they need to be stored in sets or dictionaries.

### Agents

- Saying a table-driven agent matches a prefix. It must match the complete percept sequence.
- Confusing current percept with percept sequence.
- Confusing agent function with agent program.
- Defining performance measure as an action reward instead of desired environment outcome.
- Thinking rationality means guaranteed success.
- Calling an environment fully observable just because the agent has some sensors.
- Forgetting that other drivers are agents, while objects like poles are just part of the environment.

---

## 13 · Quiz Review

### Q1

What is a method?

Answer:

> A method is a function defined inside a class and usually operating on an instance of that class.

### Q2

For `xs[a:b]`, which endpoint is included?

Answer:

> `a` is included, `b` is excluded.

### Q3

What does `xs[1:4]` select?

Answer:

> Indices `1, 2, 3`, usually $4-1=3$ elements.

### Q4

What is the difference between `==` and `is`?

Answer:

> `==` compares values; `is` checks whether two names refer to the same object.

### Q5

Why can repeated string concatenation be $O(n^2)$?

Answer:

> Strings are immutable, so each concatenation creates a new string and copies old content.

### Q6

What does `dict.get(key, default)` do?

Answer:

> It returns the value for `key` if present; otherwise it returns `default`.

### Q7

Why must graph nodes often be hashable?

Answer:

> They need to be stored in `visited` sets and predecessor dictionaries.

### Q8

What data structure should BFS use for the frontier?

Answer:

> `collections.deque`, because `append()` and `popleft()` are $O(1)$.

### Q9

What data structure should DFS use for the frontier?

Answer:

> A Python list as a stack, using `append()` and `pop()`.

### Q10

What data structure should best-first search use?

Answer:

> `heapq` with a list, using `heappush()` and `heappop()`.

### Q11

What does a table-driven agent look up?

Answer:

> The complete percept sequence.

### Q12

What is the difference between a Simple Reflex Agent and a Model-Based Reflex Agent?

Answer:

> A simple reflex agent uses only the current percept; a model-based reflex agent keeps internal state.

### Q13

What is the difference between a Goal-Based Agent and a Utility-Based Agent?

Answer:

> A goal-based agent asks whether an action helps reach the goal. A utility-based agent compares which option is better among possible outcomes.

### Q14

What does PEAS stand for?

Answer:

> Performance, Environment, Actuators, Sensors.

### Q15

Why does rationality not guarantee success?

Answer:

> Because rationality is based on available information and expected outcomes, not perfect knowledge of the future.

### Q16

Why is real-world driving hard as a task environment?

Answer:

> It is partially observable, stochastic, sequential, dynamic, continuous, and multi-agent.

### Q17

What are two ethical concerns in mortgage approval AI?

Answer:

> Bias and transparency.

### Q18

Why can zip code be risky in a mortgage model?

Answer:

> It may act as a proxy for demographic information and reproduce unfair historical patterns.

---

## 14 · One Sentence

> Homework 1 connects Python object/data-structure details with rational-agent design: good AI code needs correct object reasoning, efficient search structures, clear PEAS definitions, appropriate environment classification, and awareness of how performance measures and data choices shape behavior.

---

## 15 · Connections

Python Objects  
-> Mutability  
-> Hashability  
-> Dictionary Counting  
-> Search Frontier  
-> BFS / DFS / Best-First  
-> Agent Function  
-> Agent Types  
-> PEAS  
-> Environment Classification  
-> Rationality  
-> Ethics
