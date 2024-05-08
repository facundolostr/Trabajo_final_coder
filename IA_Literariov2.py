from os import system 
from abc import ABC,abstractmethod
import openai
# Definición de la API key de OpenAI
openai.api_key = "sk-proj-rWq5NTvCacX4Md5mBeIGT3BlbkFJ2gfSJHMtU5lqx1ZfuUQu"

#cierra el programa
def cerrar():
    print ("Gracias por usar nuestros servicios")
    exit()

# Función que solicita una respuesta S/N del usuario
def continua(texto_pregunta):
    resp = input(f'{texto_pregunta} [S/N]: ').upper()
    if resp == 'S':
        return True
    return False


# Función que devuelve un título centrado con guiones
def titulo(texto:str,largo:int=80):
    return f"{'-'*largo}\n{texto.title().center(largo)}\n{'-'*largo}"


# Función que calcula el largo de la opción más larga en un menú
def obtener_largo_opcion_mas_larga(tupla_opciones):
    maximo_largo = -float('inf')
    for i,texto in enumerate(tupla_opciones):
        if len(texto) > maximo_largo:
            maximo_largo = len(texto)
    return maximo_largo

# Función que verifica si una cadena es un entero
def isint(str_numero:str)->bool:
    try:                    # Intenta convertir str_numero a int
        int(str_numero)
    except:                 # Si no puede convertirlo devuelve False
        return False
    return True             # Si puede convertirlo devuelve True


# Función que lee un entero en un rango determinado
def leer_entero(mensaje:str='Ingrese un entero: ',minimo:int=-float('inf'),maximo:int=float('inf'))->int:
    todo_ok = False
    while not todo_ok:
        cadena = input(mensaje)
        if isint(cadena):
            numero = int(cadena)
            if minimo <= numero <= maximo:
                todo_ok = True
            else:
                print(f"Número {numero} fuera de rango [{minimo}] .. [{maximo}]")
        else:
            print(f"{cadena} No es un int.")    
    return int(cadena)

# Función que muestra un menú con las opciones de una tupla
def opcion(tupla_opciones:str)->int:
    #La primera opcion es el titulo
    #Las demas son las opciones
    largo = obtener_largo_opcion_mas_larga(tupla_opciones)
    system("cls")
    for index,opcion in enumerate(tupla_opciones):
        if index == 0: 
            print(titulo(opcion,largo))
        else:
            print(opcion.title())
    return leer_entero("Ingrese una opcion: ",1,4)

# Clase abstracta para el Asistente Literario
class AsistenteLiterario(ABC):
    def __init__(self) -> None:
        self.__nombre = "BookIa"
        self._pregunta_historia = None
        self.__respuesta = None
        self.__historia = None
        self.__consulta = None
        self.__OPCIONES = ["Escoge alguna opcion",
        "1. Asistente literario",
        "2. Asistente con imagen",
        "3. Salir del programa"
        ]
        self._OPCIONES_HISTORIA =["Escoje alguna opcion",
        "1. Tengo una historia",
        "2. Quiero crear una historia",
        "3. Salir del programa"
        ]

#Este metodo es para preguntarle al usuario si tiene una historia o crear una historia en el momento y trabajar sobre ello
    def consultar_historia (self) ->None:
        self._pregunta_historia = opcion(self._OPCIONES_HISTORIA)

        if self._pregunta_historia == 1:
            self.mandar_historia()
        elif self._pregunta_historia == 2:
            self.crear_historia()
        elif self._pregunta_historia == 3:
            cerrar()
        else:
            raise ValueError("Marque una opción válida")

#Metodo para crear una historia segun las especificaciones del usuario
    def crear_historia (self) ->str:
        generoHis = input("Indique el genero y/o subgenero de la historia: ")
        trama = input ("Indique de que quiere que se trate la historia: ")

        contexto = f"Creame una historia en 500 caracteres teniendo en cuenta, el genero: '{generoHis}' y la trama general: '{trama}'"
        conversacion = [{"role": "user", "content": contexto}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversacion,
            max_tokens=200
        )

        respuesta_texto = response['choices'][0]['message']['content'].strip()
        print("BookIa: \n", respuesta_texto)

        self.__historia = respuesta_texto

        if continua("Quiere hacer una consulta?"):
            self._interfaz()
        else:
            cerrar()


# Método para obtener y enviar la historia al Asistente Literario
    def mandar_historia(self) ->str:
        self.__historia = input("Escribe la historia con la cual trabajaremos: ")
        print(f"\n La historia que has ingresado es: \n''{self.__historia}''")
        return self.__historia

# Método para procesar la historia y realizar consultas
    def procesar_historia(self) -> None:
        self.__consulta = self.consulta() #Ejemplo "Quiero que me hagas una lluvia de ideas para continuar la historia. Como maximo 2 respuestas"

        contexto = f"{self.__historia}\nUsuario: {self.__consulta}"
        conversacion = [{"role": "user", "content": contexto}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversacion,
            max_tokens=200
        )

        respuesta_texto = response['choices'][0]['message']['content'].strip()
        print("BookIa: \n", respuesta_texto)

        if continua("Alguna otra consulta?"):
            self._interfaz()
        else:
            cerrar()

