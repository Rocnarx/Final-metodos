import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import random

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Calculadora de Matrices")
        self.root.geometry("500x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")
        
        #ESTILOS TTK
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TLabel", font=("Arial", 12, "bold"), background="#2C3E50", foreground="white")
        ttk.Label(root, text="Ingrese las matrices (separadas por comas y ';')", font=("Arial", 12), background="#2C3E50", foreground="white").pack(pady=10)

        # Entrada Matriz A
        ttk.Label(root, text="Matriz A:").pack()
        self.entry_matrix1 = tk.Text(root, height=4, width=40, font=("Arial", 12))
        self.entry_matrix1.pack(pady=5)

        swap_button = ttk.Button(root, text="↔", width=3, command=self.intercambiar_matrices)
        swap_button.pack(pady=5)

        # Entrada Matriz B
        ttk.Label(root, text="Matriz B:").pack()
        self.entry_matrix2 = tk.Text(root, height=4, width=40, font=("Arial", 12))
        self.entry_matrix2.pack(pady=5)

        # Opciones para tamaño de la matriz
        ttk.Label(root, text="Tamaño de la matriz (filas x columnas):").pack()
        self.rows_var = tk.IntVar(value=3)
        self.cols_var = tk.IntVar(value=3)
        row_col_frame = ttk.Frame(root)
        row_col_frame.pack(pady=5)
        ttk.Spinbox(row_col_frame, from_=1, to=10, textvariable=self.rows_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(row_col_frame, from_=1, to=10, textvariable=self.cols_var, width=5).pack(side=tk.LEFT, padx=5)

        # Opciones para el rango de numeros aleatorios
        ttk.Label(root, text="Rango de números aleatorios:").pack()
        self.min_var = tk.IntVar(value=-10)
        self.max_var = tk.IntVar(value=10)
        range_frame = ttk.Frame(root)
        range_frame.pack(pady=5)
        ttk.Entry(range_frame, textvariable=self.min_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(range_frame, text="a").pack(side=tk.LEFT)
        ttk.Entry(range_frame, textvariable=self.max_var, width=5).pack(side=tk.LEFT, padx=5)

        ttk.Button(root, text="Generar Matrices", command=self.generar_matrices).pack(pady=10)

        ttk.Label(root, text="Resultado:").pack()
        self.result_text = tk.Text(root, height=4, width=40, font=("Arial", 12), state='disabled', bg="#D5DBDB")
        self.result_text.pack(pady=5)

        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        operations = [
            ("Suma A + B", self.sumar),
            ("Resta A - B", self.restar),
            ("Multiplicación A x B", self.multiplicar),
            ("Inversa de A", self.inversa_A),
            ("Inversa de B", self.inversa_B),
            ("Determinante de A", self.determinante_A),
            ("Determinante de B", self.determinante_B)
        ]

        for i, (text, command) in enumerate(operations):
            ttk.Button(self.button_frame, text=text, command=command, width=20).grid(row=i//2, column=i%2, padx=10, pady=5)

    def get_matrix(self, text_widget):
        """Convierte el texto en una matriz de NumPy"""
        try:
            raw_text = text_widget.get("1.0", tk.END).strip()
            rows = raw_text.split(";")
            matrix = [list(map(float, row.split(","))) for row in rows]
            return np.array(matrix)
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto.\nUse comas para separar elementos y ';' para filas.")
            return None

    def display_result(self, matrix):
        """Muestra el resultado en el cuadro de texto"""
        self.result_text.config(state='normal')
        self.result_text.delete("1.0", tk.END)
        if isinstance(matrix, np.ndarray):
            result_str = "\n".join([", ".join(map(str, row)) for row in matrix])
        else:
            result_str = str(matrix)
        self.result_text.insert(tk.END, result_str)
        self.result_text.config(state='disabled')

    def generar_matrices(self):
        """Genera matrices aleatorias con el tamaño y rango especificados"""
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        min_val = self.min_var.get()
        max_val = self.max_var.get()

        if min_val >= max_val:
            messagebox.showerror("Error", "El valor minimo debe ser menor que el máximo.")
            return

        matriz_A = np.random.randint(min_val, max_val+1, (rows, cols))
        matriz_B = np.random.randint(min_val, max_val+1, (rows, cols))

        matriz_A_str = ";".join([",".join(map(str, row)) for row in matriz_A])
        matriz_B_str = ";".join([",".join(map(str, row)) for row in matriz_B])

        self.entry_matrix1.delete("1.0", tk.END)
        self.entry_matrix1.insert(tk.END, matriz_A_str)
        
        self.entry_matrix2.delete("1.0", tk.END)
        self.entry_matrix2.insert(tk.END, matriz_B_str)

    def sumar(self):
        A = self.get_matrix(self.entry_matrix1)
        B = self.get_matrix(self.entry_matrix2)
        if A is not None and B is not None and A.shape == B.shape:
            self.display_result(A + B)
        else:
            messagebox.showerror("Error", "Las matrices deben tener el mismo tamaño.")

    def restar(self):
        A = self.get_matrix(self.entry_matrix1)
        B = self.get_matrix(self.entry_matrix2)
        if A is not None and B is not None and A.shape == B.shape:
            self.display_result(A - B)
        else:
            messagebox.showerror("⚠️ Error", "Las matrices deben tener el mismo tamaño.")

    def multiplicar(self):
        A = self.get_matrix(self.entry_matrix1)
        B = self.get_matrix(self.entry_matrix2)
        if A is not None and B is not None and A.shape[1] == B.shape[0]:
            self.display_result(np.dot(A, B))
        else:
            messagebox.showerror("Error", "El número de columnas de A debe coincidir con las filas de B.")

    def inversa_A(self):
        A = self.get_matrix(self.entry_matrix1)
        if A is not None and A.shape[0] == A.shape[1]:
            try:
                inv_A = np.linalg.inv(A)
                inv_A = np.round(inv_A, 2) 
                self.display_result(inv_A)
            except np.linalg.LinAlgError:
                messagebox.showerror("Error", "La matriz A no es invertible.")

    def inversa_B(self):
        B = self.get_matrix(self.entry_matrix2)
        if B is not None and B.shape[0] == B.shape[1]:
            try:
                inv_B = np.linalg.inv(B)
                inv_B = np.round(inv_B, 2) 
                self.display_result(inv_B)
            except np.linalg.LinAlgError:
                messagebox.showerror("Error", "La matriz B no es invertible.")


    def determinante_A(self):
        A = self.get_matrix(self.entry_matrix1)
        if A is not None and A.shape[0] == A.shape[1]:
            det_A = np.linalg.det(A)  
            self.display_result(round(det_A, 2)) 

    def determinante_B(self):
        B = self.get_matrix(self.entry_matrix2)
        if B is not None and B.shape[0] == B.shape[1]:
            det_B = np.linalg.det(B)
            self.display_result(round(det_B, 2)) 

    def intercambiar_matrices(self):
        """Intercambia los valores de Matriz A y Matriz B"""
        matriz_A_text = self.entry_matrix1.get("1.0", tk.END).strip()
        matriz_B_text = self.entry_matrix2.get("1.0", tk.END).strip()

        self.entry_matrix1.delete("1.0", tk.END)
        self.entry_matrix1.insert(tk.END, matriz_B_text)

        self.entry_matrix2.delete("1.0", tk.END)
        self.entry_matrix2.insert(tk.END, matriz_A_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculator(root)
    root.mainloop()
