# AI Philosophy, Rational Agents, and Search

> Week 01 · Module 01

Source: user's pasted summary of Module 1 material, including AI in Philosophy, AI in SciFi, Rational Agents, Task Environments, and the transition into Search.

This note keeps the lecture's main logic. It does not try to solve the philosophical debate about whether machines really think; it records how the course moves from that debate into rational-agent design.

## 01 · Before

### Big Question

AI 的第一讲不是直接问“怎么写算法”，而是先问：

> 如果机器表现得像人，我们能不能说它真的在思考？

课程最后给出的学习方向是：

```text
philosophical question
-> difficult to define thinking
-> focus on behavior and rational action
-> model AI systems as agents
-> design agents that maximize expected performance
-> start with search in simplified environments
```

所以这节课的核心转折是：

$$
\boxed{
\text{This course focuses on acting rationally, not proving machine consciousness.}
}
$$

### Prerequisites

- Basic probability intuition for expected value（期望值）.
- Ability to describe a problem by states（状态）, actions（动作）, and goals（目标）.
- Comfort distinguishing a philosophical definition from an operational engineering definition.

### Questions

1. Turing Test 到底测试的是 thinking，还是 acting humanly？
2. Chinese Room 为什么挑战“会输出语言 = 真正理解”？
3. 为什么 rationality 不等于 omniscience？
4. PEAS 为什么是设计 agent 前必须先写清楚的东西？
5. 为什么 search 需要先假设环境是 static, fully observable, deterministic, discrete？

---

## 02 · Notes

### Core Idea

AI 可以从四个角度定义：

| | Human | Rational |
| --- | --- | --- |
| Thinking | Thinking Humanly | Thinking Rationally |
| Acting | Acting Humanly | Acting Rationally |

这门课选择的主线是：

$$
\boxed{\text{Acting Rationally}}
$$

也就是说，课程不要求机器：

- 拥有 consciousness（意识）；
- 像人一样思考；
- 像人一样说话；
- 每次都保证成功。

课程真正关心的是：

> 在已有信息下，agent 如何选择 expected performance（期望表现）最高的 action（动作）。

### Philosophy: Is the Machine Actually Thinking?

#### Descartes and Mind / Body Dualism

Descartes 的 mind / body dualism（心身二元论）把 human body（身体）和 mind（心灵）区分开：

- body 是物质性的；
- mind / thinking self 是非物质性的；
- 身体可以像复杂机器一样被理解，但 mind 不能简单还原为机械结构。

他的经典命题是：

> Cogito ergo sum: I think, therefore I am.

放到 AI 问题里，就是：

> 如果一个东西外表和行为都像人，我们怎么知道它不是 automaton（自动机器）？

Descartes 认为机器和人的关键区别之一是：机器不能真正、灵活地使用语言。

这和后来的 Turing Test 很接近。

#### Turing Test: Operationalizing the Question

Turing 认为 “Can machines think?” 太难定义，所以把问题 operationalize（操作化）：

```text
Do not ask:
Does the machine really think?

Ask:
Can the machine imitate human conversation well enough?
```

Turing Test 的基本结构：

```text
human evaluator
      |
text conversation
     / \
 human machine
```

如果 evaluator 无法可靠地区分哪个是人、哪个是机器，那么机器通过测试。

重要点：

> Turing Test 测试的是回答是否像人，而不是机器是否真的理解。

所以它属于：

$$
\boxed{\text{Acting Humanly}}
$$

不是：

$$
\text{Thinking Rationally or Acting Rationally}
$$

#### Searle's Chinese Room

Searle 的 Chinese Room（中文房间）挑战 Turing Test。

思想实验：

```text
person who does not understand Chinese
-> receives Chinese symbols
-> follows a rule book
-> outputs Chinese symbols
```

房间外的人可能觉得房间里的人懂中文，但房间里的人只是按规则做 symbol manipulation（符号操作）。

核心区分：

$$
\boxed{\text{syntax} \neq \text{semantics}}
$$

Meaning:

- syntax（语法 / 符号规则）：按照规则操作符号；
- semantics（语义）：真正理解符号的意义。

