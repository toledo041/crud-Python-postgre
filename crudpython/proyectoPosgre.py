import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkcalendar import DateEntry  # instalar este módulo usando pip install tkcalendar
import psycopg2

class EditProfileDialog:
    def __init__(self, parent, user_id, config_postgresql,action):
        self.parent = parent
        self.user_id = user_id
        self.config_postgresql = config_postgresql
        self.dialog = tk.Toplevel(parent)
        self.action = action
        
        if action == 0:
            self.dialog.title("New user")
        else:
            self.dialog.title("Edit user")
        

        self.label_username = tk.Label(self.dialog, text="User:")
        self.entry_username = tk.Entry(self.dialog) #, state="enabled"

        self.label_email = tk.Label(self.dialog, text="Email:")
        self.entry_email = tk.Entry(self.dialog) #, state="enabled"

        self.label_password = tk.Label(self.dialog, text="Password:")
        self.entry_password = tk.Entry(self.dialog, show="*")

        self.label_confirm_password = tk.Label(self.dialog, text="Confirm your password:")
        self.entry_confirm_password = tk.Entry(self.dialog, show="*")
        
        if action == 0:
            self.btn_update = tk.Button(self.dialog, text="Save", command=self.update_profile)
        else:
            self.btn_update = tk.Button(self.dialog, text="Update", command=self.update_profile)

        self.label_username.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.entry_username.grid(row=0, column=1, pady=10, padx=10)
        self.label_email.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.entry_email.grid(row=1, column=1, pady=10, padx=10)
        self.label_password.grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.entry_password.grid(row=2, column=1, pady=10, padx=10)
        self.label_confirm_password.grid(row=3, column=0, pady=10, padx=10, sticky="e")
        self.entry_confirm_password.grid(row=3, column=1, pady=10, padx=10)
        self.btn_update.grid(row=4, column=0, columnspan=2, pady=10)

        self.load_user_profile()
        # Centrar la ventana principal
        #self.center_window()

    def load_user_profile(self):
        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Consultar la base de datos para obtener la información del usuario
            cursor.execute("SELECT * FROM \"User\" WHERE \"idUser\" = %s", (self.user_id,))
            user = cursor.fetchone()

            if user:
                # Cargar la información en los campos
                self.entry_username.config(state="normal")
                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, user[1])
                self.entry_username.config(state="disabled")

                self.entry_email.config(state="normal")
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, user[2])
                self.entry_email.config(state="disabled")

        except psycopg2.Error as e:
            messagebox.showerror("Error de PostgreSQL", f"Error: {e}")

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def update_profile(self):
        # Obtener valores de los campos de entrada
        new_user = self.entry_username.get()
        new_email = self.entry_email.get()
        new_password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()
        id_user = 0
        
        # Verificar que todos los campos estén completos
        if not new_user.strip() or not new_email.strip() or not new_password.strip() or not confirm_password.strip(): #
            messagebox.showwarning("Info", "Please, type all the fields.")
            return
        
        # Verificar que las contraseñas sean iguales
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords don't match.")
            return
        
        if self.action == 0 :
            #nuevo usuario
            try:
                # Conectar a PostgreSQL
                connection = psycopg2.connect(**self.config_postgresql)
                cursor = connection.cursor()

                # Insertar nuevo elemento
                cursor.execute('''
                    INSERT INTO "User" ("name", "password", "email") 
                    VALUES (%s, %s, %s)
                ''', (new_user, new_password, new_email))

                # Confirmar la transacción
                connection.commit()

                # Cerrar la conexión
                connection.close()
                
                messagebox.showerror("Info", "Successful registration")
                # Cerrar el formulario de registro
                self.dialog.destroy()

            except psycopg2.Error as e:
                print("Error de PostgreSQL:", e)

            finally:
                # Cerrar la conexión
                if connection:
                    connection.close()
        else:
            
            try:
                # Conectar a PostgreSQL
                connection = psycopg2.connect(**self.config_postgresql)
                cursor = connection.cursor()

                # Consultar la base de datos para verificar las credenciales
                cursor.execute("SELECT \"idUser\" FROM \"User\" WHERE \"name\" = %s", (new_user,))
                user = cursor.fetchone()

                if user:
                    #Se obtiene el id del usuario con el username proporcionado
                    id_user = user[0]                                        
                else:
                    messagebox.showerror("Error", "User not exist.")

            except psycopg2.Error as e:
                messagebox.showerror("Error de PostgreSQL", f"Error: {e}")

            finally:
                # Cerrar la conexión
                if connection:
                    connection.close()
            try:
                # Conectar a PostgreSQL
                connection = psycopg2.connect(**self.config_postgresql)
                cursor = connection.cursor() 

                # Actualizar la contraseña en la base de datos
                cursor.execute("UPDATE \"User\" SET \"password\" = %s, \"email\" = %s WHERE \"idUser\" = %s", (new_password,new_email ,id_user))
                connection.commit()

                # Mostrar mensaje de éxito
                messagebox.showinfo("Info", "Profile updated successfully.")

                # Cerrar la ventana emergente
                self.dialog.destroy()

            except psycopg2.Error as e:
                messagebox.showerror("Error de PostgreSQL", f"Error: {e}")

            finally:
                # Cerrar la conexión
                if connection:
                    connection.close()
                
    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la posición de la ventana
        self.root.geometry(f"+{x}+{y}")
