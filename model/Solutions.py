# @Time : 2021/10/27 下午2:52 
# @Author : Patrick.Lai
# @File : Solutions.py 
# @Software: PyCharm
class Solution:
    def __init__(self, solution, result):
        self.variable = solution
        self.result = result

    def show(self):
        print("The best result is :", self.result, " the solution is :")
        for i in self.variable.keys():
            print("X", i, ": ", self.variable[i])

    def checkInt(self):
        values = self.variable.values()
        for i in values:
            if i % 1 != 0:
                return False
        return True
