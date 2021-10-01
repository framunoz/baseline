import os
from abc import ABC

import numpy as np
import pandas as pd


class DataBase(ABC):
    def __init__(self, path: bytes = None, df: pd.DataFrame = None, col_names: list[str] = None):
        self.path: bytes = os.path.join(path) if path is not None else None
        self.col_names: list[str] = col_names
        self.df: pd.DataFrame = df

    def __len__(self) -> int:
        return len(self.df)

    @property
    def args(self):
        return self.df.values

    def __repr__(self):
        return self.df.__repr__()


class OfertaDB(DataBase):

    def __init__(self, path: bytes = None, df: pd.DataFrame = None, col_names: list[str] = None):
        """
        Constructor.

        :param path: El path del archivo .xlsx
        :param col_names: Una lista con los nombres de las columnas en el orden
            ["id", "latitud", "longitud", "vacancia"]. Si no se entrega se asume que el dataset contiene únicamente
            estas columnas en el mismo orden.
        """
        super().__init__(path, df, col_names)
        if self.path is not None:
            self.df: pd.DataFrame = pd.read_excel(self.path, dtype=object)
        if self.col_names is not None:
            self.df: pd.DataFrame = self.df[self.col_names]
        self.df.columns = ["id", "lat", "lon", "vac"]


class ClienteDB(DataBase):
    def __init__(self, path: bytes = None, df: pd.DataFrame = None, col_names: list[str] = None):
        """
        Constructor.

        :param path: El path del archivo .xlsx
        :param col_names: Una lista con los nombres de las columnas en el orden ["id", "latitud", "longitud"].
            Si no se entrega se asume que el dataset contiene únicamente estas columnas en el mismo orden.
        """
        super().__init__(path, df, col_names)
        if self.path is not None:
            self.df: pd.DataFrame = pd.read_excel(self.path, dtype=object)
        if col_names is not None:
            self.df: pd.DataFrame = self.df[self.col_names]
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
    """
    Representa a una matriz de distancia
    """

    def __init__(self, n=None, m=None):

        if n is not None and m is not None:
            self.matriz: np.ndarray = np.zeros((n, m))
        else:
            self.matriz: np.ndarray = np.array([])

    def __getitem__(self, item):
        return self.matriz.__getitem__(item)

    def __setitem__(self, key, value):
        self.matriz.__setitem__(key, value)
