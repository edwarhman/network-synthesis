import sympy as sp
from abc import ABC, abstractmethod


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
        self.polinomio = self.construir_polinomio_complejos_conjugados(ceros, polos, A)


    @staticmethod
    def construir_polinomio_complejos_conjugados(ceros, polos, A=1):
        """
        Construye un polinomio a partir de sus ceros y polos
        :param ceros: Ceros del polinomio
        :param polos: Polos del polinomio
        :return: Polinomio
        """
        s = sp.symbols('s')
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
        
    @staticmethod        
    def construir_polinomio(ceros, polos, A=1):
        s = sp.symbols('s')
        polinomio = A
        for cero in ceros:
            polinomio *= (s + cero)
        for polo in polos:
            polinomio /= (s + polo)
        return polinomio

    
    @staticmethod
    def calcular_limite(polinomio, variable, punto_a_evaluar):
        """
        Calcula el limite de un polinomio en un punto
        :param polinomio: Polinomio a evaluar
        :param s: Punto a evaluar
        :return: Limite del polinomio en el punto
        """
        return sp.limit(polinomio, variable , punto_a_evaluar)


class RedSintetizada(ABC):
    @abstractmethod
    def polos_y_ceros(self):
        pass

    @abstractmethod
    def residuos(self):
        pass

    def polinomio(self):
        pass

    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def elementos(self):
        pass

    @abstractmethod
    def sintetizar(self):
        pass

class FosterI(RedSintetizada):
    def __init__(self, ceros, polos, A=1):
        super().__init__()
        self._ceros = ceros
        self._polos = polos
        self._polinomio = SintesisRedes.construir_polinomio_complejos_conjugados(ceros, polos, A)
        residuos = self.sintetizar()
        self._residuos = residuos

    
    def residuos(self):
        return self._residuos

    def polos_y_ceros(self):
        return (self._ceros, self._polos)

    def plot(self):
        return super().plot()

    def elementos(self):
        idx = 0
        elementos = [1/self._residuos[0]]
        for residuo in self._residuos[1:-1]:
            polos_no_nulos = [polo for polo in self._polos if polo != 0]
            inductancia = residuo / polos_no_nulos[idx]
            capacitancia = 1 / residuo
            elementos.append(inductancia)
            elementos.append(capacitancia)
            idx += 1

        elementos.append(self._residuos[-1])

        return elementos

    def sintetizar(self):
        """
        Sintetiza una red de Foster I
        :return: Polinomio de la red
        """
        s = sp.symbols('s')
        polinomio = self._polinomio
        polos = self._polos
        k_inf = SintesisRedes.calcular_limite(polinomio / s, s, sp.oo)
        k0 = SintesisRedes.calcular_limite(polinomio * s, s, 0)
        ks = [k0]
        for polo in polos:
            if(polo == 0):
                continue
            polinomio_ajustado = (polinomio * (s**2 + polo)/s).subs(s, s**(1/2))
            ki = SintesisRedes.calcular_limite(polinomio_ajustado, s, -polo)
            ks.append(ki)
        ks.append(k_inf)
        return ks

class FosterRC(RedSintetizada):
    def __init__(self, ceros, polos, A=1):
        super().__init__()
        self._ceros = ceros
        self._polos = polos
        self._polinomio = SintesisRedes.construir_polinomio(ceros, polos, A)
        residuos = self.sintetizar()
        self._residuos = residuos

    
    def residuos(self):
        return self._residuos

    def polos_y_ceros(self):
        return (self._ceros, self._polos)

    def plot(self):
        return super().plot()

    def elementos(self):
        idx = 0
        elementos = [1/self._residuos[0]]
        for residuo in self._residuos[1:-1]:
            polos_no_nulos = [polo for polo in self._polos if polo != 0]
            inductancia = residuo / polos_no_nulos[idx]
            capacitancia = 1 / residuo
            elementos.append(inductancia)
            elementos.append(capacitancia)
            idx += 1

        elementos.append(self._residuos[-1])

        return elementos

    def sintetizar(self):
        """
        Sintetiza una red de Foster I
        :return: Polinomio de la red
        """
        s = sp.symbols('s')
        polinomio = self._polinomio
        polos = self._polos
        k_inf = SintesisRedes.calcular_limite(polinomio, s, sp.oo)
        k0 = SintesisRedes.calcular_limite(polinomio * s, s, 0)
        ks = [k0]
        for polo in polos:
            if(polo == 0):
                continue
            polinomio_ajustado = (polinomio * (s + polo))
            ki = SintesisRedes.calcular_limite(polinomio_ajustado, s, -polo)
            ks.append(ki)
        ks.append(k_inf)
        return ks
