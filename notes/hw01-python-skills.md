# Homework 1 · Python Skills

> Week 01 · Programming Assignment

Source: CIS5210 Homework 1 (Python Skills, 105 points) and the submitted `homework1.py`.

这份作业不讲搜索算法，而是把后面实现 agent / search 时会反复用到的 Python 基本功钉住：类型系统、可哈希对象、切片、推导式、generator、字符串处理、以及用 special methods 做一个不可变的 `Polynomial` 类。

核心问题：

> 不 import 标准库的前提下，我能不能用内置类型把数据表示清楚，并且知道每种写法的代价和边界？

---

## 01 · 作业约束

| 约束 | 含义 |
| --- | --- |
| 不改函数名和签名 | autograder 按名字调用 |
| 默认禁止 `import x` / `from x import y` | 只用 built-in |
| 例外 | 第 7 节可以 `import numpy` 和 `import nltk` |
| PEP 8 | `pycodestyle` 默认设置，有任何 style error 就丢 5 分 |
| 例子不是完整测试 | 作业里的 `>>>` 只是典型用法 |

Python 内置里这张作业真正用到的：

```text
list / tuple / str slicing
list comprehension
yield
str.lower / split / join / capitalize
dict
sum, range, abs, enumerate, sorted
special methods: __init__ __neg__ __add__ __sub__ __mul__ __call__ __str__
```

---

## 02 · Python 类型：strong + dynamic

Python 同时是：

- **strongly typed**（强类型）：对象带着自己的类型；不相容操作通常直接报错，而不是悄悄转换。
- **dynamically typed**（动态类型）：名字没有固定声明类型；同一个名字可以先后绑定不同类型的对象。

```python
"3" + 4          # TypeError：强类型，不会把 4 变成 "4"
x = "hello"
x = 7            # 合法：动态类型，名字 x 改绑到 int
```

对比记忆：

| | 强类型 | 弱类型 |
| --- | --- | --- |
| 不相容运算 | 报错 | 常悄悄转换 |

| | 静态类型 | 动态类型 |
| --- | --- | --- |
| 类型绑在哪 | 变量名 / 声明 | 运行时的对象 |

$$
\boxed{
\text{strong ≠ static。Python 是 strong + dynamic。}
}
$$

C / Java 更接近 static；JavaScript 的 `"3" + 4 == "34"` 更接近 weak。后面 search 里把 state 写成 tuple 还是 list，本质也是在选对象的类型与可变性，而不是在选变量名的类型。

---

## 03 · Dict key 必须可哈希

下面这行会 `TypeError`：

```python
points_to_names = {[0, 0]: "home"}
```

原因链：

```text
list 可变
-> 内容变了 hash 也会变
-> 无法作为 dict key / set 元素
-> 必须用 hashable 对象
```

可哈希（作业里够用的）：`int`、`str`、元素也可哈希的 `tuple`。

不可哈希：`list`、`dict`、`set`。

解法：把点写成 tuple。

```python
points_to_names = {(0, 0): "home", (1, 2): "school", (-1, 1): "market"}
```

$$
\boxed{
\text{dict key 用 tuple，不用 list。图搜索里的 state 同理。}
}
$$

注意：`([0],)` 这种「tuple 里装着 list」仍然不可哈希，因为 hash 会递归看里面的元素。

---

## 04 · 字符串拼接：`+=` vs `join`

```python
def concatenate1(strings):
    result = ""
    for s in strings:
        result += s
    return result

def concatenate2(strings):
    return "".join(strings)
```

`str` 不可变。`result += s` 每次都新建一个字符串，并把旧内容拷过去。若最终长度是 $n$，拷贝量大约是 $1+2+\cdots+n$，即 $O(n^2)$。

`"".join(strings)` 先知道总长度，再一次写完，通常是 $O(n)$。

$$
\boxed{
\text{循环里拼字符串用 join，不要反复 +=。}
}
$$

作业后半的 `normalize`、`no_vowels`、`digits_to_words`、`Polynomial.__str__` 都走同一条路：先收集片段，最后 `join`。

