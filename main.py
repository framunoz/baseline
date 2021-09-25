import numpy as np

from despliegue.loaders import MatrizDistanciaCTO
from despliegue.nodos import FO

print(FO(3, 3.2, 123.3, 454))

lista = list(range(12))

print(lista[:5])
print(lista[5:])

array = np.zeros((4, 6))
array[0] = 1
print(array)

i1 = MatrizDistanciaCTO(3, 5)
i1[2, 3] = 5
i2 = MatrizDistanciaCTO()

print(i1.matriz)
