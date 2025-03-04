import sympy as sp


class SintesisRedes:
    def __init__(self, ceros, polos, A=1):
        """
        Constructor de la clase
        :param ceros: Ceros de la red
        :param polos: Polos de la red
        :param A: Ganancia de la red
        """
        self.s = sp.symbols('s')
        self.ceros = ceros
        self.polos = polos
        self.A = A
        self.polinomio = self.construir_polinomio(ceros, polos, A)


    def sintetizar_por_foster_I(self):
        """
        Sintetiza una red de Foster I
        :return: Polinomio de la red
        """
        s = self.s
        k_inf = self.calcular_limite(self.polinomio / s, s, sp.oo)
        k0 = self.calcular_limite(self.polinomio * s, s, 0)
        ks = []
        for polo in self.polos:
            if(polo == 0):
                continue
            polinomio = (self.polinomio * (s**2 + polo)/s).subs(s, s**(1/2))
            ki = self.calcular_limite(polinomio, s, -polo)
            ks.append(ki)
        return (k_inf, k0) + tuple(ks)
    

    def construir_polinomio(self, ceros, polos, A):
        """
        Construye un polinomio a partir de sus ceros y polos
        :param ceros: Ceros del polinomio
        :param polos: Polos del polinomio
        :return: Polinomio
        """
        s = self.s
        polinomio = A
        for cero in ceros:
            if(cero != 0):
                polinomio *= (s**2 + cero)
            else:
                polinomio *= s
        for polo in polos:
            if(polo != 0):
                polinomio /= (s**2 + polo)
            else:
                polinomio /= s
        return polinomio
    

    def calcular_limite(self, polinomio, variable, punto_a_evaluar):
        """
        Calcula el limite de un polinomio en un punto
        :param polinomio: Polinomio a evaluar
        :param s: Punto a evaluar
        :return: Limite del polinomio en el punto
        """
        return sp.limit(polinomio, variable , punto_a_evaluar)

