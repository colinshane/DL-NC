import numpy as np

from..core import Base,TIME_SCALE

class Simple(Base):
    def __init__(self, in_feature, in_number, group):
        self.in_feature = in_feature
        self.in_number = in_number
        self.group = group

    def Possion(self):
        rng = np.random
        data = []
        for i in range (self.group):
            data_t = rng.poisson(i+1,(self.in_feature,self.in_number))
            data.append(data_t)
        return data

    def Tri_function(self):
        rng = np.random
        data = []
        cla = []

        def sin_fun(l,c,t):
            return (np.sin(c*t*TIME_SCALE)+1)/2

        def tent_map(l,c,t):
            temp = l
            if (temp<0.5 and temp>=0):
                temp = (c/50)*temp
                return temp
            elif(temp>=0.5 and temp <=1):
                temp = (c/50)*(1-temp)
                return temp
            else:
                return 0

        def constant(l,c,t):
            return c/100

        def chose_fun():
            c = rng.randint(0,3)
            if c == 0:
                return sin_fun,c
            elif c == 1:
                return tent_map,c
            elif c == 2:
                return constant,c

        def change_fun(rate):
            fun = rng.randint(1,101)
            if fun > 100*rate:
                return False
            else:
                return True



        for i in range(self.group):
            data_t = np.zeros(self.in_number)
            cla_t = np.zeros(self.in_number)
            cons = rng.randint(1,101)
            fun, c  = chose_fun()

            for t in range(self.in_number):
                if change_fun(0.05):
                    cons = rng.randint(1,101)
                    fun, c = chose_fun()
                    try:
                        data_t[t] = fun(data_t[t-1],cons,t)
                        cla_t[t] = c
                    except IndexError:
                        data_t[t] = fun(rng.randint(0,101),cons,t)
                        cla_t[t] = c
                else:
                    try:
                        data_t[t] = fun(data_t[t-1],cons,t)
                        cla_t[t] = c
                    except IndexError:
                        data_t[t] = fun(rng.randint(0,101),cons,t)
                        cla_t[t] = c

            data_t = data_t[np.newaxis,:]
            data.append(data_t)
            cla.append(cla_t)
        return data, cla
