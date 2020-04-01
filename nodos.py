class Nodo:
    '''This is an abstract class'''

class NodoAritmetico(Nodo) :

    def __init__(self,  tem, c3d) :
        self.tem = str(tem)
        self.c3d = c3d

class NodoLogico(Nodo) :

    def __init__(self,  etv, etf, c3d) :
        self.etv = etv
        self.etf = etf
        self.c3d = c3d

class NodoSubIf(Nodo) :

    def __init__(self, ets, c3d) :
        self.ets = ets
        self.c3d = c3d

class NodoIf(Nodo) :

    def __init__(self, c3d) :
        self.c3d = c3d

class NodoElse(Nodo) :

    def __init__(self, c3d) :
        self.c3d = c3d

class NodoSentencia(Nodo) :

    def __init__(self, c3d) :
        self.c3d = c3d