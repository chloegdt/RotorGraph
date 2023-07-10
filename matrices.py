from smithnormalform import matrix, snfproblem, z

class Matrix(matrix.Matrix):
    
    def __init__(self, obj):
        if type(obj).__name__ == "RotorGraph":
            obj = obj.laplacian_matrix()
        elif not isinstance(obj, dict):
            raise TypeError("obj has to be a RotorGraph or a dict")
        
        self.dictionnary = obj
        n = len(obj)
        m = len(next(iter(obj.values())))
        values = [z.Z(v) for line in obj.values() for v in line.values()]
        matrix.Matrix.__init__(self, n, m, values)

    def snf_problem(self):
        """
        Compute the smith normal form problem of the matrix
        No input
        Output:
            - SNFProblem
        """
        prob = snfproblem.SNFProblem(self)
        prob.computeSNF()
        
        for i in range(min(self.h, self.w)):
            if prob.J.get(i,i).a < 0:
                prob.J.set(i,i, prob.J.get(i,i)*z.Z(-1))
                for j in range(self.w):
                    prob.S.set(i,j,prob.S.get(i,j)*z.Z(-1))
        
        if not prob.isValid:
            raise ValueError("Prob is not valid")

        if not (prob.S*self*prob.T == prob.J):
            raise ValueError("J != S*A*T")
        
        return prob

            

