import tkinter as tk
from tkinter import LabelFrame, CENTER
from tkinter import messagebox
from tkinter import filedialog
from tkinter import StringVar
from tkinter import Label,Entry,Button, Text, Scrollbar, Listbox, END, Toplevel
from tkinter import W, E
from tkinter import ttk
import sqlite3
import query
import self

class VentanaPrincipal:
    db = "database/productos.db"


    def __init__(self,root):
        self.ventana = root
        self.ventana.title('APP Gestor de Productos')
        self.ventana.resizable(width=True, height=True)
        #self.ventana.wm_iconbitmap('recursos/mac-logo.png') Solo funciona en Windows
        frame = tk.LabelFrame(self.ventana, text= "Registrar un nuevo producto")
        frame.grid(row=0, column=0,columnspan=3)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")  # Etiqueta de texto ubicada
        self.etiqueta_nombre.grid(row=1, column=0)  # Posicionamiento a traves de grid
        # Entry Nombre (caja de texto que recibira el nombre)
        self.nombre = Entry(frame)  # Caja de texto (input de texto) ubicada en el frame
        self.nombre.focus()  # Para que el foco del raton vaya a este Entry al inicio
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")  # Etiqueta de texto ubicada
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio (caja de texto que recibira el precio)
        self.precio = Entry(frame)   #Caja de texto (input de texto) ubicada en el frame
        self.precio.grid(row=2, column=1)

        # Boton Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto",command= self.add_producto) #No le tengo q poner parectesis a la funcion add_producto.
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W + E)

        # Label para mensajes (errores o confirmación)
        self.mensaje = Label(frame, text="", fg="red")  # fg="red" para mensajes de error, lo puedes cambiar dinámicamente
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E, pady=5)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0 Esta q es la primera siempre se tiene q llamar 0 y no se puede renombrar.Es fija.
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1

        #Botones de Eliminar y Actualizar

        # Botones de Eliminar y Actualizar
        s = ttk.Style()
        s.configure("my.TButton", font=('Calibri', 14, 'bold'))

        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=5, column=0, sticky=W + E)

        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=5, column=1, sticky=W + E)




        self.get_productos()



    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con :  #self.db es la base de datos
            cursor = con.cursor()
            resultado = cursor.execute(consulta,parametros)
            con.commit()

        return resultado.fetchall()

    def get_productos(self):

        #Limpiamos la tabla antes de mostrar los nuevos registros
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)


        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        print(registros)
        for registro in registros:
            print(registro)
            self.tabla.insert("",0, text= registro[1],values = registro[2])

    def validacion_nombre(self):
        # Devuelve True si el campo nombre no está vacío
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def add_producto(self):
        # Validar nombre
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio y no puede estar vacío.'
            return

        # Validar precio
        if not self.validacion_precio():
            print("El precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un número válido mayor que 0.'
            return

        # Guardar en base de datos
        query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
        parametros = (self.nombre.get(), self.precio.get())
        self.db_consulta(query, parametros)
        print("Datos guardados")

        # Mensaje de éxito
        self.mensaje['text'] = f'Producto {self.nombre.get()} añadido con éxito.'

        # Limpiar campos del formulario
        self.nombre.delete(0, END)
        self.precio.delete(0, END)

        # Actualizar lista de productos
        self.get_productos()

    def del_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacío , quiero que vacies el mensaje asi no hay nada.

        # Comprobación de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0] #text posicion 0 me devuelve el nombre.
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = f'Producto {nombre} eliminado con éxito'
        self.get_productos()

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            VentanaEditarProducto(self, nombre, precio, self.mensaje)
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto para editar'
            return

class VentanaEditarProducto:
    def __init__(self, ventana_principal, nombre, precio, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1, column=1)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Calibri', 13)).grid(row=3, column=1)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        # Botón Actualizar Producto
        ttk.Style().configure('my.TButton', font=('Calibri', 14, 'bold'))
        ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=self.actualizar).grid(row=5, columnspan=2, sticky=W + E)


    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio

        if nuevo_nombre and nuevo_precio:
            query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje['text'] = f'El producto {self.nombre} ha sido actualizado con éxito'
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()


if __name__ == "__main__":
    root = tk.Tk()
    app =  VentanaPrincipal(root)
    root.mainloop() #tiene q ser la última línea del programa




