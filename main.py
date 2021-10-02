from os import path

import pandas as pd

from despliegue.contenedores import NodosOferta, NodosDemanda
from despliegue.loaders import ClienteDB, OfertaDB
from despliegue.solvers import Solver3

# Constantes
PATH_DATA = path.join("./data/")  # Path donde estarán los Excels
PATH_CLIENTES = path.join(PATH_DATA, "Direcciones_Colina.xlsx")  # Path de los clientes
PATH_FO = path.join(PATH_DATA, "CTO_Colina.xlsx")  # Path donde estará las CTO's
PATH_RM = path.join(PATH_DATA, "SITIOS 4G TDD.xlsx")  # Path donde estarán las antenas de RM
PATH_RESULTADOS = path.join(PATH_DATA, "resultado.xlsx")

COLS_CLIENTES = ["pcm_area_tel", "gl_lat_OK", "gl_lon_OK"]
COLS_FO = ["id_pto_ftth", "latitud_ok", "longitud_ok", "eqpt_vg_qty"]
COLS_RM = None

A, B = 2, 1
C_FO, C_RM = 150, 600


def main():
    # DataFrames
    df_clientes = pd.read_excel(PATH_CLIENTES)
    df_clientes = df_clientes[df_clientes.gl_lat_OK <= -1]  # limpiamos aquellos que sean de lat-lon=0
    df_fo = pd.read_excel(PATH_FO)
    df_rm = pd.read_excel(PATH_RM)
    df_rm["vacancia"] = 30

    # Conexión a los Datos
    cliente_db = ClienteDB(df=df_clientes, col_names=COLS_CLIENTES)
    fo_db = OfertaDB(df=df_fo, col_names=COLS_FO)
    rm_db = OfertaDB(df=df_rm, col_names=COLS_RM)  # Las columnas justamente están ordenadas en [id, lat, lon, vac]

    # Conjuntos de nodos
    nodos_oferta = NodosOferta(fo_db, rm_db)
    nodos_demanda = NodosDemanda(cliente_db)

    # Optimización
    modelo3 = Solver3(nodos_oferta, nodos_demanda, a=A, b=B, c_fo=C_FO, c_rm=C_RM)
    modelo3.resolver()
    modelo3.save(PATH_RESULTADOS)


if __name__ == '__main__':
    main()