Searle 的结论是：

> 通过 Turing Test 不足以证明机器真正理解。

这引出 strong AI 和 weak AI。

| View | Meaning |
| --- | --- |
| Strong AI（强人工智能） | 机器真的拥有 understanding, mind, cognitive states |
| Weak AI（弱人工智能） | 机器只是 simulate thought，看起来像理解 |

#### Dennett and Brain in a Vat

Dennett 的 Brain in a Vat（缸中之脑）继续追问：

```text
brain removed from body
-> kept alive in vat
-> connected to body by signals
```

如果身体被摧毁，但 brain 还在工作，“我”在哪里？

如果 brain 的 information-processing structure（信息处理结构）可以被复制成 computer program，那么问题就变成：

> 如果 biological brain 也是一种 information processing，为什么 computer information processing 一定不能产生 mind？

课程不在这里解决哲学争论，只保留这个张力：

```text
actually thinking?
vs
simulating thinking?
```

然后转向更可操作的问题：

> How do we build practical AI programs that work?

### SciFi: From Imagination to Narrow AI

Science fiction 展示了人类如何想象 AI，也展示了很多想象后来变成了 narrow AI（狭义 AI）任务。

Examples:

- Star Trek
- Westworld
- Battlestar Galactica
- Blade Runner
- HAL 9000
- C-3PO

这些作品经常问：

> 如果机器人在外貌、语言、情绪、行为上都与人无法区分，它还是机器吗？

Blade Runner 里的 Voight-Kampff Test 和 Turing Test 很接近：

```text
observe behavior
-> infer whether human
```

现实 AI 的发展通常不是直接做一个 sci-fi general intelligence，而是把能力拆成 narrow subproblems：

| SciFi Ability | Real AI Subproblem |
| --- | --- |
| robot sees the world | classification, object detection, segmentation |
| natural conversation | speech recognition, dialogue systems, language models |
| universal translator | machine translation |
| game intelligence | chess, Jeopardy, Go |
| autonomous robot | driving, robotics, physical interaction |

Historical milestones:

- IBM Deep Blue: chess
- IBM Watson: Jeopardy!
- AlphaGo: Go
- DARPA Grand Challenge / Urban Challenge: autonomous driving
- DARPA Robotics Challenge and Boston Dynamics Atlas: robotics

Key idea:

> 很多以前被认为需要“人类智能”的任务，后来可以被清楚地形式化并由机器完成。

### Agent

Definition:

> An agent is anything that perceives its environment through sensors and acts on the environment through actuators.

中文理解：

```text
environment
    |
 sensors
    |
  agent
    |
actuators
    |
environment
```

Examples:

| Agent | Sensors | Actuators |
| --- | --- | --- |
| human | eyes, ears | hands, legs, mouth |
| robot | camera, range finder | motors |
| software bot | input streams, files, API data | API calls, messages, file edits |
| thermostat | temperature sensor | heating / cooling control |

### Percept and Percept Sequence

Percept（感知）是某一个时刻 agent 得到的输入。

Let:

$$
p_t
$$

be the percept at time $t$.

Then the percept sequence（感知序列）is:

$$
P=[p_0,p_1,\dots,p_t]
$$

The agent function maps a percept sequence to an action:

$$
f:P\rightarrow a
$$

where possible actions are:

$$
A=\{a_0,a_1,\dots,a_k\}
$$

Meaning:

> Agent function 是“如果看到这段历史，就应该做什么”的抽象描述。

### Agent Function vs Agent Program

Agent function:

$$
f:P\rightarrow a
$$

is an abstract mathematical description（抽象数学描述）.

Agent program 是真正运行在 hardware / architecture（硬件 / 架构）上的程序。

Compact formula:

$$
\boxed{\text{Agent}=\text{Architecture}+\text{Program}}
$$

The program implements the agent function.

理论上，可以用 giant lookup table：

```text
percept history -> action
```

但问题是：

> Table size grows exponentially with percept sequence length.

所以 AI 的任务不是死记所有输入输出，而是找到更聪明的 computation（计算方法）。

