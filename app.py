import tkinter as tk
from tkinter import LabelFrame, CENTER
from tkinter import messagebox
from tkinter import filedialog
from tkinter import StringVar
from tkinter import Label,Entry,Button, Text, Scrollbar, Listbox, END, Toplevel
from tkinter import W, E
from tkinter import ttk
import sqlite3
import ttkbootstrap as ttk1
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import query


class VentanaPrincipal:
    db = "database/productos.db"


    def __init__(self,root):

        self.icon_guardar = ImageTk.PhotoImage(Image.open("img/save.png").resize((20, 20)))
        self.icon_editar = ImageTk.PhotoImage(Image.open("img/edit.png").resize((20, 20)))
        self.icon_eliminar = ImageTk.PhotoImage(Image.open("img/delete.png").resize((20, 20)))

        self.ventana = root
        self.ventana.title('Almacen de productos')
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

        # Label Cantidad
        self.etiqueta_cantidad = Label(frame, text="Cantidad: ")
        self.etiqueta_cantidad.grid(row=3, column=0)
        self.cantidad = tk.Spinbox(frame, from_=1, to=100, width=5)
        self.cantidad.grid(row=3, column=1)

        #Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ")
        self.etiqueta_categoria.grid(row=4, column=0)
        self.categoria_var = StringVar()
        # Combobox para seleccionar la categoría del producto
        self.categoria = ttk.Combobox(frame, values=["Alimentos","Salud","Tecnologia"], state="readonly", textvariable=self.categoria_var)
        self.categoria.grid(row=4, column=1)




        # Boton Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", image=self.icon_guardar, compound="left", command=self.add_producto)#No le tengo q poner parectesis a la funcion add_producto.
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E,pady=(5, 0))

        # Label para mensajes (errores o confirmación)
        self.mensaje = Label(frame, text="", fg="red")  # fg="red" para mensajes de error, lo puedes cambiar dinámicamente
        self.mensaje.grid(row=6, column=0, columnspan=2, sticky=W + E, pady=(0, 5))

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Helvetica', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Helvetica', 13, 'bold'))  # Se
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Separador visual entre formulario y tabla
        separator = ttk.Separator(self.ventana, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
        # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=("precio", "cantidad", "precio_total","categoria"), style="mystyle.Treeview")
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla.heading("precio", text="Precio Unitario", anchor=CENTER)
        self.tabla.heading("cantidad", text="Cantidad", anchor=CENTER)
        self.tabla.heading("precio_total", text="Precio Total", anchor=CENTER)
        self.tabla.heading("categoria", text="Categoria", anchor=CENTER)
        self.tabla.column("precio", anchor=CENTER)
        self.tabla.column("cantidad", anchor=CENTER)
        self.tabla.column("precio_total", anchor=CENTER)
        self.tabla.column("categoria", anchor=CENTER)
        # Encabezado 1
        self.tabla.grid(row=8, column=0, columnspan=2)

        #Botones de Eliminar y Actualizar

        # Botones de Eliminar y Actualizar
        s = ttk.Style()
        s.configure("my.TButton", font=('Helvetica', 14, 'bold'))

        self.boton_eliminar = ttk.Button(text='ELIMINAR', image=self.icon_eliminar, compound="left", command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=5, column=0, sticky=W + E)

        self.boton_editar = ttk.Button(text='EDITAR', image=self.icon_editar, compound="left", command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=5, column=1, sticky=W + E)

        self.add_tooltip(self.boton_aniadir, "Guardar un nuevo producto en la base de datos")
        self.add_tooltip(self.boton_eliminar, "Eliminar el producto seleccionado")
        self.add_tooltip(self.boton_editar, "Editar el producto seleccionado")



        self.get_productos()

    def add_tooltip(self, widget, text):
        def on_enter(event):
            widget.tooltip = tk.Toplevel()
            widget.tooltip.overrideredirect(True)
            widget.tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = tk.Label(widget.tooltip, text=text, bg="lightyellow", relief="solid", borderwidth=1,
                             font=("Helvetica", 10))
            label.pack()

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)


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
            producto_id = registro[0]
            nombre = registro[1]
            precio = float(registro[2])
            cantidad = int(registro[3])
            precio_total = round(precio * cantidad, 2)
            categoria = registro[4]
            self.tabla.insert("", "end", text=nombre, values=(precio, cantidad, precio_total,categoria))

    def validacion_nombre(self):
        # Devuelve True si el campo nombre no está vacío
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def validacion_cantidad(self):
        try:
            cantidad = int(self.cantidad.get())
            return cantidad >= 0
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

        if not self.validacion_cantidad():
            print("La cantidad es obligatoria")
            self.mensaje['text'] = 'La cantidad es obligatoria y debe ser un número entero mayor o igual a 0.'
            return

        # Guardar en base de datos
        query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?,?)'
        parametros = (self.nombre.get(), self.precio.get(),self.cantidad.get(),self.categoria_var.get())
        self.db_consulta(query, parametros)
        print("Datos guardados")

        # Mensaje de éxito
        self.mensaje['text'] = f'Producto {self.nombre.get()} añadido con éxito.'

        # Limpiar campos del formulario
        self.nombre.delete(0, END)
        self.precio.delete(0, END)
        self.cantidad.delete(0, END)

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
            seleccion = self.tabla.selection()
            if not seleccion:
                self.mensaje['text'] = 'Por favor, seleccione un producto para editar'
                return

            item = self.tabla.item(seleccion[0])
            nombre = item['text']
            precio = item['values'][0]
            cantidad = item['values'][1]
            categoria = item['values'][3]  # Obtiene la categoría del producto seleccionado
            # Obtiene el precio del producto seleccionado

            VentanaEditarProducto(self,None, nombre,precio,cantidad,categoria,self.mensaje)
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto para editar'
            return



