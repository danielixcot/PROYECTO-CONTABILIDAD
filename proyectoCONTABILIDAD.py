import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario - El Niño")
        self.root.geometry("900x400")

        # Inicializar el código inicial
        self.codigo_inicial = 202301
        self.codigo_actual = self.codigo_inicial

        # Etiquetas
        self.etiqueta_titulo = tk.Label(self.root, text="Sistema de Inventario", font=("Arial", 16))
        self.etiqueta_titulo.grid(row=0, column=1, pady=10)

        # Campos de Entrada
        self.etiqueta_nombre = tk.Label(self.root, text="Nombre")
        self.etiqueta_nombre.grid(row=1, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5)

        self.etiqueta_descripcion = tk.Label(self.root, text="Descripción")
        self.etiqueta_descripcion.grid(row=2, column=0, padx=10, pady=5)
        self.entry_descripcion = tk.Entry(self.root)
        self.entry_descripcion.grid(row=2, column=1, padx=10, pady=5)

        self.etiqueta_talla = tk.Label(self.root, text="Talla")
        self.etiqueta_talla.grid(row=3, column=0, padx=10, pady=5)
        self.entry_talla = tk.Entry(self.root)
        self.entry_talla.grid(row=3, column=1, padx=10, pady=5)

        self.etiqueta_cantidad = tk.Label(self.root, text="Cantidad")
        self.etiqueta_cantidad.grid(row=4, column=0, padx=10, pady=5)
        self.entry_cantidad = tk.Entry(self.root)
        self.entry_cantidad.grid(row=4, column=1, padx=10, pady=5)

        self.etiqueta_precio = tk.Label(self.root, text="Precio del Producto")
        self.etiqueta_precio.grid(row=5, column=0, padx=10, pady=5)
        self.entry_precio = tk.Entry(self.root)
        self.entry_precio.grid(row=5, column=1, padx=10, pady=5)

        # Botones de Acción
        self.boton_agregar_producto = tk.Button(self.root, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar_producto.grid(row=6, column=0, columnspan=2, pady=10)

        self.boton_editar_producto = tk.Button(self.root, text="Editar Producto", command=self.editar_producto)
        self.boton_editar_producto.grid(row=6, column=2, padx=10, pady=10)

        self.boton_guardar_datos = tk.Button(self.root, text="Guardar Datos", command=self.guardar_datos)
        self.boton_guardar_datos.grid(row=6, column=3, padx=10, pady=10)

        self.boton_mostrar_resumen = tk.Button(self.root, text="Mostrar Resumen", command=self.mostrar_resumen)
        self.boton_mostrar_resumen.grid(row=6, column=4, padx=10, pady=10)

        # Crear una tabla para mostrar los productos
        self.tabla_inventario = ttk.Treeview(self.root, columns=("Código", "Nombre", "Descripción", "Talla", "Cantidad", "Precio"), show="headings")
        self.tabla_inventario.grid(row=7, column=0, columnspan=6, padx=10, pady=10)

        # Definir las columnas de la tabla
        self.tabla_inventario.heading("Código", text="Código de Producto")
        self.tabla_inventario.heading("Nombre", text="Nombre")
        self.tabla_inventario.heading("Descripción", text="Descripción")
        self.tabla_inventario.heading("Talla", text="Talla")
        self.tabla_inventario.heading("Cantidad", text="Cantidad")
        self.tabla_inventario.heading("Precio", text="Precio")

        # Ajustar el tamaño de las columnas
        self.tabla_inventario.column("Código", width=100, anchor="center")
        self.tabla_inventario.column("Nombre", width=200, anchor="center")
        self.tabla_inventario.column("Descripción", width=200, anchor="center")
        self.tabla_inventario.column("Talla", width=100, anchor="center")
        self.tabla_inventario.column("Cantidad", width=100, anchor="center")
        self.tabla_inventario.column("Precio", width=100, anchor="center")

        # Evento de selección de una fila en la tabla
        self.tabla_inventario.bind("<ButtonRelease-1>", self.seleccionar_producto)

        # Variable para almacenar el código de producto seleccionado
        self.producto_seleccionado = None

    def generar_codigo(self):
        # Genera el código automáticamente
        codigo_producto = self.codigo_actual
        self.codigo_actual += 1  # Incrementar para el siguiente producto
        return codigo_producto

    def agregar_producto(self):
        # Obtener los datos ingresados
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()

        talla = self.entry_talla.get()

        try:
            cantidad = int(self.entry_cantidad.get())  # Asegurarse que la cantidad sea un número
        except ValueError:
            messagebox.showerror("Error", "La Cantidad debe ser un número.")
            return

        try:
            precio = float(self.entry_precio.get())  # Asegurarse que el precio sea un número flotante
        except ValueError:
            messagebox.showerror("Error", "El Precio del Producto debe ser un número.")
            return

        # Verificar que todos los campos estén llenos
        if nombre and descripcion and talla:
            # Generar el código automáticamente
            codigo_producto = self.generar_codigo()

            # Insertar los datos en la tabla
            self.tabla_inventario.insert("", "end", values=(codigo_producto, nombre, descripcion, talla, cantidad, precio))

            # Limpiar los campos después de agregar el producto
            self.entry_nombre.delete(0, tk.END)
            self.entry_descripcion.delete(0, tk.END)
            self.entry_talla.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Por favor ingresa todos los datos del producto")

    def editar_producto(self):
        if self.producto_seleccionado:
            # Obtener los datos de los campos
            nombre = self.entry_nombre.get()
            descripcion = self.entry_descripcion.get()
            talla = self.entry_talla.get()

            try:
                cantidad = int(self.entry_cantidad.get())  # Asegurarse que la cantidad sea un número
            except ValueError:
                messagebox.showerror("Error", "La Cantidad debe ser un número.")
                return

            try:
                precio = float(self.entry_precio.get())  # Asegurarse que el precio sea un número flotante
            except ValueError:
                messagebox.showerror("Error", "El Precio del Producto debe ser un número.")
                return

            # Verificar que todos los campos estén llenos
            if nombre and descripcion and talla:
                # Obtener el código del producto seleccionado
                codigo = self.tabla_inventario.item(self.producto_seleccionado)["values"][0]

                # Actualizar los valores en la tabla
                self.tabla_inventario.item(self.producto_seleccionado, values=(codigo, nombre, descripcion, talla, cantidad, precio))

                # Limpiar los campos después de editar el producto
                self.entry_nombre.delete(0, tk.END)
                self.entry_descripcion.delete(0, tk.END)
                self.entry_talla.delete(0, tk.END)
                self.entry_cantidad.delete(0, tk.END)
                self.entry_precio.delete(0, tk.END)

                # Desmarcar el producto seleccionado
                self.producto_seleccionado = None
            else:
                messagebox.showerror("Error", "Por favor ingresa todos los datos del producto")
        else:
            messagebox.showerror("Error", "Selecciona un producto para editar")

    def seleccionar_producto(self, event):
        # Obtener el producto seleccionado de la tabla
        item = self.tabla_inventario.selection()
        if item:
            self.producto_seleccionado = item[0]

            # Obtener los valores del producto seleccionado
            valores = self.tabla_inventario.item(self.producto_seleccionado)["values"]

            # Cargar los valores en los campos de entrada para editar
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])

            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[2])

            self.entry_talla.delete(0, tk.END)
            self.entry_talla.insert(0, valores[3])

            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, valores[4])

            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, valores[5])

    def guardar_datos(self):
        # Obtener todos los productos de la tabla
        productos = []
        for row in self.tabla_inventario.get_children():
            values = self.tabla_inventario.item(row, "values")
            producto = {
                "codigo": values[0],
                "nombre": values[1],
                "descripcion": values[2],
                "talla": values[3],
                "cantidad": values[4],
                "precio": values[5]
            }
            productos.append(producto)

        # Guardar los datos en un archivo JSON
        try:
            with open("productos.json", "w") as archivo:
                json.dump(productos, archivo, indent=4)
            messagebox.showinfo("Éxito", "Datos guardados exitosamente en productos.json")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

    def mostrar_resumen(self):
        # Crear una nueva ventana para mostrar el resumen
        resumen_ventana = tk.Toplevel(self.root)
        resumen_ventana.title("Resumen de Productos")
        resumen_ventana.geometry("800x400")

        # Crear una tabla para mostrar el resumen
        tabla_resumen = ttk.Treeview(resumen_ventana, columns=("Código", "Nombre", "Descripción", "Talla", "Cantidad", "Precio"), show="headings")
        tabla_resumen.pack(expand=True, fill="both")

        # Definir las columnas de la tabla
        tabla_resumen.heading("Código", text="Código de Producto")
        tabla_resumen.heading("Nombre", text="Nombre")
        tabla_resumen.heading("Descripción", text="Descripción")
        tabla_resumen.heading("Talla", text="Talla")
        tabla_resumen.heading("Cantidad", text="Cantidad")
        tabla_resumen.heading("Precio", text="Precio")

        # Ajustar el tamaño de las columnas
        tabla_resumen.column("Código", width=100, anchor="center")
        tabla_resumen.column("Nombre", width=200, anchor="center")
        tabla_resumen.column("Descripción", width=200, anchor="center")
        tabla_resumen.column("Talla", width=100, anchor="center")
        tabla_resumen.column("Cantidad", width=100, anchor="center")
        tabla_resumen.column("Precio", width=100, anchor="center")

        # Obtener los productos de la tabla principal
        for row in self.tabla_inventario.get_children():
            values = self.tabla_inventario.item(row, "values")
            tabla_resumen.insert("", "end", values=values)

# Crear la ventana principal de la aplicación
root = tk.Tk()
app = InventarioApp(root)
root.mainloop()
