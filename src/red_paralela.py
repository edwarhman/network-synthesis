from src.red_electrica import RedElectrica, RedElectricaBase


class RedParalela(RedElectricaBase):
    def __init__(self, *redes):
        redes_electricas = []
        for red in redes:
            if isinstance(red, RedElectrica):
                redes_electricas.append(red)
            else:
                redes_electricas.append(RedElectrica(red))
        self.redes = redes_electricas

    def ceros_y_polos(self):
        """
        Calcula los ceros y polos de una red en paralelo.
        :return: Tupla con los ceros y polos
        """
        return RedElectricaBase.paralelo(self.redes).ceros_y_polos()

    def expresion(self):
        """
        Devuelve la expresión de la red en paralelo.
        :return: Expresión de la red en paralelo
        """
        return RedElectricaBase.paralelo(self.redes).expresion()

    def gain(self):
        raise NotImplementedError("This method should be implemented by subclasses.")
