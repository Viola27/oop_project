from claro_class import claro_class
import time

elementi = 20
chip = 10

claro = claro_class()

linear1 = time.time()
#claro.linear_fit(elementi, chip)
linear2 = time.time()
#claro.better_fit(elementi, chip)
#claro.better_fit_for_chips(chip)
claro.find_chips_threshold(110)
better2 = time.time()
#claro.sintesi_errori()

#print("Tempo fit lineare per "+str(elementi) +
#      " elementi: "+str(round(linear2-linear1,2)))
print("Tempo fit con funzione di errore per "+str(elementi) +
      " elementi: "+str(round(better2-linear2,2)))
