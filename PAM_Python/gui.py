import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
from imp_exp import ImpExp
from pam import PAM

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PAM")
        self.geometry("1020x500")

        self.modImpExp = ImpExp()
        self.modPam = PAM()

        self.init_components()

    def init_components(self):
        # Etiquetas
        tk.Label(self, text="Matriz de disimilitud:").place(x=50, y=50, width=150, height=30)
        tk.Label(self, text="Número de grupos:").place(x=50, y=100, width=150, height=30)
        tk.Label(self, text="Archivo de resultado:").place(x=50, y=150, width=150, height=30)
        tk.Label(self, text="Costo de la solución:").place(x=50, y=200, width=150, height=30)
        tk.Label(self, text="Hora inicial:").place(x=500, y=100, width=100, height=30)
        tk.Label(self, text="Hora final:").place(x=500, y=150, width=100, height=30)

        # Campos de texto
        self.txtFileName = tk.Entry(self)
        self.txtFileName.place(x=200, y=50, width=600, height=30)
        self.txtFileName.config(state='readonly')

        self.txtNClusters = tk.Entry(self)
        self.txtNClusters.place(x=200, y=100, width=100, height=30)

        self.txtFileResult = tk.Entry(self)
        self.txtFileResult.place(x=200, y=150, width=200, height=30)

        self.txtCostoSolucion = tk.Entry(self)
        self.txtCostoSolucion.place(x=200, y=200, width=200, height=30)

        self.txtInitTime = tk.Entry(self)
        self.txtInitTime.place(x=600, y=100, width=200, height=30)

        self.txtFinalTime = tk.Entry(self)
        self.txtFinalTime.place(x=600, y=150, width=200, height=30)

        # Botones
        self.cmdAbrir = tk.Button(self, text="Abrir", command=self.abrir_archivo)
        self.cmdAbrir.place(x=820, y=50, width=100, height=30)

        self.cmdClasificar = tk.Button(self, text="Clasificar", command=self.clasificar)
        self.cmdClasificar.place(x=820, y=100, width=100, height=30)

        self.cmdSalir = tk.Button(self, text="Salir", command=self.destroy)
        self.cmdSalir.place(x=820, y=150, width=100, height=30)

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.txtFileName.config(state='normal')
            self.txtFileName.delete(0, tk.END)
            self.txtFileName.insert(0, file_path)
            self.txtFileName.config(state='readonly')

    def clasificar(self):
        try:
            if not self.txtNClusters.get().strip():
                messagebox.showwarning("Advertencia", "Por favor, ingrese el número de clusters.")
                return

            if not self.txtFileName.get().strip():
                messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo.")
                return

            if not self.txtFileResult.get().strip():
                messagebox.showwarning("Advertencia", "Por favor, ingrese el nombre del archivo de resultado.")
                return

            # Importar la matriz de costos
            self.modImpExp.importMatrixCost(self.txtFileName.get())
            self.modPam.d = self.modImpExp.d
            self.modPam.nObjects = self.modImpExp.nObjects

            # Registrar hora inicial
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.txtInitTime.delete(0, tk.END)
            self.txtInitTime.insert(0, current_time)

            # Ejecutar el algoritmo PAM
            self.modPam.pam(int(self.txtNClusters.get()))
            self.txtCostoSolucion.delete(0, tk.END)
            self.txtCostoSolucion.insert(0, str(self.modPam.dCostoSolucion))

            # Registrar hora final
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.txtFinalTime.delete(0, tk.END)
            self.txtFinalTime.insert(0, current_time)

            # Guardar los resultados en un archivo
            self.send_clusters_to_file(self.txtFileResult.get())

        except ValueError:
            messagebox.showerror("Error", "Error: El número de clusters debe ser un valor entero.")
        except IOError as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def send_clusters_to_file(self, fileName):
        try:
            with open(fileName, 'w') as writer:
                writer.write(f"Costo de la solución encontrada: {self.modPam.dCostoSolucion:.2f}\n")

                for i in range(len(self.modPam.kClusters)):
                    writer.write(f"Cluster no {i + 1}: ")
                    for j in range(len(self.modPam.kClusters[i].items)):
                        obj_name = self.modImpExp.nameObjects[self.modPam.kClusters[i].items[j]]
                        writer.write(f"{obj_name}{('.' if j == len(self.modPam.kClusters[i].items) - 1 else ',')}")
                    writer.write("\n")
                writer.write("_________________________________________________________________")

        except IOError as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