class UserProfile:
    def __init__(self, parent, user_id, config_postgresql):
        self.parent = parent
        self.user_id = user_id
        self.config_postgresql = config_postgresql
        self.parent.title("Perfil de Usuario")

        self.label_name = tk.Label(parent, text="User:")
        self.entry_name = tk.Entry(parent, state="disabled")

        self.label_email = tk.Label(parent, text="Email:")
        self.entry_email = tk.Entry(parent, state="disabled")

        self.label_password = tk.Label(parent, text="Password:")
        self.entry_password = tk.Entry(parent, show="*", state="disabled")

        self.btn_edit = tk.Button(parent, text="Edit", command=self.edit_profile)

        self.label_name.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.entry_name.grid(row=0, column=1, pady=10, padx=10)
        self.label_email.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.entry_email.grid(row=1, column=1, pady=10, padx=10)
        self.label_password.grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.entry_password.grid(row=2, column=1, pady=10, padx=10)
        self.btn_edit.grid(row=3, column=0, columnspan=2, pady=10)

        self.load_user_profile()
        # Centrar la ventana principal
        self.center_window()

    def load_user_profile(self):
        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Consultar la base de datos para obtener la información del usuario
            cursor.execute("SELECT * FROM \"User\" WHERE \"idUser\" = %s", (self.user_id,))
            user = cursor.fetchone()

            if user:
                # Cargar la información en los campos
                self.entry_name.config(state="normal")
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, user[1])
                self.entry_name.config(state="disabled")

                self.entry_email.config(state="normal")
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, user[2])
                self.entry_email.config(state="disabled")

                self.entry_password.config(state="normal")
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, user[3])
                self.entry_password.config(state="disabled")

        except psycopg2.Error as e:
            messagebox.showerror("Error de PostgreSQL", f"Error: {e}")

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def edit_profile(self):
        # Pedir una nueva contraseña al usuario
        new_password = simpledialog.askstring("Edit profile", "Type your new password:", show='*')

        if new_password is not None and new_password.strip():  # Verifica si la nueva contraseña no está vacía
            try:
                # Conectar a PostgreSQL
                connection = psycopg2.connect(**self.config_postgresql)
                cursor = connection.cursor()

                # Actualizar la contraseña en la base de datos
                cursor.execute("UPDATE \"User\" SET password = %s WHERE \"idUser\" = %s", (new_password, self.user_id))
                connection.commit()

                # Actualizar la información en la pantalla
                self.entry_password.config(state="normal")
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, new_password)
                self.entry_password.config(state="disabled")

                messagebox.showinfo("Info", "Successfully updated profile")

            except psycopg2.Error as e:
                messagebox.showerror("Error de PostgreSQL", f"Error: {e}")

            finally:
                # Cerrar la conexión
                if connection:
                    connection.close()
        else:
            messagebox.showwarning("Info", "The new password can't be empty.")
            
    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la posición de la ventana
        self.root.geometry(f"+{x}+{y}")

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        # Configura el evento de cierre de la ventana principal
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.label_name = tk.Label(root, text="User:")
        self.entry_name = tk.Entry(root)

        #self.label_email = tk.Label(root, text="Correo electrónico:")
        #self.entry_email = tk.Entry(root)

        self.label_password = tk.Label(root, text="Password:")
        self.entry_password = tk.Entry(root, show="*")

        self.btn_login = tk.Button(root, text="Login", command=self.login)
        self.btn_register = tk.Button(root, text="Register", command=self.register)
        self.btn_edit_profile = tk.Button(root, text="Edit password", command=self.edit_profile)
        

        self.label_name.pack(pady=10)
        self.entry_name.pack(pady=10)
        #self.label_email.pack(pady=10)
        #self.entry_email.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.btn_login.pack(pady=10)
        self.btn_register.pack(pady=10)
        self.btn_edit_profile.pack(pady=10)

        # Configuración de conexión a PostgreSQL
        self.config_postgresql = {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': '123456789',
            'database': 'Vinculation'
        }
        # Centrar la ventana principal
        self.center_window()

    def login(self):
        # Obtener valores de los campos de entrada
        username = self.entry_name.get()
        password = self.entry_password.get()
        # Verificar que todos los campos estén completos
        if not username.strip()  or not password.strip(): #or not email.strip()
            messagebox.showwarning("Advertencia", "Please, type name and password.")
            return
        
        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Consultar la base de datos para verificar las credenciales
            cursor.execute("SELECT * FROM \"User\" WHERE \"name\" = %s AND \"password\" = %s", (username, password))
            user = cursor.fetchone()

            if user:
                # Abrir la pantalla del perfil del usuario
                profile_root = tk.Toplevel(self.root)
                profile_root.title("Perfil de Usuario")
                #UserProfile(profile_root, user[0], self.config_postgresql)
                InterfazGrafica(profile_root, user[0], self.config_postgresql, self)
                self.entry_name.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                self.root.withdraw()  # Ocultar la pantalla de inicio de sesión

            else:
                messagebox.showerror("Error", "Incorrect credentials")

        except psycopg2.Error as e:
            messagebox.showerror("Error de PostgreSQL", f"Error: {e}")

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def register(self):
        # Obtener valores de los campos de entrada
        #username = self.entry_name.get()
        #email = "" #self.entry_email.get()
        #password = self.entry_password.get()  

        edit_dialog = EditProfileDialog(self.root, 0 , self.config_postgresql, 0)        

        # Verificar que todos los campos estén completos
        
    def edit_profile(self):
        # Obtener valores de los campos de entrada
        username = self.entry_name.get()
        password = self.entry_password.get()

        edit_dialog = EditProfileDialog(self.root, 0, self.config_postgresql,1)
        
                
    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la posición de la ventana
        self.root.geometry(f"+{x}+{y}")
        
    def on_close(self):        
        # Cierra la ventana principal y termina la aplicación
        self.root.destroy()
        
    def show_login_screen(self):
        # Muestra la ventana de inicio de sesión
        self.root.deiconify()