### Rationality

最初定义：

> Rational behavior = doing the right thing.

但 “right thing” 需要被定义。

课程采用 consequentialism（结果主义）：

> 根据 action 造成的 consequence（结果）评价 action。

因此需要 performance measure（性能度量）：

> An objective criterion for success of an agent's behavior.

For a vacuum cleaner agent:

| Performance Measure | Possible Problem |
| --- | --- |
| +1 for each clean square at time $T$ | rewards final clean world state |
| +1 for cleaning | agent may clean the same square repeatedly |
| -1 for every move | encourages shorter behavior |
| -1000 if too many squares remain dirty | strongly penalizes failure |

Important design rule:

> Performance measure should describe the environment state we want, not directly prescribe the agent's actions.

Bad reward:

```text
+1 every time robot cleans
-> clean same square again and again
```

Better reward:

```text
+1 for each clean square at time T
-> reward desired world outcome
```

This connects later to reward design（奖励设计）and specification gaming（指标投机）.

### Rationality Is Not Omniscience

Omniscience（全知）means knowing the true outcome of actions.

Real agents are not omniscient.

So:

$$
\boxed{\text{Rationality}\neq\text{Guaranteed Success}}
$$

Example:

```text
weather forecast says P(rain)=0.8
-> bring umbrella
-> it does not rain
```

This does not mean bringing an umbrella was irrational. The decision was rational because it used the available information.

### Expected Performance

The stronger definition is:

> A rational agent chooses the action that maximizes expected performance.

Formula:

$$
a^*=\arg\max_a \mathbb E[\text{Performance}\mid P,a]
$$

Meaning:

- $P$ is the percept sequence so far.
- $a$ is a possible action.
- $\mathbb E[\cdot]$ means expected value over uncertain outcomes.
- $a^*$ is the action with the best expected performance.

Core memory:

$$
\boxed{\text{Rational Agent}=\text{maximize expected performance}}
$$

### Task Environment and PEAS

Before designing an agent, define the task environment（任务环境）.

PEAS:

$$
\boxed{\text{PEAS}=\text{Performance, Environment, Actuators, Sensors}}
$$

It answers four questions:

| Letter | Question |
| --- | --- |
| P | What counts as success? |
| E | Where does the agent operate? |
| A | What can the agent do? |
| S | What can the agent observe? |

#### PEAS: Self-Driving Taxi

| Component | Examples |
| --- | --- |
| Performance | safe, fast, legal, comfortable, profitable |
| Environment | roads, traffic, pedestrians, customers |
| Actuators | steering, accelerator, brake, signal, horn |
| Sensors | camera, LiDAR, speedometer, GPS |

#### PEAS: Amazon Delivery Drone

| Component | Examples |
| --- | --- |
| Performance | maximize profit, minimize delivery time, obey airspace restrictions, correct delivery, avoid damage, avoid accidents, reduce noise, preserve battery |
| Environment | airspace, birds, other drones, buildings, trees, utility poles, people, cars, weather, houses, landing areas, package weight |
| Actuators | propellers, flight control, package arm / claw / basket, lights, delivery mechanism |
| Sensors | GPS, radar / LiDAR, altitude sensor, barometer, gyroscope, accelerometer, camera, rotor sensors, weight sensor |

Key idea:

> 一个实际 AI system 的 task environment 往往远比一句“送快递”复杂。

### What the Rational Agent Designer Does

Given a PEAS description, the designer does two things:

1. Construct the agent function $f$ that maximizes expected performance.
2. Implement that function as an agent program on a concrete architecture.

Pipeline:

```text
Task
-> PEAS
-> optimal agent function f
-> agent program
-> architecture
-> actions
```

### Environment Dimensions

Task environments can be classified along several dimensions. These dimensions matter because they decide which algorithms are appropriate.

#### Fully Observable vs Partially Observable

Fully observable:

> Agent has all state information needed for decision-making.

Example: chess board.

Partially observable:

> Agent only observes part of the environment.

