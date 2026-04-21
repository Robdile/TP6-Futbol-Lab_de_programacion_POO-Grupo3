import customtkinter as ctk
from tkinter import messagebox
from clases import Arquero, JugadorCampo

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppFutbol(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Estadísticas - Grupo 3 UNSADA")
        self.geometry("950x750")
        
        self.equipo = []

        # --- MENÚ PRINCIPAL CON PESTAÑAS ---
        self.menu_tabs = ctk.CTkTabview(self)
        self.menu_tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_carga = self.menu_tabs.add("Carga de Datos")
        self.tab_consultas = self.menu_tabs.add("Consultas")

        self.armar_pestana_carga()
        self.armar_pestana_consultas()
        
        # Estado inicial seguro
        self.cambiar_posicion("ARQUERO")

    def armar_pestana_carga(self):
        marco = ctk.CTkFrame(self.tab_carga)
        marco.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(marco, text="REGISTRO DE JUGADOR", font=("Arial", 18, "bold")).pack(pady=15)

        ctk.CTkLabel(marco, text="Apellido del Jugador:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_apellido = ctk.CTkEntry(marco)
        self.ent_apellido.pack(pady=(0, 15), padx=20, fill="x")

        ctk.CTkLabel(marco, text="Número de Camiseta:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_numero = ctk.CTkEntry(marco)
        self.ent_numero.pack(pady=(0, 15), padx=20, fill="x")

        ctk.CTkLabel(marco, text="Minutos Jugados:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_minutos = ctk.CTkEntry(marco)
        self.ent_minutos.pack(pady=(0, 15), padx=20, fill="x")

        ctk.CTkLabel(marco, text="Posición en Campo:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.combo_posicion = ctk.CTkOptionMenu(
            marco, 
            values=["ARQUERO", "DEFENSA", "MEDIOCAMPISTA", "DELANTERO"],
            command=self.cambiar_posicion
        )
        self.combo_posicion.pack(pady=(0, 15), padx=20, fill="x")

        ctk.CTkLabel(marco, text="Goles Marcados:", font=("Arial", 12)).pack(anchor="w", padx=25)
        self.ent_goles = ctk.CTkEntry(marco)
        self.ent_goles.pack(pady=(0, 25), padx=20, fill="x")

        self.btn_guardar = ctk.CTkButton(marco, text="GUARDAR JUGADOR", height=40, command=self.guardar_datos)
        self.btn_guardar.pack(pady=10, padx=20, fill="x")

        self.ent_apellido.bind("<FocusOut>", self.validar_apellido_realtime)
        self.ent_numero.bind("<FocusOut>", self.validar_numero_realtime)
        self.ent_minutos.bind("<FocusOut>", self.validar_minutos_realtime)

    def armar_pestana_consultas(self):
        frame_filtros = ctk.CTkFrame(self.tab_consultas, fg_color="transparent")
        frame_filtros.pack(pady=10, fill="x")

        ctk.CTkButton(frame_filtros, text="Plantel Completo", command=lambda: self.actualizar_lista("TODOS")).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(frame_filtros, text="Solo Arqueros", command=lambda: self.actualizar_lista("ARQUEROS")).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(frame_filtros, text="Con Goles", command=lambda: self.actualizar_lista("GOLEADORES")).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(frame_filtros, text="Sin Goles", command=lambda: self.actualizar_lista("SIN_GOLES")).pack(side="left", padx=5, expand=True)

        self.txt_lista = ctk.CTkTextbox(self.tab_consultas, font=("Courier New", 13))
        self.txt_lista.pack(pady=10, padx=10, fill="both", expand=True)
        self.txt_lista.configure(state="disabled")

    def cambiar_posicion(self, seleccion):
        if seleccion == "ARQUERO":
            self.ent_goles.delete(0, 'end')
            self.ent_goles.configure(state="disabled", fg_color="gray30", placeholder_text="No aplica")
        else:
            self.ent_goles.configure(state="normal", fg_color=["#F9F9FA", "#343638"], placeholder_text="")

    def limpiar_formulario(self):
        self.ent_apellido.delete(0, 'end')
        self.ent_numero.delete(0, 'end')
        self.ent_minutos.delete(0, 'end')
        self.ent_goles.delete(0, 'end')
        self.combo_posicion.set("ARQUERO")
        self.cambiar_posicion("ARQUERO")
        self.ent_apellido.focus()

    def guardar_datos(self):
        try:
            if not self.ent_apellido.get().strip() or not self.ent_numero.get().strip() or not self.ent_minutos.get().strip():
                 raise ValueError("Debe completar apellido, número y minutos.")

            ape = self.ent_apellido.get()
            num = int(self.ent_numero.get())
            minu = float(self.ent_minutos.get() or 0)
            pos = self.combo_posicion.get()

            for jugador in self.equipo:
                if jugador.numero_camiseta == num:
                    raise ValueError(f"La camiseta {num} ya la tiene {jugador.apellido}.")
            
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
        self.txt_lista.configure(state="normal") 
        self.txt_lista.delete("1.0", "end")
        
        if not self.equipo:
            self.txt_lista.insert("end", "Sin jugadores cargados.\n")
            self.txt_lista.configure(state="disabled")
            return

        for j in self.equipo:
            if filtro == "ARQUEROS" and not isinstance(j, Arquero): continue
            if filtro == "GOLEADORES" and (not hasattr(j, 'goles') or j.goles == 0): continue


            # --- NUEVA LÓGICA: JUGADORES SIN GOLES ---
            # Si el filtro es "SIN_GOLES" le preguntamos al objeto: 
            # 1. ¿Tenés la capacidad de hacer goles? (hasattr)
            # 2. Si la tenés, ¿tu cantidad de goles es mayor a cero?
            # Si ambas son verdaderas, usamos "continue" para saltarlo y que no aparezca en la lista.
            if filtro == "SIN_GOLES" and hasattr(j, 'goles') and j.goles > 0: continue

            # Armamos el texto del renglón. 
            # Usamos ljust() para rellenar con espacios y zfill() para poner ceros a la izquierda.
            # Así logramos que la lista quede parejita como una tabla de Excel, sin importar el largo del apellido.
            info = f"• {j.apellido.ljust(12)} | Cam: {str(j.numero_camiseta).zfill(2)} | Min: {str(j.minutos_jugados).rjust(3)} | Pos: {j.posicion.ljust(12)}"
            
            # Solo le agregamos el texto "Goles: X" si el jugador no es un Arquero.
            if hasattr(j, 'goles'):
                info += f" | Goles: {j.goles}"
                
            self.txt_lista.insert("end", info + "\n")

        # Volvemos a cerrar el candado del cuadro de texto para que sea de solo lectura.    
        self.txt_lista.configure(state="disabled") 

    # ==========================================
    # VALIDACIONES EN TIEMPO REAL (UX)
    # ==========================================
    # Estas funciones reciben el parámetro "event" porque Tkinter se los manda automáticamente
    # cuando detecta que el usuario sacó el cursor de la caja de texto (<FocusOut>).

    def validar_apellido_realtime(self, event):
        texto = self.ent_apellido.get().strip()
        if texto and any(char.isdigit() for char in texto):
            messagebox.showwarning("Error", "El apellido no lleva números.")
            self.ent_apellido.delete(0, 'end')
            # Obligamos al cursor a volver a la caja del apellido (con 10 milisegundos de retraso para que no falle).
            self.after(10, self.ent_apellido.focus)

    def validar_numero_realtime(self, event):
        texto = self.ent_numero.get().strip()
        # isdigit() se asegura de que absolutamente todo lo ingresado sean números.
        if texto and not texto.isdigit():
            messagebox.showwarning("Error", "La camiseta solo lleva números.")
            self.ent_numero.delete(0, 'end')
            self.after(10, self.ent_numero.focus)

    def validar_minutos_realtime(self, event):
        texto = self.ent_minutos.get().strip()
        if texto:
            try: float(texto)
            # Intentamos convertirlo a float (por si jugó medio tiempo, ej: 45.5).
            except ValueError:
            # Si Python tira error al convertir, es porque el usuario metió letras.  
                  messagebox.showwarning("Error", "Los minutos deben ser numéricos.")
                self.ent_minutos.delete(0, 'end')
                self.after(10, self.ent_minutos.focus)

# Este bloque es el "botón de encendido" del programa. 
# Solo ejecuta la aplicación si abrimos este archivo directamente.
if __name__ == "__main__":
    app = AppFutbol()
    app.mainloop() # mainloop() mantiene la ventana gráfica abierta esperando a que el usuario haga algo.