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
            x, y, soglia_vera, num_chip, _ = self.read_single_file(
                list_of_paths[i].strip())

            if x == 0 and y == 0 and num_chip == 0 and num_ch == 0:
                continue

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

            x, y, soglia_vera, num_chip, _ = self.read_single_file(
                list_of_paths[i].strip())

            if x == 0 and y == 0 and num_chip == 0 and num_ch == 0:
                continue

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
            plt.savefig("plot/better_fig"+str(i)+"_chip_"+str(num_chip)+".jpg")
            plt.close()

    def better_fit_for_chips(self, how_many_chips=5):
        list_of_paths = self.read_pathfile(0, how_many_chips)
        last_chip = 1
        colors = ['blue', 'yellow', 'darkred', 'magenta',
                  'orange', 'red', 'green', 'lightblue']

        for i in range(0, len(list_of_paths)):
            x, y, soglia_vera, num_chip, num_ch = self.read_single_file(
                list_of_paths[i].strip())

            # Se si inizia il plot di un nuovo chip, serve chiudere la figura vecchia
            if num_chip != last_chip:
                plt.yticks(np.arange(0, 1000, step=100))
                plt.grid()
                plt.legend()
                plt.savefig("plot/better_chip_"+str(last_chip)+".png")
                last_chip = num_chip
                plt.close()

            plt.scatter(x, y, marker='o', color=colors[num_ch])
            plt.xscale('linear')
            plt.yscale('linear')

            x = np.array(x)
            x_norm = [float(i) for i in x]  # Cast a float
            x_norm -= np.mean(x_norm)

            x_plot = np.linspace(x_norm[0], x_norm[-1], len(x_norm)*200)
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

            plt.plot(x_plot, y_plot,
                     color=colors[num_ch], label='Ch. '+str(num_ch))
            self.lista_diff_err.append((soglia_vera-x_soglia)**2)

        plt.yticks(np.arange(0, 1000, step=100))
        plt.grid()
        plt.legend()
        plt.savefig("plot/better_chip_"+str(last_chip)+".png")
        plt.close()

    def find_chips_threshold(self, how_many_chips=100):
        """
        Questa funzione trova il valore di soglia per ciascun canale di ciascun chip,
        li salva su file e li disegna in uno scatter plot.
        Non salva i grafici dei fit.
        Il parametro "how_many_chips" conta i chip da analizzare senza considerare le ripetizioni
        (se impostato a 259 non leggerà tutti i chip, ma solo i primi 259, anche se il successivo è il chip 1).
        NB: "how_many_chips" verrà convertito automaticamente al successivo multiplo di 9
        """

        list_of_paths = self.read_pathfile(0, how_many_chips)
        chips_values = {}
        how_many_chips += (9- how_many_chips % 9)

        for i in range(0, len(list_of_paths)):
            x, y, _, num_chip, num_ch = self.read_single_file(
                list_of_paths[i].strip())

            if x == 0 and y == 0 and num_chip == 0 and num_ch == 0:
                continue

            x = np.array(x)
            x_norm = [float(i) for i in x]  # Cast a float
            x_norm -= np.mean(x_norm)
            x_plot = np.linspace(x_norm[0], x_norm[-1], len(x_norm)*200)
            y_plot = (special.erf(x_plot)+1)*500  # Adattamento verticale
            x_plot += x[0]  # Adattamento orizzontale

            # Ricerca valore di soglia (per commenti più dettagliati
            # si rimanda alla funzione "better_fit()")
            y_inutili = np.array(y)
            y_inutili = y_inutili[y_inutili < 50]
            index = len(y_inutili)  # Indice del primo elemento utile
            extra_funct_index = np.argmin(abs(y_plot - y[index]))
            extra = abs(x[index]-(x_plot[extra_funct_index]))
            if y[index+1] < 950:
                extra_funct_index2 = np.argmin(abs(y_plot - y[index+1]))
                extra2 = abs(x[index+1]-(x_plot[extra_funct_index2]))
                x_plot += ((extra+extra2)/2)  # Secondo adattamento orizzontale
            else:
                x_plot += extra  # Secondo adattamento orizzontale
            index_soglia = np.argmin(abs(y_plot-500))
            x_soglia = x_plot[index_soglia]

            # Aggiunta del valore soglia al dizionario
            if num_chip*10+num_ch not in chips_values:
                chips_values[num_chip*10+num_ch] = [x_soglia]
            else:
                chips_values[num_chip*10+num_ch].append(x_soglia)

        self.draw_dict(chips_values, how_many_chips)

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
        chip_string = chip_string[6].split("_")  # "Chip_001"
        num_chip = int(chip_string[5].split(".")[0])
        num_ch = int(chip_string[1])

        line = f.readline()
        if line.startswith("error") or line.startswith("Non"):
            return 0, 0, 0, 0, 0

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
        return x, y, soglia_vera, num_chip, num_ch

    def draw_dict(self, d, how_many_to_draw):
        how_many_to_draw += 1
        how_many_graph = how_many_to_draw // 9
        resto = how_many_to_draw % 9

        if resto != 0:
            how_many_graph += 1

        for i in range(1, how_many_to_draw,9):
            fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(15,10))
            colors = ['blue', 'yellow', 'darkred', 'magenta',
                      'orange', 'red', 'green', 'lightblue']

            # Itera 9 volte, una per ogni chip in fig
            for num_chip in range(i, 9+i):
                
                g = ((num_chip-1) % 9)  # g è il numero del grafico che si sta disegnando
                
                for ch in range(0, 8):  # Itera 8 volte, una per ogni canale del chip
                    try:
                        x_plot = d[num_chip * 10 + ch]
                    except:
                        print("chip "+str(num_chip)+" vuoto")
                        ax[g // 3][g % 3].title.set_text("Chip "+str(num_chip)+" (missing data on some ch)")
                        break
                    y_plot = np.ones(len(x_plot))*500
                    
                    ax[g // 3][g % 3].scatter(x_plot, y_plot,
                                            label="Ch. "+str(ch), marker='o', color=colors[ch])
                    ax[g // 3][g % 3].title.set_text("Chip "+str(num_chip))

            fig.savefig("plot/soglie"+str(i)+".png")
            plt.close(fig)

    def sintesi_errori(self):

        media_errori_lineare = np.mean(np.array(self.lista_diff_lineare))
        media_errori_lineare = math.sqrt(media_errori_lineare)
        media_errori_err_funct = np.mean(np.array(self.lista_diff_err))
        media_errori_err_funct = math.sqrt(media_errori_err_funct)

        print("\nIn media, la differenza tra le soglie 'vere' e quelle trovate con il fit lineare è: " +
              str(round(media_errori_lineare, 4)))
        print("In media, la differenza tra le soglie 'vere' e quelle trovate con il fit migliore è: " +
              str(round(media_errori_err_funct, 4))+"\n")
