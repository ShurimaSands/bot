import datetime
from funciones import (
    cargar_preguntas_respuestas, 
    obtener_respuesta, 
    listar_voces, 
    seleccionar_voz_por_indice, 
    confirmar_voz, 
    guardar_voz_seleccionada, 
    cargar_voz_seleccionada, 
    hablar,
    agregar_pregunta_respuesta,
    retroalimentar_respuesta,
    acciones_especiales,
    guardar_pregunta_no_respondida
)
import pyttsx3

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
    saludo_inicial = "¡Hola! ¿Cómo te puedo ayudar hoy?"
    print(saludo_inicial)
    hablar(saludo_inicial, voz_id)
    
    while True:
        pregunta = input("Hazme una pregunta (o escribe 'salir' para terminar, 'agregar' para agregar nuevas preguntas y respuestas): ")
        if pregunta.lower() == "salir":
            despedida = "¡Hasta luego! Fue un placer ayudarte."
            print(despedida)
            hablar(despedida, voz_id)
            break
        elif pregunta.lower() == "agregar":
            agregar_pregunta_respuesta(preguntas_respuestas)
        else:
            respuesta_especial = acciones_especiales(pregunta, preguntas_respuestas)
            if respuesta_especial:
                print("Respuesta: ", respuesta_especial)
                hablar(respuesta_especial, voz_id)
            else:
                respuesta = obtener_respuesta(pregunta, preguntas_respuestas)
                if respuesta:
                    respuesta_formateada = respuesta.format(datetime.datetime.now().strftime("%H:%M"))
                    print("Respuesta: ", respuesta_formateada)
                    hablar(respuesta_formateada, voz_id)
                else:
                    print("Lo siento, no tengo una respuesta para esa pregunta.")
                    retroalimentar = input("¿Deseas proporcionar una respuesta para esta pregunta? (escribe 'si' para confirmar): ")
                    if retroalimentar.lower() == "si":
                        retroalimentar_respuesta("", pregunta, preguntas_respuestas)
                    else:
                        guardar_pregunta_no_respondida(pregunta, preguntas_respuestas)

if __name__ == "__main__":
    main()
