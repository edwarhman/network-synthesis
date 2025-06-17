from src.red_electrica import RedElectrica, RedElectricaBase


class RedSerie(RedElectricaBase):
    def __init__(self, *redes):
        redesElectricas = []
        for red in redes:
            if isinstance(red, RedElectricaBase):
                redesElectricas.append(red)
            else:
                redesElectricas.append(RedElectrica(red))
        self.redes = redesElectricas

    def ceros_y_polos(self):
        """
        Calcula los ceros y polos de una red en serie.
        :return: Tupla con los ceros y polos
        """
        return RedElectricaBase.serie(self.redes).ceros_y_polos()

    def expresion(self):
        """
        Devuelve la expresión de la red en serie.
        :return: Expresión de la red en serie
        """
        return RedElectricaBase.serie(self.redes).expresion()

    def gain(self):
        raise NotImplementedError("This method should be implemented by subclasses.")