---

## 05 · List comprehension

### Filter then map

循环版：

```python
result = []
for x in lst:
    if p(x):
        result.append(f(x))
```

一行版：

```python
[f(x) for x in lst if p(x)]
```

阅读顺序：

```text
for x in lst
-> 若 p(x) 为真
-> 产生 f(x)
```

### 展平：双重 `for`

```python
def concatenate(seqs):
    return [x for seq in seqs for x in seq]
```

对应的嵌套循环是：

```python
result = []
for seq in seqs:
    for x in seq:
        result.append(x)
```

`for` 的书写顺序必须和外层循环一致：先 `seq in seqs`，再 `x in seq`。

```python
concatenate([[1, 2], [3, 4]])     # [1, 2, 3, 4]
concatenate(["abc", (0, [0])])    # ['a', 'b', 'c', 0, [0]]
```

字符串、tuple、list 都可迭代，所以这里的输入叫 sequences，不叫 lists。内层元素原样放进结果：`[0]` 仍是一个 list，不会再展平一层。

### 转置

矩阵是 list of lists。转置满足：

$$
\texttt{matrix}[i][j] = \texttt{transpose}(\texttt{matrix})[j][i]
$$

```python
def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]
```

外层按列号 `i` 走，内层把每一行的第 `i` 个元素抽出来，变成新的一行。

```python
transpose([[1, 2, 3]])                 # [[1], [2], [3]]
transpose([[1, 2], [3, 4], [5, 6]])    # [[1, 3, 5], [2, 4, 6]]
```

不能改输入：内层必须新建 list，而不是改 `matrix` 里的旧行。

`zip(*matrix)` 也能转置，但得到的是 tuple；作业要 list of lists，还要自己写 comprehension，所以用索引更直接。

---

## 06 · Sequence slicing

通用形式：

```python
seq[start:stop:step]
```

默认值：

| 省略 | 默认 |
| --- | --- |
| `start` | 从头（`step>0` 时是 `0`） |
| `stop` | 到尾 |
| `step` | `1` |

切片是左闭右开。结果类型跟输入相同：`str` 得到 `str`，`tuple` 得到 `tuple`，`list` 得到 `list`。

### 浅拷贝

```python
def copy(seq):
    return seq[:]
```

`[:]` 做出同类型新序列。对 list 是 shallow copy：外层新对象，里面的元素还是旧引用。作业例子只改 `x[0] = 1`，所以够用。

```python
x = [0, 0, 0]
y = copy(x)
x[0] = 1
# x == [1, 0, 0], y == [0, 0, 0]
```

如果元素本身是 list，`y[i] is x[i]` 仍为真。那是浅拷贝的边界，不是这题要求。

### 丢掉最后一个

```python
def all_but_last(seq):
    return seq[:-1]
```

`stop = -1` 表示「到最后一个之前」。空序列的 `[:-1]` 仍是同类型空序列：

```python
all_but_last("abc")    # 'ab'
all_but_last((1, 2, 3))  # (1, 2)
all_but_last("")       # ''
all_but_last([])       # []
```

### 隔一个取一个

```python
def every_other(seq):
    return seq[::2]
```

从 index `0` 起，步长 `2`：`0, 2, 4, ...`。

```python
every_other([1, 2, 3, 4, 5])  # [1, 3, 5]
every_other("abcdef")         # 'ace'
```

$$
\boxed{
\text{切片会保留原序列类型；}[:] \text{ 是浅拷贝，不是 deepcopy。}
}
$$

---

## 07 · Generators

这一节要求 `yield`，不能 `return` 一整份 list。

Generator 的要点：

- 调用函数得到的是 iterator，还没有把所有结果算完。
- 每次迭代才算出下一个值。
- `list(prefixes(...))` 只是为了把结果看清楚。

作业允许任意顺序，但例子的顺序已经提示了实现。

### Prefixes

空前缀、前 1 个、前 2 个、……、整个序列：

```python
def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[:i]
```

`i` 从 `0` 到 `len(seq)`，正好 `n+1` 个前缀。`seq[:i]` 自动保持原类型，所以 `"abc"` 得到 `''`, `'a'`, `'ab'`, `'abc'`。