class InterfazGrafica:
    def __init__(self, root,user_id, config_postgresql, login_screen):
        self.root = root
        self.root.title("Query and register en PostgreSQL")
        self.user_id = user_id        
        self.login_screen = login_screen

        # Configuración de conexión a PostgreSQL
        self.config_postgresql = config_postgresql
        #{
        #    'host': 'localhost',
        #    'port': "5432",
        #    'user': 'postgres',
        #    'password': '123456',
        #    'database': 'Vinculation'
        #}
        
        # Configura el evento de cierre de la ventana principal
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Crear un Treeview para mostrar la tabla
        self.tree = ttk.Treeview(self.root, columns=("ID", "Date", "Workplace", "Id student", "Student"), show="headings")

        # Configurar encabezados de columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Workplace", text="Workplace")
        self.tree.heading("Id student", text="Id student")        
        self.tree.heading("Student", text="Student")

        # Configurar columnas
        self.tree.column("ID", anchor=tk.W, width=50)
        self.tree.column("Date", anchor=tk.W, width=100)
        self.tree.column("Workplace", anchor=tk.W, width=100)
        self.tree.column("Id student", anchor=tk.W, width=100)        
        self.tree.column("Student", anchor=tk.W, width=200)

        # Enlazar clic en la columna para mostrar opciones
        self.tree.bind("<ButtonRelease-1>", self.mostrar_opciones)

        # Obtener datos de la base de datos y llenar la tabla
        self.obtener_datos()

        # Mostrar el Treeview
        self.tree.pack()

        # Botón para registrar un nuevo elemento
        self.btn_registrar = tk.Button(self.root, text="Register new element", command=self.mostrar_formulario_registro)
        self.btn_registrar.pack()

        # Centrar la ventana principal
        self.center_window()

    def obtener_datos(self):
        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Ejecutar la consulta SQL adaptada 
            cursor.execute('''
                SELECT "IdCompanyStudent", to_char("date", 'YYYY-MM-DD') as "date", "workplace", "CompanyStudent"."idStudent", 
                "Student"."name"||' '||"Student"."lastName"||' '||"Student"."mothersthestName" AS studentName
                FROM "CompanyStudent"
                INNER JOIN "Student" ON "CompanyStudent"."idStudent" = "Student"."idStudent" where "CompanyStudent"."status" = true
                ORDER BY "IdCompanyStudent"
            ''')
            resultados = cursor.fetchall()

            # Limpiar la tabla antes de agregar nuevos registros
            for _ in self.tree.get_children():
                self.tree.delete(_)

            # Llenar la tabla con los resultados
            for row in resultados:
                self.tree.insert("", "end", values=row)

        except psycopg2.Error as e:
            print("Error de PostgreSQL:", e)

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def mostrar_opciones(self, event):
        # Obtener el item seleccionado
        item = self.tree.selection()[0]

        # Obtener la información del elemento seleccionado
        elemento = self.tree.item(item, "values")

        # Crear y mostrar el formulario de opciones
        ActualizaElementoForm(self.root, self.config_postgresql, elemento, self.obtener_datos, self.user_id)

    def mostrar_formulario_registro(self):
        # Crear y mostrar el formulario de registro
        RegistroElementoForm(self.root, self.config_postgresql, self.obtener_datos, self.user_id)

    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la posición de la ventana
        self.root.geometry(f"+{x}+{y}")
        
    def on_close(self):
        # Oculta la ventana actual
        self.root.withdraw()
        
        # Muestra la ventana de inicio de sesión
        self.login_screen.show_login_screen()

