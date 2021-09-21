from telefonica.loaders import FODB, RMDB, ClienteDB
from telefonica.nodos import FO, RM, Oferta, Cliente


class Solver:
    def __init__(self, fo_db: FODB, rm_db: RMDB, cliente_db: ClienteDB, a=1, b=1, c1=150, c2=150):
        # Bases de Datos
        self.fo_db = fo_db
        self.rm_db = rm_db
        self.cliente_db = cliente_db

        # Nodos de Oferta
        list_fo: list[Oferta] = [FO(*args) for args in self.fo_db.args]
        list_rm: list[Oferta] = [RM(*args) for args in self.rm_db.args]
        self.nodos_oferta: list[Oferta] = list_fo + list_rm
        self.n = len(self.nodos_oferta)
        self.oferta_total = sum([oferta.oferta for oferta in self.nodos_oferta])
        self.indices_fo = list(range(len(list_fo)))
        self.indices_rm = list(range(self.indices_fo[-1], self.n))

        # Nodos Demanda
        self.nodos_demanda: list[Cliente] = [Cliente(*args) for args in self.cliente_db.args]
        self.m = len(self.nodos_demanda)
        self.demanda_total = self.m