### Suffixes

整个序列、去掉第一个、……、空后缀：

```python
def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:]
```

### 所有非空切片

固定起点 `start`，终点 `stop` 从 `start+1` 走到 `len(seq)`：

```python
def slices(seq):
    for start in range(len(seq)):
        for stop in range(start + 1, len(seq) + 1):
            yield seq[start:stop]
```

对长度 `n` 的序列，非空切片个数是：

$$
\frac{n(n+1)}{2}
$$

```python
list(slices([1, 2, 3]))
# [[1], [1, 2], [1, 2, 3], [2], [2, 3], [3]]
```

这和 prefixes/suffixes 不同：切片可以既不从头开始、也不到尾结束，例如 `[2]`。

---

## 08 · 文本处理

### `normalize`

小写，词与词之间一个空格，没有首尾空白。

```python
def normalize(text):
    return " ".join(text.lower().split())
```

`str.split()` 不带参数时，任意连续空白都当分隔符，并且会丢掉首尾空白。这正好是 normalization 要的。

```python
normalize(" EXTRA SPACE ")          # 'extra space'
normalize("This is an example.")    # 'this is an example.'
```

标点还在。这题只收空白和大小写，不删句号。

### `no_vowels`

`y` 不当元音。大小写的 `aeiou` 都删，其它字符原样保留。

```python
def no_vowels(text):
    vowels = "aeiouAEIOU"
    return "".join(char for char in text if char not in vowels)
```

```python
no_vowels("We love Python!")  # 'W lv Pythn!'
```

`Python` 里的 `y` 留下。空格、感叹号也留下。

### `digits_to_words`

只提取数字字符，按出现顺序拼成英文单词，空格分隔；没有数字则返回 `""`。

```python
names = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
}
return " ".join(names[char] for char in text if char in names)
```

```python
digits_to_words("Pi is 3.1415...")  # 'three one four one five'
```

小数点不是 digit，会被跳过。

### `to_mixed_case`

`underscore_name` → `mixedCase`。

规则：

1. 按 `_` 切开。
2. 丢掉空段，从而忽略首尾和连续下划线。
3. 每一段先 `lower`。
4. 第一段保持小写，后面每段 `capitalize`。
5. 如果全是下划线，返回 `""`。

```python
def to_mixed_case(name):
    words = [word.lower() for word in name.split("_") if word]
    if not words:
        return ""
    return words[0] + "".join(word.capitalize() for word in words[1:])
```

```python
to_mixed_case("to_mixed_case")       # 'toMixedCase'
to_mixed_case("__EXAMPLE__NAME__")   # 'exampleName'
to_mixed_case("___")                 # ''
```

`split("_")` 遇到 `"__EXAMPLE__"` 会得到 `['', '', 'EXAMPLE', '', '']`，`if word` 把空字符串滤掉。

---

## 09 · Polynomial 类

这是作业的主菜。内部表示是 **coefficient-power 对的 tuple**，例如 $2x+1$ 存成：

```python
((2, 1), (1, 0))
```

顺序按构造时的顺序，不自动化简。可以把它想成「项的序列」，还不是数学上已经合并同类项的多项式。

### 不可变内部表示

```python
def __init__(self, polynomial):
    self.polynomial = tuple(polynomial)
```

`tuple(...)` 让 list 输入和 tuple 输入都变成同一内部类型。之后算术运算都 `return Polynomial(...)` 新对象，不改旧对象。

`simplify` 会改 `self.polynomial`。作业的解释是：多项式的数学值没变，所以仍可看作不可变值上的正规化。

### 算术：不对结果化简

| 方法 | Python 语法 | 行为 |
| --- | --- | --- |
| `__neg__` | `-p` | 每个系数取负 |
| `__add__` | `p + q` | 两项序列直接拼接 |
| `__sub__` | `p - q` | `p + (-q)` |
| `__mul__` | `p * q` | 每一对项做系数相乘、次数相加 |

