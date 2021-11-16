# @Time : 2021/10/27 下午12:42 
# @Author : Patrick.Lai
# @File : BranchAndBound.py
# @Software: PyCharm
import math
import copy

from model.Problem import ProblemTree, ProblemNode, Problem
from method.Simplex import Simplex
from util import Utils


def solveProblem(problem):
    sim = Simplex(problem)
    sim.solve()
    return problem


class BranchAndBound:
    def __init__(self, problem):
        self.problem = problem
        self.problem_list = ProblemTree(ProblemNode(problem))

    def branch(self):
        # 确定树的深度，solution里有几个变量说明要分支几次
        keys = list(self.problem.solution.variable.keys())
        depth = len(keys)
        # 每次分层时做：
        for i in range(0, depth):
            # 当前解中可能有多个变量，比如X1， X2， 判断第i个变量的值是否为整数
            # 当前需要分类讨论的解为解树中的叶子节点，全部取出
            current_problems = self.problem_list.getLeaves()
            # 对于在当前需要分类讨论的解，以此做：
            for father in current_problems:
                # 如果当前问题有解
                if father.problem.solution_flag:
                    # 算第一层的时候，取变量解中的第一个变量，算第二层的时候，取变量解中的第二个变量，以此类推
                    # value = father.problem.getSolution()[i]
                    key = keys[i]
                    value = father.problem.get_solution()[key]
                    if not Utils.checkInt(value):
                        # 如果不是整数，则分别向上向下取整
                        lower = int(value)
                        upper = math.ceil(value)
                        # 分别使用向下取整和向上取整的结果生成新的线性规划问题，这一步的本质实在添加一条约束
                        lower_problem = copy.deepcopy(self.problem)
                        upper_problem = copy.deepcopy(self.problem)
                        # 这里要增加一条约束，由于之前的解是个dict形式，其中dict的key是表示第几个x，也就是说，当前key是几，就第几列为1，其余为0
                        # 比如初始解给出X1 = 2.5，这里我们向下取整为2， 向上取整为3，然后增加约束([1,0],2)和([-1,0],-3)
                        # 增加的约束，表示为1行n列的矩阵，n与原问题中的列数相同，也就是维度
                        new_constraint = [0] * self.problem.diversion
                        # 增加约束([1,0],2
                        new_constraint[i] = 1
                        lower_problem.add_constraint(new_constraint, lower)
                        # 增加约束([-1,0],2
                        new_constraint[i] = -1
                        upper_problem.add_constraint(new_constraint, -1 * upper)
                        # 重新求解
                        solveProblem(lower_problem)
                        solveProblem(upper_problem)
                        # 生成新解节点，将新解放入解树
                        lower_node = ProblemNode(lower_problem, father)
                        upper_node = ProblemNode(upper_problem, father)
                        self.problem_list.add(lower_node)
                        self.problem_list.add(upper_node)

    def show(self):
        self.problem_list.show()

    def getBestSolution(self):
        print("==================================================================================")
        print("Now Printing The Best Optimization")
        result = 0
        while not self.problem_list.isEmpty():
            new = self.problem_list.pop().problem
            if new.solution.checkInt():
                if self.problem.max_mode:
                    if new.solution.result > result:
                        result = new.solution.result
                        best = new
                else:
                    if new.solution.result < result:
                        result = new.solution.result
                        best = new
        return best


if __name__ =="__main__":
    p = Problem([13, 8], True)
    p.add_constraint([1, 2], 10)
    p.add_constraint([5, 2], 20)

    t = Simplex(p)
    solution = t.solve()
    p.solution.show()
    b = BranchAndBound(p)
    b.branch()
    b.show()
    b.getBestSolution().solution.show()
