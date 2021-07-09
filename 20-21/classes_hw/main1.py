from sys import stdin
from typing import List, Tuple
import copy


class Matrix:
    def __init__(self, list_of_lists: List[List[float]]):
        new_l_of_lts = copy.deepcopy(list_of_lists)
        self.matrix = new_l_of_lts

    def __str__(self) -> str:
        string_matrix = []
        column_limiter = 1
        for row in self.matrix:
            row_limiter = 1
            for el in row:
                string_matrix.append(str(el))
                if len(row) > row_limiter:
                    string_matrix.append('\t')
                row_limiter += 1
            if len(self.matrix) > column_limiter:
                string_matrix.append('\n')
            column_limiter += 1
        return ''.join(string_matrix)

    def size(self) -> Tuple[int, int]:
        rows = 0
        columns = 0
        for row in self.matrix:
            rows += 1
            columns = len(row)
        return rows, columns

# Task 1 check 1
m = Matrix([[1, 0], [0, 1]])
print(m)
m = Matrix([[2, 0, 0], [0, 1, 10000]])
print(m)
m = Matrix([[-10, 20, 50, 2443], [-5235, 12, 4324, 4234]])
print(m)
# Task 1 check 2
m1 = Matrix([[1, 0, 0], [1, 1, 1], [0, 0, 0]])
m2 = Matrix([[1, 0, 0], [1, 1, 1], [0, 0, 0]])
print(str(m1) == str(m2))
# Task 1 check 3
m = Matrix([[1, 1, 1], [0, 100, 10]])
print(str(m) == '1\t1\t1\n0\t100\t10')