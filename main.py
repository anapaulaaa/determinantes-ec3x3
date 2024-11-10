import numpy as np
import tkinter as tk
from tkinter import messagebox


def calcular_inversa(matriz):
    if len(matriz) != len(matriz[0]):
        return "La matriz no es cuadrada, no tiene inversa."
    determinante = np.linalg.det(matriz)
    if determinante == 0:
        return "La matriz es singular, no tiene inversa."
    inversa = np.linalg.inv(matriz)
    return np.round(inversa, 2)


def calcular_determinante(matriz):
    if len(matriz) != len(matriz[0]):
        return "La matriz no es cuadrada, no tiene determinante."
    determinante = np.linalg.det(matriz)
    return round(determinante, 2)


def calcular_transpuesta(matriz):
    return np.transpose(matriz)


# Función para mostrar resultados
def mostrar_resultado(resultado, tipo, text_widget):
    text_widget.delete(1.0, tk.END)  # Limpiar resultados anteriores
    if isinstance(resultado, str):
        text_widget.insert(tk.END, resultado)
    else:
        text_widget.insert(tk.END, f"{tipo}:\n{resultado}")


# Función para manejar la operación seleccionada
def realizar_operacion(opcion, entry_matrix1, filas, columnas, resultado_text):
    try:
        matriz1 = []

        for i in range(filas):
            fila1 = []
            for j in range(columnas):
                valor1 = float(entry_matrix1[i][j].get())
                fila1.append(valor1)
            matriz1.append(fila1)

        matriz1 = np.array(matriz1)

        if opcion == "inversa":
            resultado = calcular_inversa(matriz1)
            mostrar_resultado(resultado, "Inversa", resultado_text)
        elif opcion == "determinante":
            resultado = calcular_determinante(matriz1)
            mostrar_resultado(resultado, "Determinante", resultado_text)
        elif opcion == "transpuesta":
            resultado = calcular_transpuesta(matriz1)
            resultado = np.round(resultado, 2)  # Redondear transpuesta
            mostrar_resultado(resultado, "Transpuesta", resultado_text)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese solo números válidos.")


# Función para resolver ecuaciones 3x3 usando el método de Cramer
def resolver_ecuaciones(matriz_coeficientes, vector_resultados):
    determinante = np.linalg.det(matriz_coeficientes)
    if determinante == 0:
        return "El sistema de ecuaciones no tiene solución única."

    x1 = np.linalg.det(
        np.column_stack((vector_resultados, matriz_coeficientes[:, 1], matriz_coeficientes[:, 2]))) / determinante
    x2 = np.linalg.det(
        np.column_stack((matriz_coeficientes[:, 0], vector_resultados, matriz_coeficientes[:, 2]))) / determinante
    x3 = np.linalg.det(
        np.column_stack((matriz_coeficientes[:, 0], matriz_coeficientes[:, 1], vector_resultados))) / determinante
    return (round(x1, 2), round(x2, 2), round(x3, 2))


# Crear ventana para resolver ecuaciones 3x3
def crear_ventana_ecuaciones():
    ventana_ecuaciones = tk.Toplevel(root)
    ventana_ecuaciones.title("Resolver Ecuaciones 3x3 (Método de Cramer)")
    ventana_ecuaciones.configure(bg="#e6e6fa")  # Color de fondo lavanda

    # Frame para entradas
    frame_ecuaciones = tk.Frame(ventana_ecuaciones)
    frame_ecuaciones.pack(pady=10)

    # Entradas para las 3x3
    tk.Label(frame_ecuaciones, text="Ecuaciones 3x3:", bg="#e6e6fa").grid(row=0, column=0, columnspan=5)

    # Entradas de coeficientes y resultados
    entries = []
    for i in range(3):
        fila_entries = []
        for j in range(3):
            entry = tk.Entry(frame_ecuaciones, width=5)
            entry.grid(row=i + 1, column=j)
            fila_entries.append(entry)

        # Añadir el signo igual en la columna 3
        tk.Label(frame_ecuaciones, text="=", bg="#e6e6fa").grid(row=i + 1, column=3)

        resultado_entry = tk.Entry(frame_ecuaciones, width=5)
        resultado_entry.grid(row=i + 1, column=4)
        fila_entries.append(resultado_entry)
        entries.append(fila_entries)

    resultado_ecuaciones_text = tk.Text(ventana_ecuaciones, height=5, width=50)
    resultado_ecuaciones_text.pack(pady=10)

    # Botón para resolver
    def resolver():
        try:
            matriz_coeficientes = []
            vector_resultados = []

            for fila in entries:
                coeficientes = [float(fila[j].get()) for j in range(3)]
                resultado = float(fila[3].get())
                matriz_coeficientes.append(coeficientes)
                vector_resultados.append(resultado)

            matriz_coeficientes = np.array(matriz_coeficientes)
            vector_resultados = np.array(vector_resultados)

            resultado = resolver_ecuaciones(matriz_coeficientes, vector_resultados)
            mostrar_resultado(resultado, "Soluciones", resultado_ecuaciones_text)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese solo números válidos.")

    tk.Button(ventana_ecuaciones, text="Resolver", command=resolver).pack()


