from functools import reduce
from sympy import roots
from sympy.abc import s

def zeros_poles(expresion):
    """
    Calcula los ceros y polos de una expresión de transferencia.
    :param expresion: Expresión de transferencia
    :return: Tupla con los ceros y polos
    """
    num, den = expresion.as_numer_denom()
    ceros = roots(num, s)
    polos = roots(den, s)
    return ceros, polos

def parallel(elements):
    """
    Calcula la resistencia equivalente de dos resistencias en paralelo
    :param c1: Resistencia 1
    :param c2: Resistencia 2
    :return: Resistencia equivalente
    """
    numerador = reduce(lambda x, prod: x*prod, [1] + elements)
    denominador = reduce(lambda x, sum: x + sum, elements)
    return numerador / denominador

def voltage_divider(z1, impedances):
    """"
    Calcula el divisor de tensión entre dos impedancias en serie de un circuito eléctrico"
    :param z1: impedancia en la cual se calculará el voltage,
    :param z2: impedancia complementaria necesaria para calcular el divisor de voltaje
    """
    suma = reduce(lambda x, sum: x + sum, impedances)
    return z1 / (z1 + suma)