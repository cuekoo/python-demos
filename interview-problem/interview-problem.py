#! /usr/bin/python

# This program demonstrates the solution to the problem in Quora.
# 
# Suppose you are going to hire one person for a position. There are 100 
# candidates. You interview one by one and should make the decision 
# immediately after the interview. There's no way to get back the candidates
# who you already eliminated. Then what's the best strategy to get the best 
# candidate?

import random
import math
from collections import Counter
from matplotlib import pyplot as plt

def try_max(num, base):

    data = range(0, num)
    random.shuffle(data)

    b = math.floor(1 * num / base)

    maxv = 0
    for i in range(0, num):
        if i < b:
            if data[i-1] > maxv:
                maxv = data[i - 1]

        else:
            if data[i - 1] > maxv:
                maxv = data[i - 1]
                return maxv

    return data[num - 1]

def exp(trynum, num, base):
    temp = []
    for i in range(0, trynum):
        temp.append(try_max(num, base))

    return temp


def count(num, result):

    cnt = Counter(result)
    temp = []
    for i in range(0, num):
        temp.append(cnt[i])

    return temp


num = 100
trynum = 1000

result_quora = exp(trynum, num, math.e)

plt.title("histogram of guesses")
plt.plot(range(0, num), count(num, result_quora), "bo-")
plt.show()
