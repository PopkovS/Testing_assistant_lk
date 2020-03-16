import os
import random
import sys
from time import sleep

import pytest

from pages.locators import Links, TestData
from selenium import webdriver



browser = webdriver.Chrome()
browser.get("http://lk.corp.ast.safib.ru/User/ImportFromAD")