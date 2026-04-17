
class Jugador: # Clase base para representar a un jugador, con atributos comunes como apellido, número de camiseta y minutos jugados.
    def __init__(self, apellido, numero_camiseta, minutos_jugados=0):
        # Validación de tipo valido de apellido.
        if not isinstance(apellido, str) or not apellido.strip(): # Funcion strip() para eliminar espacios en blanco al inicio y al final, y verificar que el apellido no esté vacío.
            raise ValueError("El apellido debe ser un texto válido y no vacío.")
        self.apellido = apellido.strip()

        # Validación número de camiseta
        if not isinstance(numero_camiseta, int) or numero_camiseta <= 0:
            raise ValueError("El número de camiseta debe ser mayor a 0.")
        self.numero_camiseta = numero_camiseta

        # Validación de minutos
        if not isinstance(minutos_jugados, (int, float)) or minutos_jugados < 0:
            raise ValueError("Los minutos jugados no pueden ser negativos.") # Bloque try-except se encargará de capturar este error.
        self.minutos_jugados = minutos_jugados

    def __str__(self):
        return f"{self.apellido} (N° {self.numero_camiseta})"


class JugadorCampo(Jugador):
    
    POSICIONES_PERMITIDAS = ["DEFENSA", "MEDIOCAMPISTA", "DELANTERO"] # Posiciones válidas constantes, serviran para comparar con lo que ingrese el usuario.

    def __init__(self, apellido, numero_camiseta, posicion, goles=0, minutos_jugados=0):
        super().__init__(apellido, numero_camiseta, minutos_jugados) # Hereda los atributos de la clase Jugador.
        
        # Verificamos que posición sea un texto para evitar el crash
        if not isinstance(posicion, str):
            raise TypeError("La posición ingresada debe ser un texto.") # El bloque try-ecept se encargaría de capturar este error y mostrar este mensaje al usuario.
            
        # Limpiamos espacios en blanco (.strip()) y pasamos todo a mayúsculas (.upper())
        posicion_valida = posicion.strip().upper()
        
        # Validamos que la posicion esté dentro de las permitidas. Si no está, lanzamos un error.
        if posicion_valida in self.POSICIONES_PERMITIDAS:
            self.posicion = posicion_valida
        else:
            raise ValueError(f"Posicion de formación '{posicion}' no válida. Opciones: {self.POSICIONES_PERMITIDAS}") # Bloque try-except se encargaría de capturar este error y mostrar este mensaje.
            
        # Validación de goles posibles.
        if not isinstance(goles, int) or goles < 0:
            raise ValueError("La cantidad de goles debe ser un número entero igual o mayor a 0.")
        self.goles = goles


class Arquero(Jugador):
    def __init__(self, apellido, numero_camiseta, minutos_jugados=0):
        super().__init__(apellido, numero_camiseta, minutos_jugados) # Hereda los atributos de la clase Jugador.

        self.posicion = "ARQUERO"



"""Nota: Podemos hacer que la clase Jugador al ser padre de las otras, sea abstracta ya que no se deberia poder crear un jugador sin especificar su posicion, 
pero para eso tenemos que importar el modulo abc y hacer que Jugador herede de ABC, y luego decorar el metodo __init__ con @abstractmethod,
lo cual haria que no se pueda instanciar un objeto de la clase Jugador directamente."""