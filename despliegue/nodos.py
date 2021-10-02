import abc
import math
from abc import ABC

R = 6.3781e6  # Radio de la Tierra


def _dist_p(dx, dy, p=2):
    return (abs(dx) ** p + abs(dy) ** p) ** (1 / p)


class Nodo(ABC):
    """
    Representa un nodo. Puede ser una Fibra Óptica (FO), Red Móvil (RM), Clientes o Sumidero
    """

    def __init__(self, identificador, lat, lon):
        self.id = identificador
        self.lat, self.lon = lat, lon
        k = math.tau / 360
        self.lat_rad, self.lon_rad = lat * k, lon * k

    def __repr__(self):
        return (self.__class__.__name__ + "("
                + "id=" + str(self.id) + ", "
                + "lat=" + str(self.lat) + ", "
                + "lon=" + str(self.lon)
                + ")")

    @abc.abstractmethod
    def __sub__(self, other) -> (float, float):
        pass

    @abc.abstractmethod
    def dist_1(self, other) -> float:
        """
        Representa la distancia entre las calles. Se aproxima con la 1-distancia.

        :param other: Otro Nodo
        :return: la distancia entre el nodo actual y el siguiente nodo
        """
        pass

    @abc.abstractmethod
    def dist_2(self, other) -> float:
        """
        Representa la distancia de la esfera. Corresponde a la 2-distancia.

        :param other: Otro Nodo
        :return: la distancia entre el nodo actual y el siguiente nodo
        """
        pass


class Cliente(Nodo):
    """
    Cliente
    """

    def __sub__(self, other: Nodo) -> (float, float):
        d_lat, d_lon = self.lat_rad - other.lat_rad, self.lon_rad - other.lon_rad
        return d_lat * R, d_lon * R

    def dist_1(self, other: Nodo) -> float:
        if isinstance(other, Cliente):
            return _dist_p(*(self - other), p=1)
        return other.dist_1(self)  # Double Dispatch

    def dist_2(self, other: Nodo) -> float:
        if isinstance(other, Cliente):
            return _dist_p(*(self - other), p=2)
        return other.dist_2(self)  # Double Dispatch


class Oferta(Nodo, ABC):
    def __init__(self, identificador, lat, lon, vacancia):
        Nodo.__init__(self, identificador, lat, lon)
        self.vacancia = vacancia

    def __repr__(self):
        return (super().__repr__()[:-1] + ", "
                + "vacancia=" + str(self.vacancia)
                + ")")

    def __sub__(self, other: Nodo) -> (float, float):
        d_lat, d_lon = self.lat_rad - other.lat_rad, self.lon_rad - other.lon_rad
        return d_lat * R, d_lon * R

    def dist_1(self, other: Nodo) -> float:
        return _dist_p(*(self - other), p=1)

    def dist_2(self, other: Nodo) -> float:
        return _dist_p(*(self - other), p=2)


class FO(Oferta):
    """
    Fibra Óptica
    """


class RM(Oferta):
    """
    Red Móvil
    """


class Sumidero(Oferta):
    """
    Sumidero. Nodo Auxiliar para la oferta.
    """

    def __init__(self):
        super().__init__(0, 0., 0., 0)

    def dist_1(self, other: Nodo) -> float:
        return 0.

    def dist_2(self, other: Nodo) -> float:
        return 0.
