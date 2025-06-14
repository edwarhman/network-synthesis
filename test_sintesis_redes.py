from sintesis_redes import SintesisRedes, FosterI, FosterIRC, FosterIIRC, FosterIRL, FosterIIRL, CauerI, CauerII
from sympy import symbols, zoo, Poly, sympify
import pytest
import numpy as np

s = symbols('s')

def test_construir_polinomio():
    redes = [
        (SintesisRedes.construir_polinomio_complejos_conjugados([1, 2, 0], [3, 4]), (s**2 + 1)*(s**2 + 2)*s/(s**2 + 3)/(s**2 + 4)),
        (SintesisRedes.construir_polinomio_complejos_conjugados([1, 4], [2, 8, 0]), (s**2 + 1)*(s**2 + 4)/(s**2 + 2)/(s**2 + 8)/s),
    ]
    for red, resultado_esperado in redes:
        assert red == resultado_esperado


def test_fosterI_residuos():
    redes = [
        (FosterI([2, 6, 0], [1, 4], 1), [0, 5/3, 4/3, 1]),
        (FosterI([(3+5**(1/2))/2, (3-5**(1/2))/2], [0, 2], 1), [1/2, 1/2, 1]),
        (FosterI([1, 3], [0, 2, 4], 5), [15/8, 5/4, 15/8, 0]),
        (FosterI([0, 6/25], [1/5], 5), [0, 1/5, 5]),
        (FosterI([1/5], [0, 6/25], 1/5), [1/6, 1/30, 0]),
        (FosterI([0, 2, 6], [1, 4], 1), [0, 5/3, 4/3, 1]),
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


def test_fosterI_elementos():
    redes = [
        (FosterI([2, 6, 0], [1, 4], 1), [zoo, 5/3, 3/5, 1/3, 3/4, 1]),
        (FosterI([1, 3], [0, 2, 4], 5), [8/15, 5/8, 4/5, 15/32, 8/15, 0]),
        (FosterI([(3+5**(1/2))/2, (3-5**(1/2))/2], [0, 2], 1), [2,1/4,2,1]),
        (FosterI([0, 6/25], [1/5], 5), [zoo, 1, 5, 5]),
        (FosterI([1/5], [0, 6/25], 1/5), [6, 25/180, 30, 0]),
        (FosterI([0, 2, 6], [1, 4], 1), [zoo, 5/3, 3/5, 1/3, 3/4, 1]),
        (FosterI([1,4], [0, 2, 6], 1), [3, 1/8, 4, 5/72, 12/5, 0]),
        # (FosterI([1, 4], [3,9]), [zoo, 1/2, 2, 1/6, 2, 0])
    ]
    for red, resultado_esperado in redes:
        assert red.elementos() == pytest.approx(resultado_esperado)


def test_fosterII_polos_y_ceros():
    redes = [
        (FosterI([1,4], [2, 6, 0], 1), ([1, 4],[2,6,0])),
        (FosterI([0, 2, 4], [1,3], 5), ([0,2,4], [1,3],))
    ]
    for sintesis_foster, resultado_esperado in redes:
        assert sintesis_foster.polos_y_ceros() == pytest.approx(resultado_esperado)


def test_fosterII_residuos():
    redes = [
        (FosterI([9, 4, 0], [2, 8]), [0, 7/3, 2/3, 1]),
        (FosterI([0,2],[2.28**2, 0.61**2]), [0, 0.6627022, 0.33729772,0])
    ]
    for sintesis_foster, resultado_esperado in redes:
        assert sintesis_foster.residuos() == pytest.approx(resultado_esperado)


def test_fosterII_elementos():
    redes = [
        (FosterI([9, 4, 0], [2, 8]), [zoo, 7/6, 3/7, 1/12, 3/2, 1]),
        (FosterI([0,2],[2.28**2, 0.61**2]), [zoo, 0.6627022/(2.28**2), 1/0.6627022, 0.33729772/(0.61**2), 1/0.33729772,  0])
    ]
    for red, resultado_esperado in redes:
        assert red.elementos() == pytest.approx(resultado_esperado)


def test_fosterRC_polos_y_ceros():
    redes = [
        (FosterIRC([2], [1,3]), ([2], [1,3]))
    ]
    for red, resultado_esperado in redes:
        assert red.polos_y_ceros() == pytest.approx(resultado_esperado)

def test_fosterRC_residuos():
    redes = [
        (FosterIRC([2], [1,3]), [0, 1/2, 1/2, 0])
    ]
    for sintesis_foster, resultado_esperado in redes:
        assert sintesis_foster.residuos() == pytest.approx(resultado_esperado)


def test_fosterI_RC_elementos():
    redes = [
        (FosterIRC([2], [1,3]), [zoo, 1/2, 2, 1/6, 2, 0]),
    ]
    for red, resultado_esperado in redes:
        assert red.elementos() == pytest.approx(resultado_esperado)

def test_fosterII_RC_residuos():
    redes = [
        (FosterIIRC([1,3], [2]), [3/2, 1/2, 1]),
    ]
    for sintesis_foster, resultado_esperado in redes:
        assert sintesis_foster.residuos() == pytest.approx(resultado_esperado)


def test_fosterII_RC_elementos():
    redes = [
        (FosterIIRC([1,3], [2]), [2/3, 1/4, 2, 1])
    ]
    for red, resultado_esperado in redes:
        assert red.elementos() == pytest.approx(resultado_esperado)

def test_fosterI_RL_residuos():
    redes = [
        (FosterIRL([1, 4], [3,9]), [4/27, 1/9, 20/27, 0]),
        (FosterIRL([7.959, 0.484, 1.557], [1, 3], 5), [9.99634, 5.00025, 15.0034, 5])
    ]
    for sintesis_foster, resultado_esperado in redes:
        assert sintesis_foster.residuos() == pytest.approx(resultado_esperado)


# def test_fosterI_RL_elementos():
    # redes = [
        # (FosterIRL([1, 4], [3,9]), [4/27, 1/27, 1/9, 20/243, 20/27, 0]),
        # (FosterIRL([7.959, 0.484, 1.557], [1, 3], 5), [9.99634, 5.00025, 1/5, 15.0034/3, 1/15.0034, 5])
    # ]
    # for sintesis_foster, resultado_esperado in redes:
        # assert sintesis_foster.elementos() == pytest.approx(resultado_esperado)


def test_cauer_I():
    redes = [
        (CauerI(s*(s**2+4)*(s**2+25), (s**2+1)*(s**2+9)), [1, 1/19, 19**2/99, 11**2*9/(640*19), 640/99]),
        (CauerI((s**2+1)*(s**2+4), s*(s**2+2)*(s**2+8)), [0,1, 0.2, 25/13, 169/280, 14/13]), 
        (CauerI((s**5 + 8*s**3 + 12*s), (s**4 + 5*s**2 + 4)), [1, 1/3, 9/7, 49/60, 5/7]),
        (CauerI((s+2), (s+1)), [1, 1, 1])
    ]
    for red, resultado_esperado in redes:
        print([residuo for residuo in red.residuos()])
        print([residuo for residuo in red.elementos()])
        assert [Poly(elemento, s).all_coeffs()[0] for elemento in red.residuos()] == pytest.approx(resultado_esperado)

def test_cauer_II():
    redes = [
        # (CauerII(10*s*(s**2+4)*(s**2+2), (s**2+1)*(s**2+3)), [1, 1/19, 19**2/99, 11**2*9/(640*19), 640/99, 2]),
        # (CauerII((s**2+1)*(s**2+4), s*(s**2+2)*(s**2+8)), [1, 0.2, 25/13, 169/280, 14/13]),
        (CauerII(10*(s+1)*(s+3), s*(s+2)*(s+4)), [30/8, 32/70, 490/88, 484/105 ,15/22]),
        (CauerII((s*(s**2+2)*(s**2+6)), (s**2+1)*(s**2+4)), [0,1/3, 36/7, 49/96, 3072/105, 15/96]),
        (CauerII((10*s**5 + 60*s**3 + 80*s), (s**4 + 4*s**2 + 3)), [0, 3/80, 320/7, 49/880, 19360/42, 6/880]),
        (CauerII((s+1), (s+2)), [1/2,4,1/2])
    ]
    for red, resultado_esperado in redes:
        coefficients = extract_coefficients(red.residuos())
        assert coefficients == pytest.approx(resultado_esperado)

def extract_coefficients(elementos):
    coeffs_values = [list(sympify(elemento).as_coefficients_dict().values()) for elemento in elementos]
    flattened_coeffs = [item for sublist in coeffs_values for item in sublist]
    return flattened_coeffs
