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
