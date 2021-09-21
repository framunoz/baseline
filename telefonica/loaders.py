import abc
import os
from abc import ABC


class XLSXLoader(ABC):
    """
    Utilizado para cargar los data frames.
    """

    MAIN_PATH = os.path.join("./")

    def __init__(self, path):
        self.path = os.path.join(self.MAIN_PATH, path)
        self.df = None


class MatrizDistanciaCTO(XLSXLoader):
    pass


class DataBase(XLSXLoader, ABC):
    # TODO: COMPLETAR!

    @property
    def lat(self) -> list[float]:
        return []

    @property
    def lon(self) -> list[float]:
        return []

    def __len__(self) -> int:
        return 0

    @property
    def args(self) -> zip[tuple[int, float, float]]:
        return zip(range(len(self.lat)), self.lat, self.lon)


class FODB(DataBase):
    pass


class RMDB(DataBase):
    pass


class ClienteDB(DataBase):
    pass
