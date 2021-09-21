import numpy as np

from telefonica.loaders import MatrizDistanciaCTO
from telefonica.nodos import FO

print(FO(3, 3.2, 123.3, 454))

lista = list(range(12))

print(lista[:5])
print(lista[5:])

array = np.zeros((4, 6))
array[0] = 1
print(array)

i1 = MatrizDistanciaCTO()
i1.a = 0
i2 = MatrizDistanciaCTO()
i2.a = 10

print(i1.a)