```python
def __mul__(self, other):
    return Polynomial([
        (c1 * c2, p1 + p2)
        for c1, p1 in self.polynomial
        for c2, p2 in other.get_polynomial()
    ])
```

$(2x+1)^2$ 不化简时是：

```text
(2x)(2x) + (2x)(1) + (1)(2x) + (1)(1)
= 4x^2 + 2x + 2x + 1
```

对应 `((4, 2), (2, 1), (2, 1), (1, 0))`。乘法例子允许项顺序不同，但项集合要一样。

$$
\boxed{
\text{+ / - / * 只拼接或展开项，不合并。合并只发生在 simplify。}
}
$$

### 求值 `__call__`

让 `p(x)` 可行：

```python
def __call__(self, x):
    return sum(c * (x ** p) for c, p in self.polynomial)
```

$$
p(x)=\sum_i c_i x^{k_i}
$$

### `simplify`

三步，最后一步是原地写回：

1. 按 power 把系数加起来。
2. 丢掉系数为 0 的项。
3. 按 power **降序** 排序。
4. 如果一项都不剩，变成 `(0, 0)`，即 $0 \cdot x^0$。

```python
terms = {}
for coefficient, power in self.polynomial:
    terms[power] = terms.get(power, 0) + coefficient
```

`p - p` 化简后必须是 `((0, 0),)`，不能是空 tuple。否则 `__str__` 和 `__call__` 对「零多项式」没有项可走。

### `__str__` 的排版规则

输出形状：

```text
sign1 term1 sign2 term2 ... signN termN
```

例外（作业原文，必须逐条满足）：

1. **第一项的符号**：和第一项之间没有空格；若第一项系数为正，符号直接省略。
2. **power = 0**：不写 `x`，只写系数。
3. **power = 1**：不写 `^1`。
4. **系数绝对值为 0**：符号永远写成正的。所以是 `0x` 不是 `-0x`。
5. **系数绝对值为 1**：省略系数，除非 power 为 0。所以是 `x`、`-x`、`x^2`，但常数项仍是 `1` / `-1`。

实现时把每一项拆成「符号」和「绝对值项」：

```text
符号:  coefficient < 0 则为 "-"，否则 "+"
      （0 会走到 "+" 分支，满足规则 4）

绝对值项:
  power == 0 -> str(abs(c))
  power != 0 且 abs(c) == 1 -> "x" 或 "x^k"
  其它 -> "ax" 或 "ax^k"
```

再拼接：

```text
第一项正: term
第一项负: -term
后面的项: " + term" 或 " - term"
```

对照：

```python
str(Polynomial([(1, 1), (1, 0)]))           # 'x + 1'
str(Polynomial([(0, 1), (2, 3)]))           # '0x + 2x^3'
str(-Polynomial([(1, 1), (2, 3)]) * ...)    # 第一项负时紧贴 '-'
```

未化简的多项式按内部项顺序打印，不排序。`print(r)` 和 `r.simplify(); print(r)` 可以完全不同。

$$
\boxed{
\text{__str__ 按内部项顺序排版；simplify 才合并、删零、按次数降序。}
}
$$

---

## 10 · numpy 与 NLTK

作业从这里开始允许第三方库。

### `sort_array`

输入：若干个形状不同的矩阵。

输出：所有数拉成一个一维 `int` 数组，**降序**。

```python
values = numpy.concatenate([matrix.ravel() for matrix in list_of_matrices])
return numpy.sort(values.astype(int))[::-1]
```

| 步骤 | 作用 |
| --- | --- |
| `ravel()` | 每个矩阵压成 1D |
| `concatenate` | 拼成一条 |
| `astype(int)` | 按作业要求变成 int |
| `sort` 再 `[::-1]` | 升序之后反转成降序 |

`numpy.sort` 默认升序。不要用 `list.sort` 的 `reverse=True` 思维直接找一个 `np.sort(..., reverse=True)`，numpy 没有这个参数。

Windows 上 `astype(int)` 常是 `int32`，Linux / Gradescope 常是 `int64`。作业要的是「dtype 是 int」，一般按数值比较。

