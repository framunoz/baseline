import abc
from abc import ABC
from typing import Tuple, Any

from telefonica.loaders import DataBase, FODB, RMDB, ClienteDB
from telefonica.nodos import FO, RM, Oferta, Cliente


class Contenedor(ABC):
    def __init__(self):
        self.nodos = None
        self.total = None
        self.indice = None

    def __len__(self):
        return len(self.nodos)


class NodosOferta(Contenedor):
    def __init__(self, path_fo, path_rm):
        super().__init__()
        self.fo_db: FODB = FODB(path_fo)
        self.rm_db: RMDB = RMDB(path_rm)
        args: tuple[Any, float, float]
        list_fo: list[Oferta] = [FO(*args) for args in self.fo_db.args]
        list_rm: list[Oferta] = [RM(*args) for args in self.rm_db.args]
        self.nodos: list[Oferta] = list_fo + list_rm
        self.total = sum([of.oferta for of in self.nodos])
        len_fo = len(list_fo)
        range_oferta = list(range(len(self)))
        self.indice = set(range_oferta)
        self.indice_fo = set(range_oferta[:len_fo])
        self.indice_rm = set(range_oferta[len_fo:])


class NodosDemanda(Contenedor):
    def __init__(self, path):
        super().__init__()
        self.db: ClienteDB = ClienteDB(path)
        self.nodos: list[Cliente] = [Cliente(*args) for args in self.db.args]
        self.total = len(self)
        self.indice = set(range(len(self)))
