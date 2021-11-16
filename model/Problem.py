# @Time : 2021/10/7 下午4:06 
# @Author : Patrick.Lai
# @File : Problem.py 
# @Software: PyCharm
import numpy as np


# problem类，用于初始化线性规划问题
# 在problem中，可以添加目标函数，添加约束，
# Example
# maximize 13x1 + 8x2
#        st
#         x1 + 2x2 <= 10
#         5x1 + 2x2 <= 20
#         x1 ,x2 >= 0
# problem is described by two functions basically.
# The first function is init function, which describe the target function
# the second function is constraint addition function, witch will add constraint into problem
# In init function, variables input are matrix for target function and optimize mode.
# In constraint addition function, variables input are matrix for constraint.
class Problem:
    # Init function, init problem, problem should be presented as some mathematical expression. Problem should
    # includes target function and constraints.
    # For example, x1 + x2 + x3 <=4 is a constraint, -x1 - 14x2 - 6x2 is the target function.
    # Input max_mode = True means ask for a max value. Minimize is default mode.
    def __init__(self, obj, max_mode=False):  # default is solve min LP, if want to solve max lp,should * -1
        # get target function matrix and optimize mode
        # target function matrix should like [13,8], and with one additional col in its left, we get [0, 13, 8].
        # here, the value of the target function is presented as -z, initialed as 0
        # actually, we solve it always with a minimize optimization
        self.mat, self.max_mode = np.array([[0] + obj]) * (-1 if max_mode else 1), max_mode
        # how many variables are there in this problem, it will be used in Branch and Bound
        self.diversion = len(obj)
        # solution_flag means the problem is solvable or not, default True
        # if it do not have solution, then change it to False
        self.solution_flag = True

    # add constraint, a is the matrix for inequality, like x1 + 2x2 <= 10, then a is [1, 2]
    # b is the number of this constraint, here b should be 10, so the constraint is ([1, 2], 10)
    # constraint was added to the matrix row by row
    # for example:
    # initial state:
    # [0 13 8]
    # add constraint ([1, 2], 10)
    # it should be:
    # [[0 13 8]
    #  [10 1 2]]
    # just like init function, in this function, a presented the constraint function, and b is the number
    def add_constraint(self, a, b):
        self.mat = np.vstack([self.mat, [b] + a])

    # if the problem is not solvable, change solution_flag to False
    def no_solution(self):
        self.solution_flag = False

    # is the problem is solved, give the value to the solution of the problem
    def solved(self, solution):
        self.solution = solution

    # get the solution of the problem, exclude the final value of the target function
    def get_solution(self):
        return self.solution.variable


# ProblemNode class, it is used to construct the problem tree in Branch and Bound
# In each node, include a problem, its id and its father's id.
# Node id is automatic generated in add function.
class ProblemNode:
    def __init__(self, problem, father_problem=None, idx=-1):
        self.problem = problem
        if father_problem is not None:
            self.father_idx = father_problem.idx
        else:
            self.father_idx = -1
        self.idx = idx

    # get the solution for current node
    def getSolution(self):
        return self.problem.solution


# ProblemTree class, tree structure composed by nodes
# used in Branch and Bound to store all the problems
class ProblemTree:
    # Init function, the problem tree starts from the root node.
    # In Branch and Bound, the root is the first solution we get from simplex.
    # father_list is a list to store all idx of node who is a father node.
    def __init__(self, rootNode):
        self.list = [rootNode]
        self.node_idx = 0
        self.father_list = []

    # get children of current node
    def getChildren(self, node):
        if node not in self.list:
            return "Node Not In Problem Tree"
        children = []
        for i in self.list:
            if i.father_idx == node.idx:
                children.append(i)
        return children

    # get father node of current node
    def getFather(self, node):
        if node not in self.list:
            return "Node Not In Problem Tree"
        return node.father_idx

    # get root node
    def getRoot(self):
        for i in self.list:
            if i.idx == -1:
                return i

    # add node
    def add(self, node):
        node.idx = self.node_idx
        self.list.append(node)
        self.father_list.append(node.father_idx)
        self.node_idx += 1

    # get all leaf node
    def getLeaves(self):
        re = []
        for i in self.list:
            if i.idx not in self.father_list:
                re.append(i)
        return re

    # pop the last node
    def pop(self):
        return self.list.pop(-1)

    # if the tree is empty, return True, else return False
    def isEmpty(self):
        return len(self.list) == 0

    # show the tree
    def show(self):
        print("==================================================================================")
        print("Now Printing Solution Tree")
        print("==================================================================================")
        for i in self.list:
            print("Solution Node Id: ", i.idx)
            print("Solution Node Father Id: ", i.father_idx)
            i.problem.solution.show()
            print("==================================================================================")

