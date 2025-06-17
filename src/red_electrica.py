from abc import ABC, abstractmethod

from sympy import roots, sympify
from sympy.abc import s


class RedElectricaBase(ABC):
    """
    Clase base para representar una red eléctrica.
    Esta clase define la estructura básica de una red eléctrica y sus operaciones.
    """

    @abstractmethod
    def ceros_y_polos(self):
        """
        Método abstracto para calcular los ceros y polos de la red.
        Debe ser implementado por las subclases.
        """
        pass

    @abstractmethod
    def gain(self):
        """
        Método abstracto para calcular la ganancia de la red.
        Debe ser implementado por las subclases.
        """
        pass

    @staticmethod
    def paralelo(redes: list["RedElectrica"]) -> "RedElectrica":
        """
        Combina dos redes en paralelo.
        :param redes: Lista de redes
        :return: Nueva red combinada en paralelo
        """
        numerador = 1
        denominador = 0
        for red in redes:
            numerador *= red.expresion()
        for red in redes:
            denominador += numerador / red.expresion()
        return RedElectrica(numerador / denominador)

    @staticmethod
    def serie(redes: list["RedElectrica"]) -> "RedElectrica":
        """
        Combina varias redes en serie.
        :param redes: Lista de redes
        :return: Nueva red combinada en serie
        """
        expresion_total = 0
        for red in redes:
            expresion_total += red.expresion()
        return RedElectrica(expresion_total)


class RedElectrica(RedElectricaBase):
    def __init__(self, expresion):
        self._expresion = sympify(expresion)

    def ceros_y_polos(self):
        """
        Calcula los ceros y polos de una expresión de transferencia.
        :param expresion: Expresión de transferencia
        :return: Tupla con los ceros y polos
        """
        num, den = self._expresion.as_numer_denom()
        ceros_dict = roots(num, s)
        polos_dict = roots(den, s)

        # Verificar coincidencias y eliminar el de menor grado
        coincidencias = set(ceros_dict) & set(polos_dict)

        for c in coincidencias:
            if ceros_dict[c] == polos_dict[c]:
                del ceros_dict[c]
                del polos_dict[c]
            elif ceros_dict[c] < polos_dict[c]:
                del ceros_dict[c]
            else:
                del polos_dict[c]

        return list(ceros_dict.keys()), list(polos_dict.keys())

    def gain(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def expresion(self):
        return self._expresion
