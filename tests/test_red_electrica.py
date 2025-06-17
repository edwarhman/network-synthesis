import pytest
from sympy import sqrt

from src.red_electrica import (
    RedElectrica,
)
from tests.utils import comparar_expresiones


class TestRedElectrica:
    @pytest.mark.parametrize(
        "expresion, resultado_esperado",
        [
            ("s**2 + 2*s + 1", "s**2 + 2*s + 1"),
            ("s**3 + 3*s**2 + 3*s + 1", "s**3 + 3*s**2 + 3*s + 1"),
            ("s**4 + 4*s**3 + 6*s**2 + 4*s + 1", "s**4 + 4*s**3 + 6*s**2 + 4*s + 1"),
        ],
    )
    def test_inicializacion(self, expresion, resultado_esperado):
        # Arrange
        red = RedElectrica(expresion)
        # Act
        expresion_resultado = red.expresion()
        # Assert
        assert comparar_expresiones(expresion_resultado, resultado_esperado)

    @pytest.mark.parametrize(
        "expresion, ceros_esperados, polos_esperados",
        [
            ("s**2 + 2*s + 1", [-1], []),
            (
                "s*(s**2 + 2)*(s**2 + 6)/((s**2 + 1)*(s**2 + 4))",
                [-sqrt(-2), sqrt(-2), -sqrt(-6), sqrt(-6), 0],
                [-sqrt(-1), sqrt(-1), -sqrt(-4), sqrt(-4)],
            ),
        ],
    )
    def test_ceros_y_polos(self, expresion, ceros_esperados, polos_esperados):
        # Arrange
        red = RedElectrica(expresion)
        # Act
        ceros, polos = red.ceros_y_polos()
        # Assert
        assert ceros == ceros_esperados
        assert polos == polos_esperados

    def test_metodos_no_implementados(self):
        # Test that methods raise NotImplementedError
        red = RedElectrica("s**2 + 2*s + 1")

        with pytest.raises(NotImplementedError):
            red.gain()

    def test_serie(self):
        # Arrange
        red1 = RedElectrica("s + 1")
        red2 = RedElectrica("s**2 + 2*s + 1")
        # Act
        red_serie = RedElectrica.serie([red1, red2])
        # Assert
        assert comparar_expresiones(red_serie.expresion(), "s**2 + 3*s + 2")

    def test_paralelo(self):
        # Arrange
        red1 = RedElectrica("s + 1")
        red2 = RedElectrica("s**2 + 2*s + 1")
        # Act
        red_paralelo = RedElectrica.paralelo(red1, red2)
        # Assert
        assert comparar_expresiones(
            red_paralelo.expresion(), "(s + 1)*(s**2 + 2*s + 1)/(s**2 + 3*s + 2)"
        )
