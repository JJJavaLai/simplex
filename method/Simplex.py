# @Time : 2021/10/7 下午12:19 
# @Author : Patrick.Lai
# @File : Simplex.py
# @Software: PyCharm
import numpy as np

from model.Solutions import Solution
from util import Utils


# Example
# maximize 13x1 + 8x2
#        st
#         x1 + 2x2 <= 10
#         5x1 + 2x2 <= 20
#         x1 ,x2 >= 0
# p = Problem([13, 8], True)
# p.add_constraint([1, 2], 10)
# p.add_constraint([5, 2], 20)
# t = Simplex(p)
# solution = t.solve()
# p.solution.show()


class Simplex:
    # init function, get the optimize mode and the matrix from problem
    def __init__(self, problem):  # default is solve min LP
        self.mat, self.max_mode, self.problem = problem.mat, problem.max_mode, problem

    def simplex(self, mat, m, n):
        # here, we try to find a variable is less then 0, this means we can make the target function more less.
        while mat[0, 1:].min() < 0:
            # get first minus variable
            col = np.where(mat[0, 1:] < 0)[0][0] + 1  # use Bland's method to avoid degeneracy. use mat[0].argmin() ok?

            row = self.getOutVariableIndex(mat, col)+1
            # f the coefficient of a variable is minus, it means the variable could
            # be soooo big that there is not a best answer, which means the problem is unbound
            if mat[row][col] <= 0:
                self.problem.no_solution()
                return None  # the theta is ∞, the problem is unbounded
            self.pivot(mat,row, col)
        # result = mat[0][0] * (1 if self.max_mode else -1)
        # values = {B[i]: mat[i, 0] for i in range(1, m) if B[i] < n}
        variable_values = mat[0:,0]
        values = {}
        # for i in len(variable_values):
        #     for j in range(1,n):
        result = variable_values[0] * (1 if self.max_mode else -1)
        for i in range(1, len(variable_values)):
            for j in range(1, n):
                if mat[i][j] == 1:
                    if np.sum(mat[0:,j]) == 1:
                        values[j] = variable_values[i]

        solution = Solution(Utils.sort(values), result)
        self.problem.solved(solution)
        return solution

    # pivot: in pivot, input mat and where to pivot. for the row contain the pivoting coordinate, it is only means
    # each element should be divided by the coefficient of the variable for example: constraint x1 + 2x2 + x3 = 10,
    # in mat it should be [10, 1, 2, 1, 0], we choose x2 as after pivot, it should be [10, 1, 2, 1, 0] / 2 = [5, 0.5,
    # 1, 0.5, 0] for other rows, it should be the coefficient of x2 multiply [5, 0.5, 1, 0.5, 0],
    # and do a subtraction between mat[row] and the result finally, for i row, do mat[i] - mat[row] * mat[i][col]
    def pivot(self, mat,row, col):
        mat[row] /= mat[row][col]
        for i in range(0, mat.shape[0]):
            if i != row:
                mat[i] -= mat[row] * mat[i][col]
    # find the best variable out, this method will find the smallest ratio of number in B and the number of efficients.
    # the right one we need is the smallest and greater than 0
    def getOutVariableIndex(self, mat,col):
        ratio = []
        for i in range(1, mat.shape[0]):
            if mat[i][col] > 0:
                ratio.append(mat[i, 0] / mat[i][col])
            else:
                ratio.append(0x7fffffff)

        return np.argmin(ratio)

    # in solve function:
    # first, make the matrix into a slack one, add a n*m matrix on the right of it
    # here, n is the number of row of matrix and m is the number - 1 of the matrix, it means how many variable we need.
    def solve(self):
        m, n = self.mat.shape  # m - 1 is the number slack variables we should add
        temp = np.vstack([np.zeros((1, m - 1)), np.eye(m - 1)])  # add diagonal array
        self.mat = np.hstack([self.mat, temp])  # combine them
        # go to simplex
        return self.simplex(self.mat, m, n)