# Crear la ventana de determinantes
def crear_ventana_matriz():
    ventana_matriz = tk.Toplevel(root)
    ventana_matriz.title("Operaciones con Determinantes")
    ventana_matriz.configure(bg="#d6f5d6")  # Color de fondo verde más suave

    # Entradas para dimensiones de la matriz
    tk.Label(ventana_matriz, text="Filas:", bg="#d6f5d6").grid(row=0, column=0)
    entry_filas = tk.Entry(ventana_matriz, width=5)
    entry_filas.grid(row=0, column=1)

    tk.Label(ventana_matriz, text="Columnas:", bg="#d6f5d6").grid(row=0, column=2)
    entry_columnas = tk.Entry(ventana_matriz, width=5)
    entry_columnas.grid(row=0, column=3)

    # Frame para las entradas de la matriz
    frame_matriz1 = tk.Frame(ventana_matriz)
    frame_matriz1.grid(row=1, column=0, columnspan=4, pady=10)

    def crear_entradas():
        try:
            filas = int(entry_filas.get())
            columnas = int(entry_columnas.get())

            # Limpiar entradas anteriores
            for widget in frame_matriz1.winfo_children():
                widget.destroy()

            # Crear nuevas entradas
            global entry_matrix1
            entry_matrix1 = []
            tk.Label(frame_matriz1, text="Matriz 1", bg="#d6f5d6").grid(row=0, column=0, columnspan=columnas)
            for i in range(filas):
                fila_entries1 = []
                for j in range(columnas):
                    entry1 = tk.Entry(frame_matriz1, width=5)
                    entry1.grid(row=i + 1, column=j)
                    fila_entries1.append(entry1)

                entry_matrix1.append(fila_entries1)

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese números válidos para filas y columnas.")

    # Botón para crear entradas de matriz
    tk.Button(ventana_matriz, text="Crear Entradas", command=crear_entradas).grid(row=0, column=4)

    # Frame para resultados
    resultado_text = tk.Text(ventana_matriz, height=10, width=50)
    resultado_text.grid(row=3, column=0, columnspan=4, pady=10)

    # Botones para operaciones
    tk.Button(ventana_matriz, text="Calcular Inversa",
              command=lambda: realizar_operacion("inversa", entry_matrix1, int(entry_filas.get()),
                                                 int(entry_columnas.get()), resultado_text)).grid(row=2, column=0,
                                                                                                  padx=5)
    tk.Button(ventana_matriz, text="Calcular Determinante",
              command=lambda: realizar_operacion("determinante", entry_matrix1, int(entry_filas.get()),
                                                 int(entry_columnas.get()), resultado_text)).grid(row=2, column=1,
                                                                                                  padx=5)
    tk.Button(ventana_matriz, text="Calcular Transpuesta",
              command=lambda: realizar_operacion("transpuesta", entry_matrix1, int(entry_filas.get()),
                                                 int(entry_columnas.get()), resultado_text)).grid(row=2, column=2,
                                                                                                  padx=5)


# Crear la ventana principal
root = tk.Tk()
root.title("Menú Principal")
root.configure(bg="#add8e6")  # Color de fondo azul claro

# Título
tk.Label(root, text="Menú Operaciones Álgebra Lineal", bg="#add8e6", font=("Arial", 16)).pack(pady=10)

# Botones para abrir las ventanas de operaciones
tk.Button(root, text="Operaciones con Determinantes", command=crear_ventana_matriz).pack(pady=5)
tk.Button(root, text="Resolver Ecuaciones 3x3", command=crear_ventana_ecuaciones).pack(pady=5)

root.mainloop()