### `POS_tag`

流水线必须按作业顺序：

```text
1. 全部小写
2. tokenize
3. 去掉 stop words 和 punctuation
4. pos_tag，返回 list of (word, tag)
```

```python
tokens = nltk.word_tokenize(sentence.lower())
words = [
    token for token in tokens
    if token not in stop_words and any(char.isalnum() for char in token)
]
return nltk.pos_tag(words)
```

`any(char.isalnum() for char in token)` 的意思是：token 里至少有一个字母或数字才留下。纯标点 `'.'`、`','`、`'!'` 会被丢掉。

```python
POS_tag("The Force will be with you. Always.")
# [('force', 'NN'), ('always', 'RB')]
```

`the / will / be / with / you` 是 stop words；句号是标点；剩下 `force`（名词）和 `always`（副词）。

第一次用 NLTK 需要下载：

```python
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")
```

---

## 11 · 这张作业在练什么

```text
类型与可变性
 -> 选 list 还是 tuple
 -> dict / set / 图的 state

切片与推导式
 -> 少写手工循环
 -> 保持序列类型

generator
 -> 需要「所有前缀 / 所有切片」时不必先建成巨大 list

字符串
 -> split / join 是 normalization 的默认工具
 -> 循环 += 有二次代价

special methods
 -> 让自定类看起来像内置对象：-p, p+q, p(x), print(p)

numpy / nltk
 -> 矩阵拉平排序、NLP 预处理流水线
```

和后面 search homework 的接口：

- 可哈希 state：用 tuple，不要用 list。
- BFS 的路径、前缀、切片：先想 slice / generator，再想要不要存整张表。
- 输出字符串：收集片段再 `join`。

---

## 12 · 易错点

1. `concatenate` 的双重 `for` 写反，会变成「先元素后序列」，直接错。
2. `copy` 若写成 `list(seq)`，字符串会变成字符 list，类型就错了。必须用切片保住类型。
3. `all_but_last([])` 必须仍是 `[]`，不能 `None` 或报错。
4. `prefixes` / `suffixes` 都包含空序列，所以循环是 `range(len(seq) + 1)`。
5. `slices` 不包含空切片；内层从 `start + 1` 开始。
6. `normalize` 用 `split(" ")` 会留下空字符串，多个空格就清不干净。要用无参 `split()`。
7. `to_mixed_case` 必须先 `lower` 再 `capitalize`，否则 `"EXAMPLE"` 会变成 `"EXAMPLE"` 而不是 `"example"` / `"Example"`。
8. 多项式加减乘 **不要** 自动 `simplify`。autograder 会检查未化简的内部 tuple。
9. 零多项式化简后是 `((0, 0),)`，不是 `()`。
10. `__str__` 里系数 `0` 的符号必须是 `+`；系数 `1` 在 `x^k` 上要省略，在常数项上不能省略。
11. 除第 7 节外出现任何 `import` 都可能整份作业作废。
12. PEP 8 行宽 79、顶层函数之间两行空行、`pycodestyle` 任意一条都丢 style 分。

---

## 13 · 一句话

$$
\boxed{
\text{用内置序列、切片、推导式和 special methods 把数据表示做对；}
\text{可变性、可哈希、字符串代价是后面写 search 时最先踩的坑。}
}
$$

---

## 14 · 自测

不看代码，试着回答：

1. 为什么 `(0, 0)` 能当 dict key，`[0, 0]` 不能，`([0],)` 也不能？
2. `seq[:-1]` 对空 list、空字符串、单元素 tuple 各返回什么类型、什么内容？
3. `prefixes("ab")` 和 `slices("ab")` 的结果差在哪一项？
4. 为什么 `p + p` 的内部表示是四项而不是两项？
5. `Polynomial([(0, 1)])` 和 `-Polynomial([(0, 1)])` 的 `str` 是否相同？为什么作业要单独写「零系数永远正号」？
6. `to_mixed_case("__A__B__")` 应该是什么？
7. 若 POS 流水线先 `pos_tag` 再删 stop words，tag 还可靠吗？
