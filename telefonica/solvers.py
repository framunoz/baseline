import numpy as np
import pulp

from telefonica.contenedores import NodosOferta, NodosDemanda


class Solver:
    def __init__(self, oferta: NodosOferta, demanda: NodosDemanda, a=1, b=1, c_fo=150, c_rm=600):

        # Nodos oferta y demanda
        self.oferta = oferta
        self.demanda = demanda

        # Constantes
        self.a = a
        self.b = b
        self.c_fo = c_fo
        self.c_rm = c_rm

        # Matriz de Costos
        self.matriz_costos = np.zeros((len(self.oferta), len(self.demanda)))
        for i in self.oferta.indice_fo:
            self.matriz_costos[i] = a
        for i in self.oferta.indice_rm:
            self.matriz_costos[i] = b

        # Definición del modelo
        self.modelo = pulp.LpProblem("telefonica", pulp.LpMaximize)
        self.x = pulp.LpVariable.dicts(
            "x",
            (ind for ind in zip(self.oferta.indice, self.demanda.indice)),
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
            self.modelo += pulp.lpSum([self.x[i, j] for j in self.demanda.indice]) <= self.oferta[i].oferta

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

    def construir_modelo(self):
        self.definir_funcion_objetivo()
        self.definir_restricciones()

    def resolver(self, verbose=False):
        self.modelo.solve()
        if verbose:
            print("Estado: " + pulp.LpStatus[self.modelo.status])

    @property
    def variables(self):
        return self.modelo.variables()
