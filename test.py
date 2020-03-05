import os
import random
import sys

import pytest

from pages.locators import Links, TestData
from pages import pg_data_base
from xml.etree import ElementTree as E

# s = 'aaaabbcaa'
# s = input() + " "
# r = ''
# count = 1
# for i in range(len(s) - 1):
#     if s[i] == s[i+1]:
#         count += 1
#     else:
#         r += s[i] + str(count)
#         count = 1
# print(r)

# a = [int(i) for i in input().split()]
a = [4, 8, 0, 3, 4, 2, 0, 3]
# a = [1, 1, 1, 1, 1, 2, 2, 2]
r =[]
for i in a:
    if a.count(i) >= 2 and i not in r:
        r.append(i)
print(*sorted(r))
