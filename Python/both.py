from first_guess import firstname
from last_guess import lastname
from typo import miskey
from selenium import webdriver
from numpy import random

def first_both(names, n):
    names = names.copy()
    index = random.choice(range(len(names)),n, replace = False)
    br = webdriver.Firefox()
    for i in index:
         temp = firstname(names.loc[i],br)
         names.loc[i] = miskey(temp,br)
    br.close()
    return names

def last_both(names, n):
    names = names.copy()
    index = random.choice(range(len(names)),n, replace = False)
    br = webdriver.Firefox()
    for i in index:
         temp = lastname(names.loc[i],br)
         names.loc[i] = miskey(temp,br)
    br.close()
    return names.map(str).map(str.upper)
    