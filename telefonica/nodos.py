from abc import ABC


class Nodo(ABC):
    """
    Representa un nodo. Puede ser una Fibra Óptica (FO), Red Móvil (RM), Clientes o Nodos Auxiliares
    """
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return (self.__class__.__name__ + "("
                + "id=" + str(self.id) + ", "
                + "lat=" + str(self.lat) + ", "
                + "lon=" + str(self.lon)
                + ")")

    def dist_1(self, other) -> float:
        return 0.

    def dist_2(self, other) -> float:
        return 0.


class Oferta(Nodo, ABC):
    def __init__(self, id, lat, lon, oferta):
        Nodo.__init__(self, id, lat, lon)
        self.oferta = oferta


class FO(Oferta):
    """
    Fibra Óptica
    """
    pass


class RM(Oferta):
    """
    Red Móvil
    """
    pass


class Cliente(Nodo):
    """
    Cliente
    """
    pass


# TODO: Borrar en el futuro
# class NodoAuxiliar(Nodo):
#     """
#     Nodo Auxiliar. Utilizado para la optimización.
#     """