class RegistroElementoForm(tk.Toplevel):
    def __init__(self, parent, config_postgresql, callback_actualizacion,user_id):
        super().__init__(parent)
        self.title("Registro de Nuevo Elemento")
        self.config_postgresql = config_postgresql
        self.callback_actualizacion = callback_actualizacion
        self.user_id = user_id

        # Campos de entrada para el nuevo elemento
        self.lbl_fecha = tk.Label(self, text="Fecha:")
        self.entry_fecha = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2,date_pattern='YYYY-MM-DD')
        self.lbl_lugar = tk.Label(self, text="Lugar:")
        self.entry_lugar = tk.Entry(self)
        self.lbl_id_estudiante = tk.Label(self, text="Estudiante:")
        self.combo_id_estudiante = ttk.Combobox(self, state="readonly")
        #self.lbl_estado = tk.Label(self, text="Estado:")
        #self.entry_estado = tk.Entry(self)

        # Botón para realizar el registro
        self.btn_registrar = tk.Button(self, text="Registrar", command=self.registrar_elemento)

        # Organizar widgets
        self.lbl_fecha.pack()
        self.entry_fecha.pack()
        self.lbl_lugar.pack()
        self.entry_lugar.pack()
        self.lbl_id_estudiante.pack()
        self.combo_id_estudiante.pack()
        #self.lbl_estado.pack()
        #self.entry_estado.pack()
        self.btn_registrar.pack()

        # Obtener y cargar los nombres de estudiantes en el combo box
        self.cargar_nombres_estudiantes()

        # Centrar la ventana
        self.center_window()

    def cargar_nombres_estudiantes(self):
        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Obtener los nombres de estudiantes
            cursor.execute("SELECT \"idStudent\", \"name\" || ' ' || \"lastName\" || ' ' || \"mothersthestName\" nombre FROM public.\"Student\" ORDER BY \"idStudent\" ASC")
            
            
            resultados = cursor.fetchall()

            # Cargar los nombres en el combo box
            nombres_estudiantes = [f"{id_estudiante} - {nombre}" for id_estudiante, nombre in resultados]
            self.combo_id_estudiante["values"] = nombres_estudiantes

        except psycopg2.Error as e:
            print("Error de PostgreSQL:", e)

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def registrar_elemento(self):
        # Obtener valores de los campos de entrada
        fecha = self.entry_fecha.get()
        lugar = self.entry_lugar.get()
        id_estudiante = self.combo_id_estudiante.get().split(" - ")[0]
        estado = '1' #self.entry_estado.get()
        id_user = self.user_id

        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Insertar nuevo elemento
            cursor.execute('''
                INSERT INTO "CompanyStudent" ("date", "workplace", "idStudent", "status","idUserCreate","dateCreate") 
                VALUES (%s, %s, %s, %s,%s,NOW())
            ''', (fecha, lugar, id_estudiante, estado,id_user))

            # Confirmar la transacción
            connection.commit()

            # Cerrar la conexión
            connection.close()

            # Llamar al callback para actualizar la tabla principal
            self.callback_actualizacion()

            # Cerrar el formulario de registro
            self.destroy()

        except psycopg2.Error as e:
            print("Error de PostgreSQL:", e)

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la posición de la ventana
        self.geometry(f"+{x}+{y}")

