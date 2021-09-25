import os
from abc import ABC

import pandas as pd


class DataBase(ABC):
    def __init__(self, path, col_names=None):
        self.path: bytes = os.path.join(path)
        self.col_names: list[str] = col_names
        self.df: pd.DataFrame = pd.DataFrame()

    def __len__(self) -> int:
        return len(self.df)

    @property
    def args(self):
        return self.df.values


class OfertaDB(DataBase):

    def __init__(self, path, col_names=None):
        """
        Constructor.

        :param path: El path del archivo .xlsx
        :param col_names: Una lista con los nombres de las columnas en el orden
            ["id", "latitud", "longitud", "vacancia"]. Si no se entrega se asume que el dataset contiene únicamente
            estas columnas en el mismo orden.
        """
        super().__init__(path, col_names)
        if col_names is not None:
            self.df: pd.DataFrame = pd.read_excel(self.path, dtype=object)[self.col_names]
        else:
            self.df: pd.DataFrame = pd.read_excel(self.path, dtype=object)
        self.df.columns = ["id", "lat", "lon", "vac"]


class ClienteDB(DataBase):
    def __init__(self, path, col_names=None):
        """
        Constructor.

        :param path: El path del archivo .xlsx
        :param col_names: Una lista con los nombres de las columnas en el orden ["id", "latitud", "longitud"].
            Si no se entrega se asume que el dataset contiene únicamente estas columnas en el mismo orden.
        """
        super().__init__(path, col_names)
        if col_names is not None:
            self.df: pd.DataFrame = pd.read_excel(self.path, dtype=object)[self.col_names]
        else:
            self.df: pd.DataFrame = pd.read_excel(self.path, dtype=object)
        self.df.columns = ["id", "lat", "lon"]


class SingletonMeta(type):
    """
    Para ocupar el patrón Singleton
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MatrizDistanciaCTO(metaclass=SingletonMeta):
    pass
