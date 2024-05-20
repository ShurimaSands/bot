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
    agregar_pregunta_respuesta
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
    saludo_inicial = "¡Hola! Soy tu asistente virtual. Puedes hacerme preguntas, pedirme que te cuente una broma o enseñarme nuevas preguntas y respuestas."
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
            respuesta = obtener_respuesta(pregunta, preguntas_respuestas)
            if "{}" in respuesta:
                respuesta = respuesta.format(datetime.datetime.now().strftime("%H:%M"))
            print("Respuesta: ", respuesta)
            hablar(respuesta, voz_id)

if __name__ == "__main__":
    main()