class ActualizaElementoForm(tk.Toplevel):
    def __init__(self, parent, config_postgresql, elemento, callback_actualizacion,user_id):
        super().__init__(parent)
        self.title("Update or delete element")
        self.config_postgresql = config_postgresql
        self.elemento = elemento
        self.callback_actualizacion = callback_actualizacion
        self.user_id = user_id

        # Campos de entrada para el elemento seleccionado
        self.lbl_fecha = tk.Label(self, text="Fecha:")
        self.entry_fecha = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2,date_pattern='YYYY-MM-DD')
        self.lbl_lugar = tk.Label(self, text="Lugar:")
        self.entry_lugar = tk.Entry(self)
        self.lbl_id_estudiante = tk.Label(self, text="Estudiante:")
        self.combo_id_estudiante = ttk.Combobox(self, state="readonly")
        #self.lbl_estado = tk.Label(self, text="Estado:")
        #self.entry_estado = tk.Entry(self)

        # Botones para actualizar o eliminar
        self.btn_actualizar = tk.Button(self, text="Actualizar", command=self.actualizar_elemento)
        self.btn_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_elemento)

        # Organizar widgets
        self.lbl_fecha.grid(row=0, column=0, sticky="e")
        self.entry_fecha.grid(row=0, column=1)
        self.lbl_lugar.grid(row=1, column=0, sticky="e")
        self.entry_lugar.grid(row=1, column=1)
        self.lbl_id_estudiante.grid(row=2, column=0, sticky="e")
        self.combo_id_estudiante.grid(row=2, column=1)
        #self.lbl_estado.grid(row=3, column=0, sticky="e")
        #self.entry_estado.grid(row=3, column=1)
        self.btn_actualizar.grid(row=4, column=0, pady=10)
        self.btn_eliminar.grid(row=4, column=1, pady=10)

        # Llenar campos con la información del elemento
        print("fecha:", elemento[1])
        self.entry_fecha.set_date(elemento[1])
        self.entry_lugar.insert(0, elemento[2])
        #self.entry_estado.insert(0, elemento[4])

        # Obtener y cargar los nombres de estudiantes en el combo box
        self.cargar_nombres_estudiantes()

        # Establecer la selección actual en el combo box
        id_estudiante_seleccionado = elemento[3]
        self.combo_id_estudiante.set(f"{id_estudiante_seleccionado} - {self.obtener_nombre_estudiante(id_estudiante_seleccionado)}")
        
        # Centrar la ventana
        self.center_window()

    def cargar_nombres_estudiantes(self):
        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Obtener los nombres de estudiantes
            cursor.execute("SELECT \"idStudent\", \"name\" || ' ' || \"lastName\" || ' ' || \"mothersthestName\" FROM \"Student\"")
            resultados = cursor.fetchall()

            # Cargar los nombres en el combo box
            nombres_estudiantes = [f"{id_estudiante} - {nombre}" for id_estudiante, nombre in resultados]
            self.combo_id_estudiante["values"] = nombres_estudiantes

        except psycopg2.Error as e:
            print("Error de PostgreSQL:", e)

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def obtener_nombre_estudiante(self, id_estudiante):
        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Obtener el nombre del estudiante
            cursor.execute("SELECT \"name\" || ' ' || \"lastName\" || ' ' || \"mothersthestName\" FROM \"Student\" WHERE \"idStudent\" = %s", (id_estudiante,))
            nombre = cursor.fetchone()[0]

            return nombre

        except psycopg2.Error as e:
            print("Error de PostgreSQL:", e)
            return ""

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def actualizar_elemento(self):
        # Obtener valores de los campos de entrada
        nueva_fecha = self.entry_fecha.get()
        nuevo_lugar = self.entry_lugar.get()
        nuevo_id_estudiante = self.combo_id_estudiante.get().split(" - ")[0]
        user_id = self.user_id
        #nuevo_estado = self.entry_estado.get()

        try:
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.config_postgresql)
            cursor = connection.cursor()

            # Ejecutar la actualización en la base de datos
            cursor.execute('''
                UPDATE "CompanyStudent" SET "date"=%s, "workplace"=%s, "idStudent"=%s, "idUserModified"=%s, "dateModified" = NOW() 
                WHERE "IdCompanyStudent"=%s
            ''', (nueva_fecha, nuevo_lugar, nuevo_id_estudiante, user_id,self.elemento[0]))

            # Confirmar la transacción
            connection.commit()

            # Cerrar la conexión
            connection.close()

            # Llamar al callback para actualizar la tabla principal
            self.callback_actualizacion()

            # Cerrar el formulario
            self.destroy()

        except psycopg2.Error as e:
            print("Error de PostgreSQL:", e)

        finally:
            # Cerrar la conexión
            if connection:
                connection.close()

    def eliminar_elemento(self):
        # Mostrar un cuadro de diálogo de confirmación
        confirmacion = askyesno("Confirmar Eliminación", "¿Estás seguro de eliminar este elemento?")

        if confirmacion:
            try:
                # Conectar a PostgreSQL
                connection = psycopg2.connect(**self.config_postgresql)
                cursor = connection.cursor()

                # Ejecutar la eliminación en la base de datos
                cursor.execute('''
                    UPDATE "CompanyStudent" SET "status" = false  WHERE "IdCompanyStudent"=%s
                ''', (self.elemento[0],))

                # Confirmar la transacción
                connection.commit()

                # Cerrar la conexión
                connection.close()

                # Llamar al callback para actualizar la tabla principal
                self.callback_actualizacion()

                # Cerrar el formulario
                self.destroy()

            except psycopg2.Error as e:
                print("Error de PostgreSQL:", e)

            finally:
                # Cerrar la conexión
                if connection:
                    connection.close()

    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la posición de la ventana
        self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
