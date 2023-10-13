class Matrix:
    def __init__(self, elements):
        if self.is_valid(elements):
            self.elements = elements
        else:
            raise Exception("Not a valid matrix \ncorrect format: List[List]")
    def is_valid(self, matrix = None):
        if matrix == None:
            matrix = self.elements
        if type(matrix) != list or type(matrix[0]) != list:
            return False
        for row in matrix:
            if len(row) != len(matrix[0]):
                return False
        return True
    def __str__(self):
        mat = ""
        for row in self.elements:
            mat += str(row) + '\n'
        return mat + '\n(' + str(len(row)) + ' x '+ str(len(self.elements)) + ' matrix)'
    def dimensions(self):
        '''
        returns the dimension of the matrix as:
        (row, column)
        '''
        return f"({len(self.elements)} x {len(self.elements[0])})"
    def get_element_by_pos(self, i, j):
        '''
        returns an element of the given position
        '''
        if i < 1 or i > len(self.elements):
            raise Exception("row not found")
        if j < 1 or j > len(self.elements[0]):
            raise Exception("column not found")
        return self.elements[i-1][j-1]
    def get_row_by_pos(self, i):
        if i < 1 or i > len(self.elements)+1:
            raise Exception("row not found")
        return self.elements[i-1]
    def get_col_by_pos(self, j):
        if j < 1 or j > len(self.elements[0]) + 1:
            raise Exception("col not found")
        col = []
        for row in self.elements:
            col.append(row[j-1])
        return col
    def __getitem__(self, index):
        return self.elements[index]
    def __add__(self, other_mat):
        if type(other_mat) != Matrix:
            raise Exception("Can only add to a Matrix type")
        if self.dimensions() != other_mat.dimensions():
            raise Exception("Not of the same dimensions")
        new_mat = []
        i = 0
        while i < len(other_mat.elements):
            new_mat.append([])
            j = 0
            while j < len(other_mat[0]):
                new_mat[i].append(self.elements[i][j] + other_mat[i][j])

                j += 1
            i += 1
        return Matrix(new_mat)
    def __sub__(self, other_mat):
        if type(other_mat) != Matrix:
            raise Exception("Can only perform operation to a Matrix type")
        if self.dimensions() != other_mat.dimensions():
            raise Exception("Not of the same dimensions")
        new_mat = []
        i = 0
        while i < len(other_mat.elements):
            new_mat.append([])
            j = 0
            while j < len(other_mat[0]):
                new_mat[i].append(self.elements[i][j] - other_mat[i][j])
                j += 1
            i += 1
        return Matrix(new_mat)
    def __mul__(self, other_mat):
        if not type(other_mat) in (Matrix, int):
            raise Exception("Can only perform operation an integer or Matrix")
        if type(other_mat) == int:
            new_mat = []
            i = 0
            while i < len(self.elements):
                new_mat.append([])
                j = 0
                while j < len(self.elements[0]):
                    new_mat[i].append(self.elements[i][j] * other_mat)
                    j += 1
                i += 1
            return Matrix(new_mat)
        if self.dimensions()[5] != other_mat.dimensions()[1]:
            raise Exception("Dimensions of matrices not compatible (m x n) * (n x q)")
        new_mat = []
        i = 0
        while i < len(self.elements):
            new_mat.append([])
            j = 0
            while j < len(other_mat.elements[0]):
                k,l = 0,0
                while k < len(self.elements[0]):
                    l += self.elements[i][k] * other_mat.get_col_by_pos(j + 1)[k]
                    k += 1
                new_mat[i].append(l)
                l = 0
                j += 1
            i += 1
        return Matrix(new_mat)
    def __truediv__(self, num):
        if type(num) != int:
            raise Exception("Can only divide a matrix with a number")
        new_mat = []
        i = 0
        while i < len(self.elements):
            new_mat.append([])
            j = 0
            while j < len(self.elements[0]):
                new_mat[i].append(self.elements[i][j] / num)
                j += 1
            i += 1
        return Matrix(new_mat)
    def transpose(self):
        new_mat = []
        i = 0
        while i < len(self.elements[0]):
            new_mat.append([])
            j = 0
            while j < len(self.elements):
                new_mat[i].append(self.elements[j][i])
                j += 1
            i += 1
        return Matrix(new_mat)
    def is_square(self):
        return self.dimensions()[1] == self.dimensions()[5]
    def determinant_2_by_2(self):
        if self.is_square() == False:
            raise Exception("Only a square matrix can have a determinant")
        if len(self.elements) > 2:
            raise Exception("This method can only for a 2 by 2 matrix try the determinant method")
        return self.elements[0][0] * self.elements[1][1] - self.elements[1][0] * self.elements[0][1]
    def minor(self, i,j):
        if self.is_square() == False:
            raise Exception("Only a square matrix can use this method")
        if i > len(self.elements) or j > len(self.elements):
            raise Exception("Element not found for this position")
        new_mat = []
        t = 0
        for a,b in enumerate(self.elements):
            if a == i:
                continue
            new_mat.append([])
            for c,d in enumerate(self.elements[a]):
                if c == j:
                    continue
                new_mat[t].append(d)
            t += 1
        return Matrix(new_mat)
    def determinant(self, j = 0):
        if self.is_square() == False:
            raise Exception("Only a square matrix can have a determinant")
        if len(self.elements) == 2:
            return self.determinant_2_by_2()
        if j % 2 == 0:
            sign = 1
        else:
            sign = -1
        if len(self.minor(0,j).elements) <= 2:
            if j == len(self.elements) - 1:
                return sign * self.elements[0][j] * self.minor(0,j).determinant_2_by_2()
            return sign * self.elements[0][j] * self.minor(0,j).determinant_2_by_2() + self.determinant(j + 1)
        else:
            if j == len(self.elements) - 1:
                return sign * self.elements[0][j] * self.minor(0,j).determinant()   
            return sign * self.elements[0][j] * self.minor(0,j).determinant() + self.determinant(j + 1)
    def cofactor(self):
        new_mat = []
        for index,row in enumerate(self.elements):
            new_mat.append([])
            for jndex,element in enumerate(row):
                if (index + jndex) % 2 == 0:
                    sign = 1
                else:
                    sign = -1
                new_mat[index].append(sign * self.minor(index,jndex).determinant())
        return Matrix(new_mat)
    def adjoint(self):
        if len(self.elements) == 2:
            return Matrix([[self.elements[1][1],-self.elements[0][1]],[-self.elements[1][0], self.elements[0][0]]])
        return self.cofactor().transpose()
    def inverse(self):
        return self.adjoint() / self.determinant()
