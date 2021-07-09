from sys import stdin
from typing import List, Tuple, Union
import copy


class Matrix:
    def __init__(self, list_of_lists: List[List[float]]):
        new_l_of_lts = copy.deepcopy(list_of_lists)
        self.matrix = new_l_of_lts

    def __repr__(self):
        for i in range(len(self.matrix)):
            for j in self.matrix[i]:
                print(j, end="\t")
            print("")

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

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if len(self.matrix) != len(other.matrix):
            raise MatrixError(self.matrix, other.matrix)

        c_other = copy.deepcopy(other)
        res = [[0 for x in range(len(self.matrix[0]))]
               for y in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(c_other.matrix[0])):
                res[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return Matrix(res)

    def __mul__(self, other: Union['Matrix', float]) -> 'Matrix':
        if isinstance(other, int):
            c_int = copy.deepcopy(other)
            res = [[0 for x in range(len(self.matrix))]
                   for y in range(len(self.matrix))]
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    res[i][j] = self.matrix[i][j] * c_int
            return Matrix(res)

        else:
            try:
                res = []
                for y in range(len(self.matrix[0])):
                    res.append([0 for x in range(len(other.matrix[0]))])
                for i in range(len(self.matrix)):
                    for j in range(len(other.matrix[0])):
                        for k in range(len(other.matrix)):
                            res[i][j] += self.matrix[i][k] * other.matrix[k][j]
                return Matrix(res)

            except:
                raise MatrixError(self.matrix, other.matrix)

    __rmul__ = __mul__

    def transpose(self) -> 'Matrix':
        res = [[self.matrix[j][i] for j
                in range(len(self.matrix))] for i
               in range(len(self.matrix[0]))]
        self.matrix = res
        res = Matrix(res)
        return res

    @staticmethod
    def transposed(m: 'Matrix') -> 'Matrix':
        copied_m = copy.deepcopy(m)
        res = copied_m.transpose()
        return res


class MatrixError(Exception):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = Matrix(matrix1)
        self.matrix2 = Matrix(matrix2)

    def __str__(self):
        return 'Problem with size of some matrix'


