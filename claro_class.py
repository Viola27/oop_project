import subprocess
from matplotlib import pyplot as plt
import numpy as np
import numpy.ma as ma
from scipy import special


class claro_class:

    def __init__(self):
        print("inizializzazione")

    # ATTENZIONE! Accertarsi che "analisi_file.sh" abbia i permessi di exec

    def find_files(self):
        # TODO aggiungere gestione delle eccezioni in caso non si abbia i permessi
        subprocess.call("./analisi_file.sh")

    def linear_fit(self, how_many=20):
        """
        Funzione per il fit lineare.
        Richiede un intero come parametro che indichi quanti file analizzare.
        Deafult: 20.
        """
        try:
            file_path = open('file_path.txt', 'r')
        except:
            print("Errore nella lettura del file")

        for i in range(0, how_many):
            f = open(file_path.readline().strip())

            x = []
            y = []

            # Le prime 3 righe sono di header
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

            plt.plot(x_plot, y_plot)
            plt.savefig("plot/fig"+str(i)+".png")
            plt.close()

        file_path.close()

    def better_fit(self, how_many=20):

        try:
            file_path = open('file_path.txt', 'r')
        except:
            print("Errore nella lettura del file")

        for i in range(0, how_many):
            f = open(file_path.readline().strip())

            x = []
            y = []

            # Le prime 3 righe sono di header
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
                x_plot += extra #Secondo adattamento orizzontale
            

            index_soglia = np.argmin(abs(y_plot-500))
            x_soglia = x_plot[index_soglia]

            plt.scatter(x_plot[index_soglia],
                        y_plot[index_soglia], marker='o', color="black")

            plt.plot(x_plot, y_plot)

            plt.text(x[0], y_plot[index_soglia], "Soglia calcolata: x="+str(round(x_soglia, 2))+"V\nSoglia vera: x=" +
                     str(round(soglia_vera, 2))+"V\nDifferenza: "+str(round(soglia_vera-x_soglia, 2))+"V", fontsize=8)

            plt.savefig("plot/better_fig"+str(i)+".png")
            plt.close()

        file_path.close()