Example: self-driving car, because sensors are limited, objects can be hidden, and other drivers' intentions are unknown.

#### Deterministic vs Stochastic

Deterministic:

> Given state + action, the next state is fixed.

Stochastic:

> Action outcomes involve randomness.

Example: roulette or real-world driving.

#### Episodic vs Sequential

Episodic:

> Each decision is mostly independent.

Sequential:

> Current actions affect future states, so the agent must plan ahead.

Example: autonomous driving.

#### Static vs Dynamic

Static:

> The environment does not change while the agent thinks.

Example: crossword puzzle.

Dynamic:

> The environment can change while the agent thinks.

Example: driving.

Semi-dynamic:

> The environment state may not change, but performance changes with time.

Example: chess with a clock.

#### Discrete vs Continuous

Discrete:

> States, actions, or time steps can be counted as separate units.

Example: chess.

Continuous:

> Position, velocity, time, or actions vary continuously.

Example: self-driving car and industrial control.

#### Single-Agent vs Multi-Agent

Single-agent:

> No other entity needs to be modeled as having its own goal.

Multi-agent:

> Other entities have their own goals and performance measures.

Good test:

> If an object's behavior is best explained by its own performance measure, treat it as another agent.

Examples:

- telephone pole: environment
- another driver: agent

### Why Real-World Driving Is Hard

The hardest environments often combine:

- continuous state/action/time;
- partial observability;
- stochastic outcomes;
- multi-agent interaction;
- unknown consequences.

Self-driving is hard because the agent cannot fully see the world, the world keeps changing, other people have goals, and action outcomes are uncertain.

### Course Simplification Before Search

To introduce search, the course temporarily assumes the environment is:

$$
\boxed{
\text{Static, Fully Observable, Deterministic, Discrete}
}
$$

This matters because search algorithms become clean when:

- the agent knows the current state;
- actions have predictable results;
- the world does not change while planning;
- states and actions can be enumerated.

### Reflex Agent vs Problem-Solving Agent

Simple reflex agent:

```text
current percept
-> condition-action rule
-> action
```

Example:

```python
if dirty:
    suck
```

It ignores percept history and does not plan ahead.

Problem-solving agent:

```text
current state
-> possible action
-> next state
-> possible action
-> ...
-> goal state
```

This planning process is search（搜索）.

### Search Problem: 8-Puzzle

A search problem is not just “choose one action.” It asks for a sequence of actions from initial state to goal state.

For 8-puzzle:

| Component | Meaning |
| --- | --- |
| Goal | tiles arranged correctly |
| States | possible puzzle configurations |
| Number of configurations | $9!$ |
| Actions | move a tile into the blank space |
| Branching | each state has up to $4$ actions |
| Performance measure | minimize total moves |
| Solution | action sequence |

Solution form:

```text
action 1 -> action 2 -> action 3 -> ... -> goal
```

This prepares the next topic: BFS, DFS, UCS, and other search algorithms.

---

## 03 · Explain

Explain the topic from memory in my own words.

### Simple Explanation

这节课先用哲学问题说明：机器“看起来像人在思考”不一定等于它真的理解。Turing Test 关注的是行为是否像人，Chinese Room 反驳说符号操作不等于理解。课程不想陷在这个争论里，所以转向更可操作的目标：把 AI system 看成 agent，让它根据感知到的信息选择期望表现最好的动作。

### Technical Explanation

An agent perceives its environment through sensors and acts through actuators. Its agent function maps a percept sequence $P$ to an action $a$. A rational agent selects the action that maximizes expected performance, not guaranteed success. To design such an agent, we first define the task environment using PEAS: performance measure, environment, actuators, and sensors. Environment properties such as observability, determinism, sequentiality, dynamics, discreteness, and number of agents determine what algorithms are appropriate. The course begins search under simplified assumptions: static, fully observable, deterministic, and discrete environments.

### 3-Minute Explanation

