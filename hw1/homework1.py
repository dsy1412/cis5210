import numpy
import nltk

############################################################
# CIS 521: Homework 1
############################################################

student_name = "Shengyang Dong"

# This is where your grade report will be sent.
student_email = "sd3666@engineering.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python is strongly typed because objects keep their types and Python does not
silently convert incompatible types in most operations. For example, "3" + 4
raises a TypeError instead of automatically converting one value.

Python is dynamically typed because variable names do not have fixed declared
types. A name can refer to a string at one moment and an integer later, as in
x = "hello"; x = 7.
"""

python_concepts_question_2 = """
The problem is that lists are mutable and therefore unhashable, so they cannot
be used as dictionary keys. Dictionary keys must be hashable because Python
uses their hash values to find stored entries efficiently.

A solution is to use tuples instead of lists:
points_to_names = {(0, 0): "home", (1, 2): "school",
                   (-1, 1): "market"}
"""

python_concepts_question_3 = """
concatenate2 is better for large inputs because "".join(strings) builds the
final string in one pass. In concatenate1, strings are immutable, so each
result += s creates a new string and copies the old contents. Repeated copying
can make the total running time much larger, often quadratic in the final
string length.
"""

############################################################
# Section 2: Working with Lists
############################################################


def extract_and_apply(lst, p, f):
    return [f(x) for x in lst if p(x)]


def concatenate(seqs):
    return [x for seq in seqs for x in seq]


def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    return seq[:]


def all_but_last(seq):
    return seq[:-1]


def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[:i]


def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:]


def slices(seq):
    for start in range(len(seq)):
        for stop in range(start + 1, len(seq) + 1):
            yield seq[start:stop]

############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    return " ".join(text.lower().split())


def no_vowels(text):
    vowels = "aeiouAEIOU"
    return "".join(char for char in text if char not in vowels)


def digits_to_words(text):
    names = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    return " ".join(names[char] for char in text if char in names)


def to_mixed_case(name):
    words = [word.lower() for word in name.split("_") if word]
    if not words:
        return ""
    return words[0] + "".join(word.capitalize() for word in words[1:])

############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        return Polynomial([(-coefficient, power)
                           for coefficient, power in self.polynomial])

    def __add__(self, other):
        return Polynomial(self.polynomial + other.get_polynomial())

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Polynomial([
            (coefficient1 * coefficient2, power1 + power2)
            for coefficient1, power1 in self.polynomial
            for coefficient2, power2 in other.get_polynomial()
        ])

    def __call__(self, x):
        return sum(coefficient * (x ** power)
                   for coefficient, power in self.polynomial)

    def simplify(self):
        terms = {}
        for coefficient, power in self.polynomial:
            terms[power] = terms.get(power, 0) + coefficient

        simplified = [
            (coefficient, power)
            for power, coefficient in terms.items()
            if coefficient != 0
        ]

        if not simplified:
            self.polynomial = ((0, 0),)
            return

        self.polynomial = tuple(
            sorted(simplified, key=lambda term: term[1], reverse=True)
        )

    def __str__(self):
        rendered_terms = []
        for index, (coefficient, power) in enumerate(self.polynomial):
            sign = "-" if coefficient < 0 else "+"
            magnitude = abs(coefficient)

            if power == 0:
                term = str(magnitude)
            else:
                if magnitude == 1:
                    term = "x"
                else:
                    term = str(magnitude) + "x"
                if power != 1:
                    term += "^" + str(power)

            if index == 0:
                if sign == "-":
                    rendered_terms.append("-" + term)
                else:
                    rendered_terms.append(term)
            else:
                rendered_terms.append(" " + sign + " " + term)

        return "".join(rendered_terms)

############################################################
# Section 7: Python Packages
############################################################


def sort_array(list_of_matrices):
    if not list_of_matrices:
        return numpy.array([], dtype=int)
    values = numpy.concatenate([matrix.ravel() for matrix in list_of_matrices])
    return numpy.sort(values.astype(int))[::-1]


def POS_tag(sentence):
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = nltk.word_tokenize(sentence.lower())
    words = [
        token for token in tokens
        if token not in stop_words and any(char.isalnum() for char in token)
    ]
    return nltk.pos_tag(words)

############################################################
# Section 8: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
8
"""

feedback_question_2 = """
The Polynomial class was the hardest part, especially simplify() and __str__().
There were many small rules for signs, coefficients, and powers, so it was easy
to miss one case. Setting up NLTK and removing stop words and punctuation also
took some time.
"""

feedback_question_3 = """
I liked the Polynomial section because it showed how to use special methods
like __add__ and __mul__. The slicing and generator problems were also clear
and useful. I would not change much, but more test cases for __str__() would
help.
"""
