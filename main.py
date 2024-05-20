import datetime
from funciones import (
    cargar_preguntas_respuestas, 
    obtener_respuesta, 
    listar_voces, 
    seleccionar_voz_por_indice, 
    confirmar_voz, 
    guardar_voz_seleccionada, 
    cargar_voz_seleccionada, 
    hablar
)
import pyttsx3

def main():
    voz_id = cargar_voz_seleccionada()
    if not voz_id:
        print("Voces disponibles:")
        voces = listar_voces()
        indice = int(input("Elige el número de la voz que quieres utilizar: "))
        try:
            voz_id = seleccionar_voz_por_indice(pyttsx3.init(), indice)
            if confirmar_voz(voz_id):
                guardar_voz_seleccionada(voz_id)
            else:
                print("Selección de voz no confirmada. Usando la voz por defecto.")
                voz_id = None
        except IndexError as e:
            print(f"Error: {e}. Usando la voz por defecto.")
            voz_id = None

    preguntas_respuestas = cargar_preguntas_respuestas()
    print("¡Hola! Soy tu asistente virtual. Puedes hacerme preguntas o pedirme que te cuente una broma.")
    while True:
        pregunta = input("Hazme una pregunta (o escribe 'salir' para terminar): ")
        if pregunta.lower() == "salir":
            despedida = "¡Hasta luego! Fue un placer ayudarte."
            print(despedida)
            hablar(despedida, voz_id)
            break
        respuesta = obtener_respuesta(pregunta, preguntas_respuestas)
        if "{}" in respuesta:
            respuesta = respuesta.format(datetime.datetime.now().strftime("%H:%M"))
        print("Respuesta: ", respuesta)
        hablar(respuesta, voz_id)

if __name__ == "__main__":
    main()
