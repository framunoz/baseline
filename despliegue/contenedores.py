import abc
from abc import ABC

from despliegue.loaders import OfertaDB, ClienteDB
from despliegue.nodos import FO, RM, Oferta, Cliente, Sumidero


class Contenedor(ABC):
    def __init__(self):
        self.nodos = None
        self.total = None
        self.indice = None

    def __len__(self):
        return len(self.nodos)

    @abc.abstractmethod
    def __getitem__(self, item):
        pass


class NodosOferta(Contenedor):
    def __init__(self, path_fo, path_rm):
        super().__init__()
        self.fo_db: OfertaDB = OfertaDB(path_fo)
        self.rm_db: OfertaDB = OfertaDB(path_rm)
        list_fo: list[Oferta] = [FO(*args) for args in self.fo_db.args]
        list_rm: list[Oferta] = [RM(*args) for args in self.rm_db.args]
        self.nodos: list[Oferta] = list_fo + list_rm + [Sumidero()]
        self.total = sum([of.vacancia for of in self.nodos])
        len_fo = len(list_fo)
        range_oferta = list(range(len(self)))
        self.indice = set(range_oferta)
        self.indice_fo = set(range_oferta[:len_fo])
        self.indice_rm = set(range_oferta[len_fo:-1])
        # TODO: Añadir el nodo auxiliar!

    def __getitem__(self, item) -> Oferta:
        return self.nodos.__getitem__(item)


class NodosDemanda(Contenedor):
    def __init__(self, path):
        super().__init__()
        self.db: ClienteDB = ClienteDB(path)
        self.nodos: list[Cliente] = [Cliente(*args) for args in self.db.args]
        self.total = len(self)
        self.indice = set(range(len(self)))

    def __getitem__(self, item) -> Cliente:
        return self.nodos.__getitem__(item)
