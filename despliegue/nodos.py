import abc
from abc import ABC


class Nodo(ABC):
    """
    Representa un nodo. Puede ser una Fibra Óptica (FO), Red Móvil (RM), Clientes o Sumidero
    """

    def __init__(self, identificador, lat, lon):
        self.id = identificador
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return (self.__class__.__name__ + "("
                + "id=" + str(self.id) + ", "
                + "lat=" + str(self.lat) + ", "
                + "lon=" + str(self.lon)
                + ")")

    @abc.abstractmethod
    def dist_1(self, other) -> float:
        pass

    @abc.abstractmethod
    def dist_2(self, other) -> float:
        pass


class Cliente(Nodo):
    """
    Cliente
    """

    def dist_1(self, other) -> float:
        pass

    def dist_2(self, other) -> float:
        pass


class Oferta(Nodo, ABC):
    def __init__(self, identificador, lat, lon, vacancia):
        Nodo.__init__(self, identificador, lat, lon)
        self.vacancia = vacancia

    def __repr__(self):
        return (super().__repr__()[:-1] + ", "
                + "vacancia=" + str(self.vacancia)
                + ")")


class FO(Oferta):
    """
    Fibra Óptica
    """

    def dist_1(self, other) -> float:
        pass

    def dist_2(self, other) -> float:
        pass


class RM(Oferta):
    """
    Red Móvil
    """

    def dist_1(self, other) -> float:
        pass

    def dist_2(self, other) -> float:
        pass


class Sumidero(Oferta):
    """
    Sumidero. Nodo Auxiliar para la oferta.
    """

    def __init__(self):
        super().__init__(0, 0., 0., 0)

    def dist_1(self, other) -> float:
        pass

    def dist_2(self, other) -> float:
        pass
