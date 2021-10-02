import abc

import numpy as np
import pulp

from despliegue.contenedores import NodosOferta, NodosDemanda


class AbstractSolver(abc.ABC):
    def __init__(self, oferta: NodosOferta, demanda: NodosDemanda, verbose):
        self.verbose = verbose

        # Nodos oferta y demanda
        self.oferta = oferta
        self.demanda = demanda
        self.oferta[-1].vacancia = len(demanda)  # Seteamos la vacancia del sumidero

        # Matriz de Costos
        self.matriz_costos = np.zeros((len(self.oferta), len(self.demanda)))

        # Definición del modelo
        self.modelo = pulp.LpProblem("despliegue", pulp.LpMaximize)
        self.x = None

    @abc.abstractmethod
    def definir_funcion_objetivo(self):
        pass

    @abc.abstractmethod
    def definir_restricciones(self):
        pass

    def construir_modelo(self):
        if self.verbose:
            print("Construyendo modelo...")
        self.definir_funcion_objetivo()
        self.definir_restricciones()

    def resolver(self):
        if self.verbose:
            print("Empezando a resolver...")
        self.modelo.solve()
        if self.verbose:
            print("Estado: " + pulp.LpStatus[self.modelo.status])

    @property
    def variables(self):
        return self.modelo.variables()


class Solver1(AbstractSolver):
    """
    Solver que utiliza muchas variables. Aunque sea factible, toma mucho tiempo.
    """

    def __init__(self, oferta: NodosOferta, demanda: NodosDemanda, a=1, b=1, c_fo=150, c_rm=600, verbose=False):
        super().__init__(oferta, demanda, verbose)

        # Constantes
        self.a = a
        self.b = b
        self.c_fo = c_fo
        self.c_rm = c_rm

        # Matriz de Costos
        for i in self.oferta.indice_fo:
            self.matriz_costos[i] = self.a
        for i in self.oferta.indice_rm:
            self.matriz_costos[i] = self.b

        # Definición del modelo
        self.x: pulp.LpVariable.dicts = pulp.LpVariable.dicts(
            "x",
            ((i, j) for i in self.oferta.indice for j in self.demanda.indice),
            cat="Binary"
        )

    def definir_funcion_objetivo(self):
        self.modelo += pulp.lpSum([
            pulp.lpSum([
                self.matriz_costos[i, j] * self.x[i, j] for j in self.demanda.indice
            ]) for i in self.oferta.indice
        ])

    def definir_restricciones(self):
        # Restricción de la Oferta
        for i in self.oferta.indice:
            self.modelo += pulp.lpSum([self.x[i, j] for j in self.demanda.indice]) <= self.oferta[i].vacancia

        # Restricción de la Demanda
        for j in self.demanda.indice:
            self.modelo += pulp.lpSum([self.x[i, j] for i in self.oferta.indice]) == 1

        # Restricción de la distancia en FO
        for i in self.oferta.indice_fo:
            for j in self.demanda.indice:
                o_i, d_j = self.oferta[i], self.demanda[j]
                self.modelo += self.x[i, j] * o_i.dist_1(d_j) <= self.c_fo

        # Restricción de la distancia en RM
        for i in self.oferta.indice_rm:
            for j in self.demanda.indice:
                o_i, d_j = self.oferta[i], self.demanda[j]
                self.modelo += self.x[i, j] * o_i.dist_2(d_j) <= self.c_rm
