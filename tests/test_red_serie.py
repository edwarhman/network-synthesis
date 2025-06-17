import pytest

from src.red_serie import (
    RedSerie,
)
from tests.utils import comparar_expresiones


class TestRedSerie:
    @pytest.mark.parametrize(
        "expresion, resultado_esperado",
        [
            (["s**2", "2*s", "1"], "s**2 + 2*s + 1"),
            (["s**3", "3*s**2", "3*s", "1"], "s**3 + 3*s**2 + 3*s + 1"),
            (
                ["s**4", "4*s**3", "6*s**2", "4*s", "1"],
                "s**4 + 4*s**3 + 6*s**2 + 4*s + 1",
            ),
            (["s", "1", "1/s"], "s + 1 + 1/s"),
        ],
    )
    def test_obtener_expresion(self, expresion, resultado_esperado):
        # Arrange
        red = RedSerie(*expresion)
        # Act
        expresion_resultado = red.expresion()
        # Assert
        assert comparar_expresiones(expresion_resultado, resultado_esperado)

    @pytest.mark.parametrize(
        "expresion, ceros_esperados, polos_esperados",
        [
            (["s**2", "2*s", "1"], [-1], []),
            (["16 / 3 / (s + 1)", "5 / 3 / (s + 4)", "1"], [-3, -9], [-1, -4]),
        ],
    )
    def test_ceros_y_polos(self, expresion, ceros_esperados, polos_esperados):
        # Arrange
        red = RedSerie(*expresion)
        # Act
        ceros, polos = red.ceros_y_polos()
        # Assert
        assert ceros == ceros_esperados
        assert polos == polos_esperados

    def test_metodos_no_implementados(self):
        # Test that methods raise NotImplementedError
        red = RedSerie(["s**2 + 2*s + 1"])

        with pytest.raises(NotImplementedError):
            red.gain()