class VentanaEditarProducto:
    def __init__(self, ventana_principal, producto_id, nombre, precio,cantidad,categoria, mensaje):
        self.ventana_principal = ventana_principal
        self.producto_id = producto_id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Helvetica', 13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
              state='readonly', font=('Helvetica', 13),
              readonlybackground="gray20", fg="white").grid(row=1, column=1)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Helvetica', 13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Helvetica', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Helvetica', 13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio),
              state='readonly', font=('Helvetica', 13),
              readonlybackground="gray20", fg="white").grid(row=3, column=1)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Helvetica', 13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Helvetica', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        # Cantidad antigua (solo lectura)
        Label(frame_ep, text="Cantidad antigua: ", font=('Helvetica', 13)).grid(row=5, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=cantidad),
              state='readonly', font=('Helvetica', 13),
              readonlybackground="gray20", fg="white").grid(row=5, column=1)

        # Cantidad nueva
        Label(frame_ep, text="Cantidad nueva: ", font=('Helvetica', 13)).grid(row=6, column=0)
        self.input_cantidad_nueva = Entry(frame_ep, font=('Helvetica', 13))
        self.input_cantidad_nueva.grid(row=6, column=1)

        # Categoría antigua (solo lectura)
        Label(frame_ep, text="Categoría antigua: ", font=('Helvetica', 13)).grid(row=7, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=self.categoria),
              state='readonly', font=('Helvetica', 13),
              readonlybackground="gray20", fg="white").grid(row=7, column=1)

        # Categoría nueva
        Label(frame_ep, text="Categoría nueva: ", font=('Helvetica', 13)).grid(row=8, column=0)
        self.input_categoria_nueva = ttk.Combobox(frame_ep, values=["Alimentos", "Salud", "Tecnologia"], state="readonly", font=('Helvetica', 13))
        self.input_categoria_nueva.grid(row=8, column=1)



        # Botón Actualizar Producto
        ttk.Style().configure('my.TButton', font=('Helvetica', 14, 'bold'))
        ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=self.actualizar).grid(row=9, columnspan=2, sticky=W + E)


    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        nuevo_cantidad = self.input_cantidad_nueva.get() or self.cantidad
        nueva_categoria = self.input_categoria_nueva.get() or self.categoria

        if nuevo_nombre and nuevo_precio:
            query = 'UPDATE producto SET nombre = ?, precio = ? , cantidad = ?, categoria = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio,nuevo_cantidad, nueva_categoria, self.nombre)  # id_producto debe ser definido, por ejemplo, obteniendo el ID del producto seleccionado
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje['text'] = f'El producto {self.nombre} ha sido actualizado con éxito'
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()




if __name__ == "__main__":
    root = ttk1.Window(themename="superhero")  # Puedes cambiar el tema a tu preferencia
    app =  VentanaPrincipal(root)
    root.mainloop() #tiene q ser la última línea del programa
    




