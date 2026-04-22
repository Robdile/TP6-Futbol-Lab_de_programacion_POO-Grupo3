import customtkinter as ctk # Importamos la librería de interfaz gráfica. "ctk" es un alias para su uso.
from tkinter import messagebox # De la librería base de tkinter, importamos el modulo de cuadros para diálogos.
from clases import Arquero, JugadorCampo # Importamos las plantillas desde el archivo "clases.py".

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppFutbol(ctk.CTk):
    def __init__(self):   #Inicializamos la clase padre (CTk)
        super().__init__()

        self.title("Sistema de Estadísticas - Grupo 3 UNSADA") #Configuramos la estetica
        self.geometry("950x750")
        
        self.equipo = []   #Estructura de datos principal para almacenar los jugadores 

        # --- MENÚ PRINCIPAL CON PESTAÑAS ---
        self.menu_tabs = ctk.CTkTabview(self)   #Contenedor de Pestañas para la interfaz
        self.menu_tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_carga = self.menu_tabs.add("Carga de Datos") #Se añaden las dos secciones principales
        self.tab_consultas = self.menu_tabs.add("Consultas")

        self.armar_pestana_carga()              # se llaman a metodos internos para imprimir las pestañas
        self.armar_pestana_consultas()
        
        # Estado inicial seguro 
        self.cambiar_posicion("ARQUERO")

    def armar_pestana_carga(self):
        # Contenedor principal de la pestaña
        marco = ctk.CTkFrame(self.tab_carga)
        marco.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(marco, text="REGISTRO DE JUGADOR", font=("Arial", 18, "bold")).pack(pady=15)

        # ==========================================
        # ZONA DE ENTRADA DE DATOS 
        # ==========================================

        # --- APELLIDO ---
        # Usamos anchor="w" (West/Oeste) para alinear a la izquierda y fill="x" para expandir la caja.
        ctk.CTkLabel(marco, text="Apellido del Jugador:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_apellido = ctk.CTkEntry(marco)
        self.ent_apellido.pack(pady=(0, 15), padx=20, fill="x") # 'fill="x"' hace que la caja de texto se estire horizontalmente

        # --- NÚMERO DE CAMISETA ---
        ctk.CTkLabel(marco, text="Número de Camiseta:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_numero = ctk.CTkEntry(marco)
        self.ent_numero.pack(pady=(0, 15), padx=20, fill="x")

        # --- MINUTOS JUGADOS ---
        ctk.CTkLabel(marco, text="Minutos Jugados:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_minutos = ctk.CTkEntry(marco)
        self.ent_minutos.pack(pady=(0, 15), padx=20, fill="x")

        # --- POSICIÓN EN CAMPO ---
        ctk.CTkLabel(marco, text="Posición en Campo:", font=("Arial", 12)).pack(anchor="w", padx=25)
        # En lugar de un Entry libre, restringimos las opciones para prevenir errores de tipeo.
        self.combo_posicion = ctk.CTkOptionMenu(
            marco, 
            values=["ARQUERO", "DEFENSA", "MEDIOCAMPISTA", "DELANTERO"],
            command=self.cambiar_posicion # Dispara la función de bloqueo de goles dinámicamente.
        )
        self.combo_posicion.pack(pady=(0, 15), padx=20, fill="x")

        # ==========================================
        # GOLES Y BOTÓN 
        # ==========================================
        ctk.CTkLabel(marco, text="Goles Marcados:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_goles = ctk.CTkEntry(marco)
        self.ent_goles.pack(pady=(0, 25), padx=20, fill="x")

        # Al hacer clic, se dispara el método 'guardar_datos' para procesar la info
        self.btn_guardar = ctk.CTkButton(marco, text="GUARDAR JUGADOR", height=40, command=self.guardar_datos)
        self.btn_guardar.pack(pady=10, padx=20, fill="x")

        # Validación UX en tiempo real 
        # '.bind("<FocusOut>", ...)' detecta cuando el usuario hace clic fuera de la caja de texto.
        # Esto permite validar si lo que escribió es correcto sin esperar a que presione "Guardar".
        self.ent_apellido.bind("<FocusOut>", self.validar_apellido_realtime)
        self.ent_numero.bind("<FocusOut>", self.validar_numero_realtime)
        self.ent_minutos.bind("<FocusOut>", self.validar_minutos_realtime)

    #SEGUNDA PESTAÑA DONDE SE FILTRAN LAS CONSULTAS

    def armar_pestana_consultas(self):
        # Panel de botones de consulta 
        frame_filtros = ctk.CTkFrame(self.tab_consultas, fg_color="transparent")
        frame_filtros.pack(pady=10, fill="x")

        # Botones de filtrado:
        # Usamos 'lambda' para que la función actualizar_lista no se ejecute sola al iniciar la app,
        # sino que espere a que el usuario haga clic enviando un parámetro específico.

        ctk.CTkButton(frame_filtros, text="Plantel Completo", command=lambda: self.actualizar_lista("TODOS")).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(frame_filtros, text="Solo Arqueros", command=lambda: self.actualizar_lista("ARQUEROS")).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(frame_filtros, text="Con Goles", command=lambda: self.actualizar_lista("GOLEADORES")).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(frame_filtros, text="Sin Goles", command=lambda: self.actualizar_lista("SIN_GOLES")).pack(side="left", padx=5, expand=True)
       
        # Caja de texto grande para mostrar la lista de jugadores procesada.
        # Usamos 'Courier New' porque es una fuente monoespaciada
        self.txt_lista = ctk.CTkTextbox(self.tab_consultas, font=("Courier New", 13))
        self.txt_lista.pack(pady=10, padx=10, fill="both", expand=True)

        # Bloqueamos la edición del texto para que el usuario no pueda borrar los resultados a mano.
        self.txt_lista.configure(state="disabled")

    def cambiar_posicion(self, seleccion):
        # Lógica visual para bloquear/desbloquear el campo de goles 
        if seleccion == "ARQUERO": # Si es arquero, bloquea la opcion de cargar goles.
            self.ent_goles.delete(0, 'end')
            self.ent_goles.configure(
                state="disabled", fg_color="gray30", placeholder_text="No aplica"
                )
        else:   # Si es jugador de campo, habiltia la carga de goles.
            self.ent_goles.configure(state="normal", fg_color=["#F9F9FA", "#343638"], placeholder_text="")

    # Función que limpia la interfaz después de guardar un jugador.
    def limpiar_formulario(self):
        # Vaciamos cajas y devolvemos el cursor al inicio 
        self.ent_apellido.delete(0, 'end')
        self.ent_numero.delete(0, 'end')
        self.ent_minutos.delete(0, 'end')
        self.ent_goles.delete(0, 'end')
        self.combo_posicion.set("ARQUERO")
        self.cambiar_posicion("ARQUERO")
        self.ent_apellido.focus()

    def guardar_datos(self):
        # Lógica central de instanciación y control de errores 
        # Usamos un bloque try-except para atrapar cualquier error y que la app no se cierre sola
        try:
            if not self.ent_apellido.get().strip() or not self.ent_numero.get().strip() or not self.ent_minutos.get().strip(): #elimina espacios en blanco innecesarios
                 raise ValueError("Debe completar apellido, número y minutos.")  # Si falta algo, 'lanzamos' un error manualmente

            ape = self.ent_apellido.get()
            num = int(self.ent_numero.get())
            minu = float(self.ent_minutos.get() or 0)
            pos = self.combo_posicion.get()

            # Evitamos duplicados de camiseta
            for jugador in self.equipo: # Itera sobre la lista del equipo para comparar el numero ingresado con los ya cargados.
                if jugador.numero_camiseta == num:
                    raise ValueError(f"La camiseta {num} ya la tiene {jugador.apellido}.")
            
            # Aplicación de Herencia
            if pos == "ARQUERO":
                nuevo_jugador = Arquero(ape, num, minu)
            else:
                goles_str = self.ent_goles.get().strip()
                goles = int(goles_str) if goles_str else 0
                nuevo_jugador = JugadorCampo(ape, num, pos, goles, minu)

            self.equipo.append(nuevo_jugador)
            self.actualizar_lista()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", f"Jugador {ape} guardado.")
            
        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")


    def actualizar_lista(self, filtro="TODOS"):
        # Motor de filtrado y visualización 
        self.txt_lista.configure(state="normal") 
        self.txt_lista.delete("1.0", "end")
        
        if not self.equipo:
            self.txt_lista.insert("end", "Sin jugadores cargados.\n")
            self.txt_lista.configure(state="disabled")
            return

        for j in self.equipo:
            # LÓGICA DE FILTRADO
            if filtro == "ARQUEROS" and not isinstance(j, Arquero): continue
            
            if filtro == "GOLEADORES" and (not hasattr(j, 'goles') or j.goles == 0): continue
            
            # --- NUEVA LÓGICA: JUGADORES SIN GOLES ---
            # Si tocamos "Sin Goles", validamos si tiene la capacidad y si metió más de cero.
            if filtro == "SIN_GOLES" and hasattr(j, 'goles') and j.goles > 0: continue

            # Armamos el renglón. ljust y zfill simulan una grilla prolija tipo Excel.
            info = f"• {j.apellido.ljust(12)} | Cam: {str(j.numero_camiseta).zfill(2)} | Min: {str(j.minutos_jugados).rjust(3)} | Pos: {j.posicion.ljust(12)}"
            
            # Solo mostramos goles si no es arquero
            if hasattr(j, 'goles'):
                info += f" | Goles: {j.goles}"
                
            self.txt_lista.insert("end", info + "\n")
            
        self.txt_lista.configure(state="disabled") 

    # ==========================================
    # VALIDACIONES EN TIEMPO REAL 
    # ==========================================
    # Estas funciones capturan el evento <FocusOut> de Tkinter.

    def validar_apellido_realtime(self, event):
        texto = self.ent_apellido.get().strip()
        # any() busca letra por letra. Si encuentra un número, frena el ingreso.
        if texto and any(char.isdigit() for char in texto):
            messagebox.showwarning("Error", "El apellido no lleva números.")
            self.ent_apellido.delete(0, 'end')
            self.after(10, self.ent_apellido.focus)

    def validar_numero_realtime(self, event):
        texto = self.ent_numero.get().strip()
        # isdigit() asegura que absolutamente todo lo ingresado sean números.
        if texto and not texto.isdigit():
            messagebox.showwarning("Error", "La camiseta solo lleva números.")
            self.ent_numero.delete(0, 'end')
            self.after(10, self.ent_numero.focus)

    def validar_minutos_realtime(self, event):
        texto = self.ent_minutos.get().strip()
        if texto:
            try: 
                # Intentamos convertir a float (permite decimales como 45.5)
                valor = float(texto)
                # Los minutos no deben deben ser < 0.
                if valor < 0:
                    messagebox.showwarning("Error", "Los minutos no pueden ser negativos.")
                    # Se limpia el campo para corregir el error.
                    self.ent_minutos.delete(0, 'end')
                    self.after(10, self.ent_minutos.focus) 
                    # Usamos return para que no siga ejecutando código extra.
                    return
            except ValueError: 
                messagebox.showwarning("Error", "Los minutos deben ser numéricos.")
                self.ent_minutos.delete(0, 'end')
                self.after(10, self.ent_minutos.focus)

if __name__ == "__main__":
    app = AppFutbol()
    app.mainloop()