AI can be defined as thinking humanly, acting humanly, thinking rationally, or acting rationally. The philosophical part asks whether machine behavior proves real thought. Descartes separates mind and body and doubts whether machines can use language flexibly. Turing avoids defining thought and proposes the imitation game, which tests whether a machine can act humanly in conversation. Searle's Chinese Room argues that symbol manipulation is not the same as semantic understanding. Dennett pushes back by asking whether brains themselves are information-processing systems. The course does not resolve this debate. Instead, it chooses the rational-agent framework. An agent gets percepts through sensors, acts through actuators, and can be abstractly described by an agent function $f:P\to a$. Rationality means choosing the action with maximum expected performance under the available information. PEAS makes the task precise. After classifying environments, the course simplifies to static, fully observable, deterministic, discrete problems so that search can be introduced as planning a sequence of actions from an initial state to a goal.

---

## 04 · Test

### Q1

Why is the Turing Test categorized as acting humanly rather than thinking rationally?

My answer:

It evaluates whether a machine's conversational behavior is indistinguishable from a human's, not whether its internal reasoning is rational or whether it truly understands.

### Q2

What is the main point of Searle's Chinese Room?

My answer:

Following rules to manipulate symbols can produce correct-looking answers without semantic understanding. Therefore syntax is not the same as semantics.

### Q3

What is the difference between rationality and omniscience?

My answer:

Rationality chooses the best action based on available information and expected outcomes. Omniscience would mean knowing the true future outcome, which real agents do not have.

### Q4

What does the formula $f:P\to a$ mean?

My answer:

The agent function maps a percept sequence to an action. It describes what the agent should do for any history of percepts.

### Q5

What does PEAS stand for?

My answer:

Performance measure, Environment, Actuators, Sensors.

### Q6

Why should a performance measure describe desired world states rather than directly reward individual actions?

My answer:

If it rewards actions directly, the agent may exploit the metric, such as repeatedly cleaning the same square. Rewarding desired world states better matches the real objective.

### Q7

Why does the course initially assume static, fully observable, deterministic, discrete environments?

My answer:

Those assumptions make search well-defined and easier to analyze: the agent knows the state, actions have fixed results, the world does not change while planning, and states/actions can be enumerated.

### Q8

In the 8-puzzle, what is the solution?

My answer:

The solution is a sequence of actions that transforms the initial puzzle configuration into the goal configuration, usually minimizing total moves.

---

## 05 · Gaps

- [ ] I can explain why Turing Test is acting humanly, not proof of understanding.
- [ ] I can explain syntax vs semantics using Chinese Room.
- [ ] I can distinguish strong AI and weak AI.
- [ ] I can state the four AI definitions without mixing rows and columns.
- [ ] I can define agent, sensor, actuator, percept, and percept sequence.
- [ ] I can explain agent function vs agent program.
- [ ] I can explain why giant lookup tables do not scale.
- [ ] I can define rationality as maximizing expected performance.
- [ ] I can explain why rational action may still fail.
- [ ] I can write PEAS for a new task environment.
- [ ] I can classify an environment along the six dimensions.
- [ ] I can explain why self-driving is hard using environment dimensions.
- [ ] I can explain the assumptions that make early search algorithms clean.
- [ ] I can formulate a simple search problem with states, actions, goal, cost, and solution.

---

## 06 · Build

No lab yet.

Possible lab:

`labs/search-problem-visualizer.ipynb`

Questions the experiment should answer:

- How does branching factor affect the number of explored states?
- How does the choice of performance measure change agent behavior?
- How do different environment assumptions change which search algorithm is appropriate?

Before implementing:

1. Predict how fast a search tree grows when branching factor increases.
2. Predict what a bad performance measure might incentivize.
3. Predict which assumptions fail in a real self-driving task.

---

## 07 · One Sentence

> A rational agent perceives its environment, uses its percept history to choose actions that maximize expected performance, and in simple deterministic environments can plan by searching for an action sequence from an initial state to a goal.

---

## 08 · Connections

AI Philosophy  
-> Acting Humanly  
-> Turing Test  
-> Chinese Room  
-> Strong AI / Weak AI  
-> Rational Agents  
-> Performance Measure  
-> Expected Value  
-> PEAS  
-> Task Environment  
-> Search
