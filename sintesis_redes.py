import sympy as sp
from sympy.plotting import plot
from sympy.physics.control.lti import TransferFunction
from sympy.physics.control.control_plots import pole_zero_plot
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

    def graficar(self, destination, xlim, ylim):
        polinomio = self._polinomio
        p1 = plot(polinomio, xlim=xlim, ylim=ylim)
        p1.save(destination)

    def graficar_polos_zeros(self, destination):
        tf = TransferFunction(self._polinomio, sp.symbols('s'))
        p = pole_zero_plot(tf)
        p.save(destination)


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

class FosterII(FosterI):
    def __init__(self, ceros, polos, A=1):
        self._ceros = polos
        self._polos = ceros
        self._polinomio = SintesisRedes.construir_polinomio_complejos_conjugados(polos, ceros, A)
        residuos = self.sintetizar()
        self._residuos = residuos


class FosterIRC(RedSintetizada):
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
        a_2n = SintesisRedes.calcular_limite(polinomio, s, sp.oo)
        a_0 = SintesisRedes.calcular_limite(polinomio * s, s, 0)
        ks = [a_0]
        for polo in polos:
            if(polo == 0):
                continue
            polinomio_ajustado = (polinomio * (s + polo))
            a_i = SintesisRedes.calcular_limite(polinomio_ajustado, s, -polo)
            ks.append(a_i)
        ks.append(a_2n)
        return ks


class FosterIIRC(RedSintetizada):
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
        k_inf = SintesisRedes.calcular_limite(polinomio/s, s, sp.oo)
        k0 = SintesisRedes.calcular_limite(polinomio, s, 0)
        ks = [k0]
        for polo in polos:
            if(polo == 0):
                continue
            polinomio_ajustado = (polinomio / s * (s + polo))
            ki = SintesisRedes.calcular_limite(polinomio_ajustado, s, -polo)
            ks.append(ki)
        ks.append(k_inf)
        return ks

class FosterIRL(FosterIIRC):
    def elementos(self):
        idx = 0
        elementos = [self._residuos[0]]
        for residuo in self._residuos[1:-1]:
            polos_no_nulos = [polo for polo in self._polos if polo != 0]
            inductancia = residuo / polos_no_nulos[idx]
            resistencia = residuo
            elementos.append(inductancia)
            elementos.append(resistencia)
            idx += 1

        elementos.append(self._residuos[-1])
        return elementos

class FosterIIRL(FosterIRC):
    def __init__(self, ceros, polos, A=1):
        self._ceros = polos
        self._polos = ceros
        self._polinomio = SintesisRedes.construir_polinomio(polos, ceros, A)
        residuos = self.sintetizar()
        self._residuos = residuos

    def elementos(self):
        elementosRC =  super().elementos()
        elementosRL = [elemento for elemento in elementosRC]
        for i in range(1, len(elementosRC), 2):
            elementosRL[i] = 1 / elementosRL[i]
        return elementosRL



class CauerI(RedSintetizada):
    def __init__(self, numerador, denominador):
        self._numerador = numerador
        self._denominador = denominador
        self._polinomio = numerador / denominador
        self._s = sp.symbols('s')
        self._elementos = self.sintetizar()

    def sintetizar(self):
        numerador = sp.expand(self._numerador)
        denominador = sp.expand(self._denominador)
        cocientes = []
        residuo = 999
        while (residuo != 0):
            polyDen = sp.Poly(denominador, self._s)
            polyNum = sp.Poly(numerador, self._s)
            if polyDen.degree() == 0 and polyNum.degree() != 0:
                cociente = self._s * polyNum.LC() / denominador 
                residuo = numerador - self._s * polyNum.LC() 
                print(cociente, residuo)
            elif polyDen.degree() == 0 and polyNum.degree() == 0:
                cociente = numerador / denominador
                residuo = numerador % denominador
            else:
                cociente, residuo = sp.div(numerador, denominador)
            cocientes.append(cociente)
            numerador = denominador
            denominador = residuo
        return cocientes

    def residuos(self):
        return self._elementos
    
    def elementos(self):
        return self._elementos

    def polos_y_ceros(self):
        return self._numerador

    def plot(self):
        return super().plot()

class CauerII(RedSintetizada):
    def __init__(self, numerador, denominador):
        self._numerador = numerador
        self._denominador = denominador
        self._polinomio = numerador / denominador
        self._s = sp.symbols('s')
        self._elementos = self.sintetizar()

    def sintetizar(self):
        numerador = self._numerador
        denominador = self._denominador
        cocientes = []
        residuo = 99
        while (residuo != 0):
            numerador_coeffs = sp.expand(numerador).as_coefficients_dict()
            denominador_coeffs = sp.expand(denominador).as_coefficients_dict()
            # Find the lowest degree (minor degree) term in numerador and denominador
            min_degree_numerador = min([k.as_coeff_exponent(self._s)[1] for k in numerador_coeffs.keys()])
            min_degree_denominador = min([k.as_coeff_exponent(self._s)[1] for k in denominador_coeffs.keys()])

            # Get the coefficients corresponding to the lowest degree
            min_coeff_numerador = numerador_coeffs.get(self._s**min_degree_numerador, 0)
            min_coeff_denominador = denominador_coeffs.get(self._s**min_degree_denominador, 0)
            
            if min_degree_numerador > min_degree_denominador:
                aux = denominador 
                denominador = numerador
                numerador = aux
                cocientes.append(0)
            else: 
                cociente = min_coeff_numerador / min_coeff_denominador * self._s**(min_degree_numerador - min_degree_denominador)
                residuo = sp.expand(numerador - cociente * denominador)
                cocientes.append(cociente)
                numerador = denominador
                denominador = residuo
        return cocientes

    def residuos(self):
        return self._elementos
    
    def elementos(self):
        return self._elementos

    def polos_y_ceros(self):
        return self._numerador

    def plot(self):
        return super().plot()