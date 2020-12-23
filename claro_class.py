import subprocess
from matplotlib import pyplot as plt
import numpy as np
import numpy.ma as ma
from scipy import special
import math


class claro_class:

    def __init__(self):
        self.lista_diff_lineare = []
        self.lista_diff_err = []

    def find_files(self):
        # TODO aggiungere gestione delle eccezioni in caso non si abbia i permessi di exec
        subprocess.call("./analisi_file.sh")

    def linear_fit(self, how_many=20, how_many_chips=0):
        """
        Funzione per il fit lineare.
        Richiede un intero come parametro che indichi quanti file analizzare.
        Deafult: 20.
        """

        list_of_paths = self.read_pathfile(how_many, how_many_chips)

        for i in range(0, len(list_of_paths)):
            x, y, soglia_vera, num_chip = self.read_single_file(
                list_of_paths[i].strip())

            y_fit = np.array(y)
            y_fit = y_fit[y_fit > 1]
            y_fit = y_fit[y_fit < 999]

            mask_array = np.in1d(y, y_fit)
            # True solo i valori scelti per il fit
            mask_array = np.invert(mask_array)
            # Usando una maschera ricavo i valori x utili
            x_fit = ma.masked_array(x, mask=mask_array).compressed()

            plt.scatter(x, y, marker='o')
            plt.grid()
            plt.xscale('linear')
            plt.yscale('linear')

            coeff = np.polyfit(x_fit, y_fit, 1)
            x_plot = x_fit
            # Aggiunti due punti in più per allungare la retta
            x_plot = np.insert(x_plot, 0, x_fit[0]-2)
            x_plot = np.append(x_plot, x_fit[-1]+2)
            y_plot = x_plot*coeff[0] + coeff[1]

            x_soglia = (500 - coeff[1]) / coeff[0]

            plt.text(x[0], y_plot[-2], "Soglia calcolata: x="+str(round(x_soglia, 2))+"V\nSoglia vera: x=" +
                     str(round(soglia_vera, 2))+"V\nDifferenza: "+str(round(soglia_vera-x_soglia, 2))+"V", fontsize=8)

            self.lista_diff_lineare.append((soglia_vera-x_soglia)**2)
            plt.plot(x_plot, y_plot)
            plt.savefig("plot/fig"+str(i)+"_chip_"+str(num_chip)+".png")
            plt.close()

    def better_fit(self, how_many=20, how_many_chips=0):

        list_of_paths = self.read_pathfile(how_many, how_many_chips)

        for i in range(0, len(list_of_paths)):

            x, y, soglia_vera, num_chip = self.read_single_file(list_of_paths[i].strip())

            plt.scatter(x, y, marker='o')
            plt.grid()
            plt.xscale('linear')
            plt.yscale('linear')

            x = np.array(x)
            x_norm = [float(i) for i in x]  # Cast a float
            x_norm -= np.mean(x_norm)

            x_plot = np.linspace(x_norm[0], x_norm[-1], len(x_norm)*100)
            y_plot = (special.erf(x_plot)+1)*500  # Adattamento verticale
            x_plot += x[0]  # Adattamento orizzontale

            y_inutili = np.array(y)
            y_inutili = y_inutili[y_inutili < 50]
            index = len(y_inutili)  # Indice del primo elemento utile

            # Indice dell'elemento della funzione con stessa y
            extra_funct_index = np.argmin(abs(y_plot - y[index]))
            extra = abs(x[index]-(x_plot[extra_funct_index]))

            # Se ci sono due punti centrali, la curva è traslata in modo da essere
            # il più vicina possibile ad entrambi i punti
            if y[index+1] < 950:
                extra_funct_index2 = np.argmin(abs(y_plot - y[index+1]))
                extra2 = abs(x[index+1]-(x_plot[extra_funct_index2]))
                x_plot += ((extra+extra2)/2)  # Secondo adattamento orizzontale
            else:
                x_plot += extra  # Secondo adattamento orizzontale

            index_soglia = np.argmin(abs(y_plot-500))
            x_soglia = x_plot[index_soglia]

            plt.scatter(x_plot[index_soglia],
                        y_plot[index_soglia], marker='o', color="black")

            plt.plot(x_plot, y_plot)

            plt.text(x[0], y_plot[index_soglia], "Soglia calcolata: x="+str(round(x_soglia, 2))+"V\nSoglia vera: x=" +
                     str(round(soglia_vera, 2))+"V\nDifferenza: "+str(round(soglia_vera-x_soglia, 2))+"V", fontsize=8)

            self.lista_diff_err.append((soglia_vera-x_soglia)**2)
            plt.savefig("plot/better_fig"+str(i)+"_chip_"+str(num_chip)+".png")
            plt.close()

    def read_pathfile(self, how_many, how_many_chips):
        """
        Dati il numero di file o il numero di chip (ignorato se 0),
        restituisce una lista di stringhe corrispondenti ai path degli X file o X path chiesti.
        """

        try:
            file_path = open('file_path.txt', 'r')
        except:
            print("Errore nella lettura del file")

        list_of_paths = []

        # In caso l'utente specifichi un numero X di chip
        if how_many_chips != 0:
            set_of_chips = set()
            while True:
                pathfile = file_path.readline().strip()
                chip_string = pathfile.split("/")
                chip_string = chip_string[4].split("_")  # "Chip_001"
                chip_number = int(chip_string[1])
                set_of_chips.add(chip_number)

                if len(set_of_chips) == how_many_chips+1:
                    # Rimuove l'ultimo elemento (in più)
                    set_of_chips.remove(chip_number)
                    break

                # Aggiunge il path alla lista di path
                list_of_paths.append(pathfile)

        # In caso l'utente specifichi un numero X di file
        else:
            for _ in range(0, how_many):
                pathfile = file_path.readline().strip()
                list_of_paths.append(pathfile)

        file_path.close()

        return list_of_paths

    def read_single_file(self, path):
        """
        Dato il path di un file, restituisce una lista di x, una lista di y e il valore di soglia.
        """

        f = open(path, "r")

        x = []
        y = []

        chip_string = path.split("/")
        chip_string = chip_string[4].split("_")  # "Chip_001"
        num_chip = int(chip_string[1])

        line = f.readline()
        line = line.split()
        soglia_vera = float(line[1])
        line = f.readline()
        line = f.readline()

        while True:
            # Get next line from file
            line = f.readline()

            if not line:
                break

            values = line.split()
            x.append(int(values[0]))
            y.append(int(values[1]))

        f.close()
        return x, y, soglia_vera, num_chip

    def sintesi_errori(self):

        media_errori_lineare = np.mean(np.array(self.lista_diff_lineare))
        media_errori_lineare = math.sqrt(media_errori_lineare)
        media_errori_err_funct = np.mean(np.array(self.lista_diff_err))
        media_errori_err_funct = math.sqrt(media_errori_err_funct)

        print("\nIn media, la differenza tra le soglie 'vere' e quelle trovate con il fit lineare è: " +
              str(round(media_errori_lineare, 4)))
        print("In media, la differenza tra le soglie 'vere' e quelle trovate con il fit migliore è: " +
              str(round(media_errori_err_funct, 4))+"\n")
