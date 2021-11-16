# @Time : 2021/10/27 下午12:44 
# @Author : Patrick.Lai
# @File : Utils.py 
# @Software: PyCharm
import math


def sort(values):
    keys = sorted(values.keys())
    re = {}
    for i in keys:
        re[i] = values[i]
    return re


def checkInt(number):
    return number % 1 == 0
