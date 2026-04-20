import customtkinter as ctk
from tkinter import messagebox
from clases import Arquero, JugadorCampo

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppFutbol(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Estadísticas - Grupo 3 UNSADA")
        self.geometry("900x600")
        
        self.equipo = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- PANEL IZQUIERDO: FORMULARIO ---
        self.frame_carga = ctk.CTkFrame(self, width=320)
        self.frame_carga.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.frame_carga, text="REGISTRO DE JUGADOR", font=("Arial", 18, "bold")).pack(pady=15)

     # ==========================================
        # ZONA DE ENTRADA DE DATOS (FORMULARIO)
        # ==========================================

        # --- APELLIDO ---
        # Etiqueta (Label): Usamos anchor="w" (West/Oeste) para que el texto quede alineado a la izquierda.
        ctk.CTkLabel(self.frame_carga, text="Apellido del Jugador:", font=("Arial", 12)).pack(anchor="w", padx=25)
        
        # Caja de texto (Entry): El fill="x" permite que la caja se expanda horizontalmente.
        self.ent_apellido = ctk.CTkEntry(self.frame_carga)
        # El pady=(0, 15) es un detalle de diseño: 0 píxeles de margen arriba y 15 abajo para separar prolijamente los campos.
        self.ent_apellido.pack(pady=(0, 15), padx=20, fill="x")

        # --- NÚMERO DE CAMISETA ---
        ctk.CTkLabel(self.frame_carga, text="Número de Camiseta:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_numero = ctk.CTkEntry(self.frame_carga)
        self.ent_numero.pack(pady=(0, 15), padx=20, fill="x")

        # --- MINUTOS JUGADOS ---
        ctk.CTkLabel(self.frame_carga, text="Minutos Jugados:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_minutos = ctk.CTkEntry(self.frame_carga)
        self.ent_minutos.pack(pady=(0, 15), padx=20, fill="x")

        # --- POSICIÓN EN CAMPO ---
        ctk.CTkLabel(self.frame_carga, text="Posición en Campo:", font=("Arial", 12)).pack(anchor="w", padx=25)
        
        # Menú Desplegable (OptionMenu): Decisión clave de interfaz.
        # En lugar de usar un Entry libre, restringimos las opciones para prevenir errores de tipeo.
        # Esto hace "match" perfecto con la constante POSICIONES_PERMITIDAS de la clase JugadorCampo de Eros.
        self.combo_posicion = ctk.CTkOptionMenu(
            self.frame_carga, 
            values=["ARQUERO", "DEFENSA", "MEDIOCAMPISTA", "DELANTERO"],
            command=self.cambiar_posicion # Evento: Dispara la función de bloqueo/desbloqueo de goles dinámicamente.
        )
        self.combo_posicion.pack(pady=(0, 15), padx=20, fill="x")   
        
         # Goles, solo jugadores de campo. Por eso inicialmente lo dejamos bloqueado (state="disabled").
        ctk.CTkLabel(self.frame_carga, text="Goles Marcados:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_goles = ctk.CTkEntry(self.frame_carga)  # Campo de entrada de texto para los goles.
        self.ent_goles.pack(pady=(0, 25), padx=20, fill="x")
        
        # El parámetro 'command' enlaza el clic del botón con el método self.guardar_datos.
        self.btn_guardar = ctk.CTkButton(self.frame_carga, text="GUARDAR JUGADOR", height=40, command=self.guardar_datos)
        self.btn_guardar.pack(pady=10, padx=20, fill="x")

        # --- PANEL DERECHO: CONSULTAS ---
        self.frame_lista = ctk.CTkFrame(self) # Frame contenedor para separar visualmente la lista del formulario
        self.frame_lista.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.frame_lista, text="PLANTEL ACTUAL", font=("Arial", 18, "bold")).pack(pady=15) # Título del panel de consultas
        
        self.txt_lista = ctk.CTkTextbox(self.frame_lista, font=("Courier New", 13))
        self.txt_lista.pack(pady=10, padx=20, fill="both", expand=True)

import customtkinter as ctk     
from tkinter import messagebox
from clases import Arquero, JugadorCampo

ctk.set_appearance_mode("dark")  #se establece el modo oscuro
ctk.set_default_color_theme("blue") #botones en Azul

class AppFutbol(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Estadísticas - Grupo 3 UNSADA")
        self.geometry("950x750")
        
        self.equipo = []

        # --- MENÚ PRINCIPAL CON PESTAÑAS ---
        self.menu_tabs = ctk.CTkTabview(self)       #creamos el panel
        self.menu_tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_carga = self.menu_tabs.add("Carga de Datos") #creamos la pestaña
        self.tab_consultas = self.menu_tabs.add("Consultas") #creamos la pestaña

        self.armar_pestana_carga()      #modula
        self.armar_pestana_consultas()

