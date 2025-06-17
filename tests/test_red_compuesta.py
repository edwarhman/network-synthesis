import pytest

from src.red_paralela import RedParalela
from src.red_serie import RedSerie
from tests.utils import comparar_expresiones

paralelo = RedParalela
serie = RedSerie


class TestRedCompuesta:
    @pytest.mark.parametrize(
        "red, resultado_esperado",
        [
            (
                serie(
                    "4/27",
                    paralelo("1/27 * s", "1 / 9"),
                    paralelo("20 / 243 * s", "20 / 27"),
                ),
                "(s+4)*(s+1)/(s+9)/(s+3)",
            ),
            (
                serie(
                    paralelo("1 / 2", "1 / (2 * s)"), paralelo("1 / 6", "1 / (2 * s)")
                ),
                "(s + 2) / (s+3) / (s + 1)",
            ),
            (
                serie(
                    "1 / (4 / 15 * s)",
                    paralelo("5 / 2 / 2", "1 / (2 / 5 * s)"),
                    paralelo("15 / 4 / 4", "1 / (4 / 15 * s)"),
                ),
                "10*(s+3)*(s+1)/(s+4)/(s+2)/s",
            ),
            (
                paralelo(paralelo("3 / 16 * s + 3 / 16", "3 / 5 * s + 12 / 5"), "1"),
                "(s+4)*(s+1)/(s+3)/(s+9)",
            ),
            (
                paralelo(
                    serie("3 / 16 * s", "3 / 16"), serie("3 / 5 * s", "12 / 5"), "1"
                ),
                "(s+4)*(s+1)/(s+3)/(s+9)",
            ),
            (
                serie("16 / 3 / (s + 1)", "5 / 3 / (s + 4)", "1"),
                "(s + 3) * (s + 9) / (s + 1) / (s + 4)",
            ),
            (
                serie(
                    paralelo("16 / 3", "16 / 3 / s"),
                    paralelo("5 / 12", "5 / 3 / s"),
                    "1",
                ),
                "(s + 3) * (s + 9) / (s + 1) / (s + 4)",
            ),
            (
                serie(
                    paralelo("3 / 2 * s", "3 / 2"), paralelo("1 / 6 * s", "1 / 2"), "s"
                ),
                "s*(s + 4) * (s + 2) / (s + 3) / (s + 1)",
            ),
            (
                paralelo(paralelo("8 / 3 * s", "8 + 4 * s"), "8 * 4 / 3 + 8 / 3 * s"),
                "s*(s + 4) * (s + 2) / (s + 3) / (s + 1)",
            ),
        ],
    )
    def test_obtener_expresion(self, red, resultado_esperado):
        # Act
        expresion_resultado = red.expresion()
        # Assert
        assert comparar_expresiones(expresion_resultado, resultado_esperado)

    @pytest.mark.parametrize(
        "expresion, ceros_esperados, polos_esperados",
        [
            (
                serie(
                    "4/27",
                    paralelo("1/27 * s", "1 / 9"),
                    paralelo("20 / 243 * s", "20 / 27"),
                ),
                [-1, -4],
                [-3, -9],
            ),
            (
                serie(
                    paralelo("1 / 2", "1 / (2 * s)"), paralelo("1 / 6", "1 / (2 * s)")
                ),
                [-2],
                [-1, -3],
            ),
            (
                serie(
                    "1 / (4 / 15 * s)",
                    paralelo("5 / 2 / 2", "1 / (2 / 5 * s)"),
                    paralelo("15 / 4 / 4", "1 / (4 / 15 * s)"),
                ),
                [-1, -3],
                [-2, -4, 0],
            ),
            (
                paralelo(paralelo("3 / 16 * s + 3 / 16", "3 / 5 * s + 12 / 5"), "1"),
                [-1, -4],
                [-3, -9],
            ),
            (serie("16 / 3 / (s + 1)", "5 / 3 / (s + 4)", "1"), [-3, -9], [-1, -4]),
            (
                serie(
                    paralelo("16 / 3", "16 / 3 / s"),
                    paralelo("5 / 12", "5 / 3 / s"),
                    "1",
                ),
                [-3, -9],
                [-1, -4],
            ),
            (
                serie(
                    paralelo("3 / 2 * s", "3 / 2"), paralelo("1 / 6 * s", "1 / 2"), "s"
                ),
                [-2, -4, 0],
                [-1, -3],
            ),
            (
                paralelo(paralelo("8 / 3 * s", "8 + 4 * s"), "8 * 4 / 3 + 8 / 3 * s"),
                [-2, -4, 0],
                [-1, -3],
            ),
        ],
    )
    def test_ceros_y_polos(self, expresion, ceros_esperados, polos_esperados):
        # Act
        ceros, polos = expresion.ceros_y_polos()
        # Assert
        assert ceros == ceros_esperados
        assert polos == polos_esperados

    def test_metodos_no_implementados(self):
        # Test that methods raise NotImplementedError
        red = RedParalela(["s**2", "1"])

        with pytest.raises(NotImplementedError):
            red.gain()
