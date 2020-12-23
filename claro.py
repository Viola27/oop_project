from claro_class import *
import time

elementi = 20

claro = claro_class()

linear1 = time.time()
claro.linear_fit(elementi)
linear2 = time.time()
claro.better_fit(elementi)
better2 = time.time()

print("Tempo fit lineare per "+str(elementi) +
      " elementi: "+str(round(linear2-linear1,2)))
print("Tempo fit con funzione di errore per "+str(elementi) +
      " elementi: "+str(round(better2-linear2,2)))
