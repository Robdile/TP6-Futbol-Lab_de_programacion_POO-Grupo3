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
