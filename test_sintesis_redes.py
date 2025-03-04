from sintesis_redes import SintesisRedes
from sympy import symbols
import pytest

s = symbols('s')

def test_construir_polinomio():
    redes = [
        (SintesisRedes([1, 2, 0], [3, 4]), (s**2 + 1)*(s**2 + 2)*s/(s**2 + 3)/(s**2 + 4)),
        (SintesisRedes([1, 4], [2, 8, 0]), (s**2 + 1)*(s**2 + 4)/(s**2 + 2)/(s**2 + 8)/s),
    ]
    for red, resultado_esperado in redes:
        assert red.polinomio == resultado_esperado


def test_sintetizar_por_foster_I():
    redes = [
        (SintesisRedes([2, 6, 0], [1, 4]), (1, 0, 5/3, 4/3)),
        (SintesisRedes([(3+5**(1/2))/2, (3-5**(1/2))/2], [0, 2]), (1, 1/2, 1/2)),
        (SintesisRedes([1, 3], [0, 2, 4], 5), (0, 15/8, 5/4, 15/8))
    ]
    for red, resultado_esperado in redes:
        assert red.sintetizar_por_foster_I() == pytest.approx(resultado_esperado)


