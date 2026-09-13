# Review

Notes record what I understand; review records what I do not understand.

## Current Weak Points

### High Priority

- Python skills check: identify any prerequisite gaps before Homework 1.
- Python object model: distinguish class, instance, attribute, method, aliasing, mutability, and identity.
- Python data structures: choose `deque`, `list`, `heapq`, `set`, and `dict` correctly for graph search.
- Homework 1 implementation details: explain slicing, generators, text normalization, and `Polynomial` special methods from memory.
- Rational agents: explain what makes an action rational in a specific environment.
- Search formulation: distinguish states, actions, transition model, goal test, and path cost.
- Search nodes: distinguish a world state from a search-tree node with parent, action, path cost, and depth.
- Tree search vs graph search: explain why repeated states can turn a simple problem exponential.
- BFS / DFS / iterative deepening: compare completeness, optimality, time, and space from memory.
- Search complexity variables: distinguish branching factor $b$, shallowest goal depth $d$, and maximum depth $m$.
- Optimal solution cost: explain what $C^*$ means and when it equals depth $d$.
- Iterative deepening derivation: explain why repeated depth-limited search is still $O(b^d)$.
- PEAS: write Performance, Environment, Actuators, and Sensors for a new task without mixing them.
- Bounded rationality: explain why rational agents cannot require omniscience or unlimited computation.

### Medium Priority

- Uninformed vs informed search: explain what information the algorithm is allowed to use.
- LLMs and planning: explain why a language model can answer a famous shortest-path example without reliably computing shortest paths.
- Adversarial games: explain why an optimal move depends on assumptions about the opponent.
- Constraint satisfaction: distinguish search over paths from search over assignments.
- Turing Test vs Chinese Room: distinguish acting humanly from real understanding.
- ELIZA and symbol manipulation: explain why plausible conversation is not enough to prove semantic understanding.
- AGI / LLMs: explain why GPT-style systems bring philosophy questions back into AI discussion.
- Environment dimensions: classify whether a task is fully/partially observable, deterministic/stochastic, episodic/sequential, static/dynamic, discrete/continuous, and single/multi-agent.
- AI ethics: explain bias and transparency in automated mortgage approval.

---

## Recurring Mistakes

Record repeated confusions here after quizzes, homework, or oral explanations.

---

## Oral Exams

### Week 01

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

What do $b$, $d$, and $m$ mean in search complexity?

My answer:


Verdict:


Missing:

Question:

What is $C^*$, and when is it equal to $d$?

My answer:


Verdict:


Missing:

Question:

Why does BFS test a generated child for the goal before inserting it into the frontier?

My answer:


Verdict:


Missing:

Question:

Why is BFS complete and unit-cost optimal, but memory-heavy?

My answer:


Verdict:


Missing:

Question:

In depth-limited search, what goes wrong when $l<d$ and when $l>d$?

My answer:


Verdict:


Missing:

Question:

Derive why iterative deepening is still $O(b^d)$ even though it repeats shallow nodes.

My answer:


Verdict:


Missing:

Question:

Why does iterative deepening recover BFS-like guarantees with DFS-like memory?

My answer:


Verdict:


Missing:

Question:

Why can a large language model get the Romania shortest path right without being a reliable planner?

My answer:


Verdict:


Missing:

Question:

What does it mean for an AI agent to act rationally?

My answer:


Verdict:


Missing:

Question:

How would you formulate a simple route-finding problem as a search problem?

My answer:


Verdict:


Missing:

Question:

Why can a rational action still lead to a bad outcome?

My answer:


Verdict:


Missing:

Question:

What is bounded rationality, and why does it matter for AI?

My answer:


Verdict:


Missing:

Question:

Why is ELIZA a useful example for Searle's Chinese Room argument?

My answer:


Verdict:


Missing:

Question:

Write PEAS for a delivery drone.

My answer:


Verdict:


Missing:

Question:

Why is `collections.deque` better than a list with `pop(0)` for BFS?

My answer:


Verdict:


Missing:

Question:

Why can `zip code` be ethically risky in a mortgage approval model?

My answer:


Verdict:


Missing:

---

## Revisit

- [ ] Compare this course map with the full Canvas Modules page.
- [x] Add Lecture 1 note after studying the actual Module 1 material.
- [x] Add Homework 1 Python / agent review note.
- [x] Add Homework 1 Python Skills implementation note.
- [ ] Check whether quizzes should be tracked in a separate assignment calendar.
