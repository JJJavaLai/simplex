
# Example
# maximize 13x1 + 8x2
#        st
#         x1 + 2x2 <= 10
#         5x1 + 2x2 <= 20
#         x1 ,x2 >= 0
from method import Simplex, BranchAndBound
from model import Problem

# p = Problem.Problem([-1, -14, -6])
# p.add_constraint([1, 1, 1], 4)
# p.add_constraint([1, 0, 0], 2)
# p.add_constraint([0, 0, 1], 3)
# p.add_constraint([0, 3, 1], 6)

p = Problem.Problem([13, 8], True)
p.add_constraint([1, 2], 10)
p.add_constraint([5, 2], 20)

t = Simplex.Simplex(p)
solution = t.solve()
if p.solution_flag:
    p.solution.show()
    b = BranchAndBound.BranchAndBound(p)
    b.branch()
    b.show()
    b.getBestSolution().solution.show()
else:
    print("No Solution for original problem")