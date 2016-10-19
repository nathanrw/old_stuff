class matrix(object):
    def __init__(self,data):
        self.data = data
    def multiplied_by_matrix(self,X):
        
        if len(self.data) == len(X.data[0]):
            pass
        else:
            print "Multiplication Failed - Wrong Dimensions"
            exit

        A = self.data
        X = X.columnify()
        B = X.data
        
        
        return matrix(C)
    
    def plus_matrix(self,X):
        if len(self.data) == len(X.data) and \
           len(self.data[0]) == len(X.data[0]):
            pass
        else:
            print "Addition Failed - Wrong Dimensions"
            exit

        A = self.data
        B = X.data

        ptr1 = 0
        ptr2 = 0

        while ptr1 < len(A):
            while ptr2 < len(A[0]):
                A[ptr1][ptr2] += B[ptr1][ptr2]
                ptr2 += 1
            ptr1+=1

        return matrix(A)
        
    def plus_scalar(self,scalar):
        A = self.data
        for x in A:
            for y in x:
                y += scalar
        return matrix(A)

    def multiplied_by_scalar(self,scalar):
        B = []
        for x in self.data:
            b = []
            for y in x:
                b.append(y*scalar)
            B.append(b)
        return matrix(B)
    def _print(self):
        for x in self.data:
            print x

    def columnify(self):
        B = []
        b = []
        for i in range(0,len(self.data)):
            b = []
            for x in self.data:
                b.append(x[i])
            B.append(b)
        return matrix(B)

A = matrix([[2,6,1],
            [6,3,4],
            [0,8,2]]
           )
B = matrix([[1,0,0],
            [0,1,0],
            [0,0,1]]
           )
X = matrix([[1,0,2],
           [-1,3,1]]
           )
Y = matrix([[3,1],
            [2,1],
            [1,0]]
           )

C = A.multiplied_by_matrix(B)
C._print()
print ""
C = X.multiplied_by_matrix(Y)
C._print()
print ""
