import datetime
from funciones import *
import pyttsx3

# Variable para mantener el contexto de la conversación
contexto = []

def agregar_contexto(pregunta, respuesta):
    if len(contexto) >= 5:
        contexto.pop(0)
    contexto.append((pregunta, respuesta))

def main():
    voz_id = cargar_voz_seleccionada()
    if not voz_id:
        print("Voces disponibles:")
        voces = listar_voces()
        while True:
            try:
                indice = int(input("Elige el número de la voz que quieres utilizar: "))
                voz_id = seleccionar_voz_por_indice(pyttsx3.init(), indice)
                if confirmar_voz(voz_id):
                    guardar_voz_seleccionada(voz_id)
                    break
                else:
                    print("Selección de voz no confirmada. Inténtalo de nuevo.")
            except (IndexError, ValueError) as e:
                print(f"Error: {e}. Por favor, elige un número válido.")

    preguntas_respuestas = cargar_preguntas_respuestas()
    usuarios = cargar_usuarios()
    nombre = obtener_nombre_usuario(usuarios)
    saludo_inicial = saludar_usuario(nombre)
    print(saludo_inicial)
    hablar(saludo_inicial, voz_id)
    
    while True:
        pregunta = input(f"{nombre}, hazme una pregunta (o escribe 'salir' para terminar, 'agregar' para agregar nuevas preguntas y respuestas, 'curiosidad' para una curiosidad): ")
        if pregunta.lower() == "salir":
            despedida = "¡Hasta luego! Fue un placer ayudarte."
            print(despedida)
            hablar(despedida, voz_id)
            break
        elif pregunta.lower() == "agregar":
            agregar_pregunta_respuesta(preguntas_respuestas)
        elif pregunta.lower() == "curiosidad":
            curiosidad = compartir_curiosidad()
            print("Curiosidad: ", curiosidad)
            hablar(curiosidad, voz_id)
        else:
            respuesta = obtener_respuesta(pregunta, preguntas_respuestas)
            if respuesta:
                respuesta_formateada = respuesta.format(datetime.datetime.now().strftime("%H:%M"))
                emocion = random.choice(['feliz', 'triste', 'emocionado'])
                respuesta_emocion = responder_con_emocion(respuesta_formateada, emocion)
                print("Respuesta: ", respuesta_emocion)
                hablar(respuesta_emocion, voz_id)
                agregar_contexto(pregunta, respuesta_formateada)
            else:
                respuesta_especial = acciones_especiales(pregunta, preguntas_respuestas)
                if respuesta_especial:
                    emocion = random.choice(['feliz', 'triste', 'emocionado'])
                    respuesta_emocion = responder_con_emocion(respuesta_especial, emocion)
                    print("Respuesta: ", respuesta_emocion)
                    hablar(respuesta_emocion, voz_id)
                    agregar_contexto(pregunta, respuesta_emocion)
                else:
                    print("Lo siento, no tengo una respuesta para esa pregunta.")
                    retroalimentar = input("¿Deseas proporcionar una respuesta para esta pregunta? (escribe 'si' para confirmar): ")
                    if retroalimentar.lower() == "si":
                        retroalimentar_respuesta("", pregunta, preguntas_respuestas)
                    else:
                        guardar_pregunta_no_respondida(pregunta, preguntas_respuestas)

if __name__ == "__main__":
    main()