# Método para recibir la consulta del usuario
    def consulta(self) -> str:
        return str(input("\n Escriba la solicitud que desee realizar: "))

    def __str__ (self) ->str:
        return titulo("Bienvenido al asistente literario")

    def nombre (self) ->str:
        return self.__nombre

    def _interfaz(self) ->None:
        self.__respuesta = opcion(self.__OPCIONES)

        if self.__respuesta == 1:
            self.procesar_historia()
        elif self.__respuesta == 2:
            self.procesar_imagen()
        elif self.__respuesta ==3:
            cerrar()
        else:
            raise ValueError("Marque una opción válida")
        

    def procesar_imagen(self) -> None:
        # Aquí se llama al Asistente de Imágenes y se pasa el contexto de la historia
        asistente_imagen = AsistenteImagen(self.__historia)
        asistente_imagen._interfaz()


# Clase para el Asistente de Imágenes
class AsistenteImagen:
    def __init__ (self, historia) -> None:
        self.__asistente_literario = AsistenteLiterario()
        self.__consulta_especifica = None
        self.__nombre = "BookIa" 
        self.__respuesta_imagen = None
        self.__respuesta = None
        self.__imagen = None
        self.__historia = historia  # Aquí se recibe el contexto de la historia
        self.__consulta = None
        self.__OPCIONES = ["Escoge alguna opcion",
                           "1. Crear una imagen",
                           "2. Volver al menú principal"
                           ]

        self.__OPCIONES_IMG = ["Escoge alguna opcion",
                            "1. Crear una portada",
                            "2. Crear una escenografía",
                            "3. Crear un personaje",
                            "4. Salir del programa"]

# Método para obtener el nombre del asistente de imágenes
    def nombre(self) -> str:
        return self.__nombre

# Método para obtener la representación en cadena del asistente de imágenes
    def __str__(self) -> str:
        return titulo("Bienvenido al asistente de imágenes")

 # Método para gestionar la interfaz del asistente de imágenes
    def _interfaz(self) -> None:
        self.__respuesta = opcion(self.__OPCIONES)

        if self.__respuesta == 1:
            self.consulta_imagen()
        elif self.__respuesta == 2:
            self.__asistente_literario._interfaz()
        else:
            raise ValueError("Marque una opción válida")

 # Método para manejar la consulta relacionada con la creación de imágenes
    def consulta_imagen(self) ->None:
        self.__respuesta_imagen = opcion(self.__OPCIONES_IMG)

        if self.__respuesta_imagen == 1:
            self.crear_portada()
        elif self.__respuesta_imagen == 2:
            self.crear_escena()
        elif self.__respuesta_imagen == 3:
            self.crear_pj()
        elif self.__respuesta_imagen == 4:
            cerrar()
        else:
            raise ValueError("Marque una opción válida")

# Método para crear una portada según las especificaciones proporcionadas
    def crear_portada(self) -> None:
        portada = input("Ingrese las especificaciones para la portada: ")
        self.__consulta_especifica = f"Creame una imagen para usar de portada, teniendo en cuenta la historia y las siguientes especificaciones: {portada}"
        self.procesar_imagen()

# Método para crear una escena según las especificaciones proporcionadas    
    def crear_escena(self) -> None:
        escenografia = input("Ingrese las especificaciones para crear una imagen de la escenografia: ")
        self.__consulta_especifica = f"Creame una imagen que represente la escenografia, teniendo en cuenta la historia y las siguientes especificaciones: {escenografia}"
        self.procesar_imagen()

# Método para crear un personaje según las especificaciones proporcionadas
    def crear_pj(self) -> None:
        personaje = input("Ingrese las especificaciones para crear una imagen del personaje: ")
        self.__consulta_especifica = f"Creame una imagen del personaje principal, teniendo en cuenta la historia y las siguientes especificaciones: {personaje}"
        self.procesar_imagen()

# Metodo para crear la imagen con el contexto de la historia y la consulta
    def crear_imagen(self,consulta) -> str:
        self.__consulta = f"{self.__historia}[:400]\n{consulta}" # "Creame una imagen para usar de portada, teniendo en cuenta la historia"
        image_response = openai.Image.create(
            prompt=self.__consulta,
            n=1,
            size="1024x1024"
        )
        return image_response['data'][0]['url']

# Método para procesar la historia y realizar la imagen
    def procesar_imagen(self) -> None:
        nueva_consulta = self.__consulta_especifica
        self.__imagen = self.crear_imagen(nueva_consulta)
        print("Imagen creada:", self.__imagen)

        if continua("¿Desea crear otra imagen?"):
            self._interfaz()
        else:
            print("\n ---**--- Gracias por usar el asistente de imágenes. ---**--- \n")
            exit()



# Defino la parte principal del programa para que pueda iniciarse
def main():
    asistente = AsistenteLiterario()
    
    while True:
        print(titulo(f"Bienvenido a *{asistente.nombre()}*"))
        system('pause')
        asistente.consultar_historia()
        system('pause')
        asistente._interfaz()
main()

# Verificar si este archivo es el punto de entrada principal
if __name__ == "__main__":
    main()