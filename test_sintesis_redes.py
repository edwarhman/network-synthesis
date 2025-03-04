from sintesis_redes import SintesisRedes, FosterI
from sympy import symbols
import pytest

s = symbols('s')

def test_construir_polinomio():
    redes = [
        (SintesisRedes.construir_polinomio([1, 2, 0], [3, 4]), (s**2 + 1)*(s**2 + 2)*s/(s**2 + 3)/(s**2 + 4)),
        (SintesisRedes.construir_polinomio([1, 4], [2, 8, 0]), (s**2 + 1)*(s**2 + 4)/(s**2 + 2)/(s**2 + 8)/s),
    ]
    for red, resultado_esperado in redes:
        assert red == resultado_esperado


def test_sintetizar_por_foster_I():
    redes = [
        ([2, 6, 0], [1, 4], 1, (1, 0, 5/3, 4/3)),
        ([(3+5**(1/2))/2, (3-5**(1/2))/2], [0, 2], 1, (1, 1/2, 1/2)),
        ([1, 3], [0, 2, 4], 5, (0, 15/8, 5/4, 15/8))
    ]
    for ceros, polos, A, resultado_esperado in redes:
        assert SintesisRedes.sintetizar_por_foster_I(ceros, polos, A) == pytest.approx(resultado_esperado)


def test_fosterI_residuos():
    redes = [
        (FosterI([2, 6, 0], [1, 4], 1), (1, 0, 5/3, 4/3)),
        (FosterI([(3+5**(1/2))/2, (3-5**(1/2))/2], [0, 2], 1), (1, 1/2, 1/2)),
        (FosterI([1, 3], [0, 2, 4], 5), (0, 15/8, 5/4, 15/8))
    ]
    for sintesis_foster, resultado_esperado in redes:
        assert sintesis_foster.residuos() == pytest.approx(resultado_esperado)

def test_fosterI_polos_y_ceros():
    redes = [
        (FosterI([2, 6, 0], [1, 4], 1), ([2,6,0], [1, 4])),
        (FosterI([1, 3], [0, 2, 4], 5), ([1,3], [0,2,4]))
    ]
    for sintesis_foster, resultado_esperado in redes:
        assert sintesis_foster.polos_y_ceros() == pytest.approx(resultado_esperado)


