class Vector:

    def __init__(self, configuration:dict=None):
        if isinstance(configuration, dict):
            self.configuration = configuration
        elif isinstance(configuration, RotorGraph):
            self.configuration = {node: 0 for node in configuration}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, RotorGraph or nothing")

    def __str__(self):
        return repr(self.configuration)

    def __repr__(self):
        return repr(self.configuration)

    def __add__(self, other: object or int) -> object:
        """
        Overload the + operator.
        Case: ParticleConfig + ParticleConfig
            for each node, do the sum of the particles in both configurations
        Case: ParticleConfig + integer
            for each node, add the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) + config2.get(n, 0) for n in set(config1) | set(config2)}
        elif isinstance(other, int):
            res_dic = {n: k + other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
        return ParticleConfig(res_dic)

    def __radd__(self, other: object or int) -> object:
        """
        Same method as __add__ except that it makes the + operator commutative. 
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) + config2.get(n, 0) for n in set(config1) | set(config2)}
        elif isinstance(other, int):
            res_dic = {n: k + other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
        return ParticleConfig(res_dic)

    def __sub__(self, other: object or int) -> object:
        """
        Overload the - operator.
        Case: ParticleConfig - ParticleConfig
            for each node, do the substraction of the particles in both configurations
        Case: ParticleConfig - integer
            for each node, substract the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) - config2.get(n, 0) for n in set(config1) | set(config2)}
        elif isinstance(other, int):
            res_dic = {n: k - other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
        return ParticleConfig(res_dic)

    def __mul__(self, other: int) -> object:
        """
        Overload the * operator.
        Case: ParticleConfig * integer
            for each node, multiply the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k * other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)

    def __rmul__(self, other: int) -> object:
        """
        Same method as __mul__ except that it makes the * operator commutative. 
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k * other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)

    def __truediv__(self, other: int) -> object:
        """
        Overload the / operator.
        Case: ParticleConfig / integer
            for each node, divide the number of particles by an integer
        Input: 
            - self: particle configuration
            - other: integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k // other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)

    def __floordiv__(self, other: int) -> object:
        """
        Overload the // operator.
        Case: ParticleConfig // integer
            for each node, divide the number of particles by an integer
        Input: 
            - self: particle configuration
            - other: integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k // other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)

    def __lt__(self, other: object or int) -> bool:
        """
        Overload the < operator.
        Case: ParticleConfig < ParticleConfig
            for each node, compare the particles in both configurations
        Case: ParticleConfig < integer
            for each node, compare the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - True if self < object
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) >= config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k >= other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")

    def __le__(self, other: object or int) -> bool:
        """
        Overload the <= operator.
        Case: ParticleConfig <= ParticleConfig
            for each node, compare the particles in both configurations
        Case: ParticleConfig <= integer
            for each node, compare the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - True if self <= object
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) > config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k > other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
    
    def __eq__(self, other: object or int) -> bool:
        """
        Overload the == operator.
        Case: ParticleConfig == ParticleConfig
            for each node, compare the particles in both configurations
        Case: ParticleConfig == integer
            for each node, compare the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - True if self == object
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) != config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k != other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
    
    def __ne__(self, other: object or int) -> bool:
        """
        Overload the != operator.
        Case: ParticleConfig != ParticleConfig
            for each node, compare the particles in both configurations
        Case: ParticleConfig != integer
            for each node, compare the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - True if self != object
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) == config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k == other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
    
    def __gt__(self, other: object or int) -> bool:
        """
        Overload the > operator.
        Case: ParticleConfig > ParticleConfig
            for each node, compare the particles in both configurations
        Case: ParticleConfig > integer
            for each node, compare the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - True if self > object
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) <= config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k <= other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")

    def __ge__(self, other: object or int) -> bool:
        """
        Overload the >= operator.
        Case: ParticleConfig >= ParticleConfig
            for each node, compare the particles in both configurations
        Case: ParticleConfig >= integer
            for each node, compare the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - True if self >= object
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) < config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k < other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")

        
    def __setitem__(self, index:object, value:object):
        """
        Overload the assignement operator.
        Set the value in dict at the given index.
        Input: 
            - self: vector
            - index: dictionnary key
            - value: value to store
        No ouput
        """
        self.configuration[index] = value

    def __getitem__(self, index: object):
        """
        Overload the getter operator.
        Return the value in dict at the given index.
        Input: 
            - self: vector
            - index: dictionnary key
        Output:
            - the value at the given index
        """
        self.configuration[index] = value

        return self.configuration[index]

    def __delitem__(self, index: object):
        """
        Overload the deleter operator.
        Input:
            - self: vector 
            - index: dictinnay key
        No output
        """
        del self.configuration[index]

    def __len__(self) -> int:
        """
        doc
        """
        return len(self.configuration)
