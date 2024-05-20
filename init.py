import pyttsx3
import random

respuestas_basicas = {
    "Como estas?": ["Estoy bien, gracias por preguntar.", "Me siento genial, ¿y tú?"],
    "¿Cuál es tu nombre?": ["Mi nombre es Bot.", "Puedes llamarme Bot."],
    "¿Qué hora es?": ["Es hora de aprender a programar.", "Son las "],
    "¿Qué tiempo hace hoy?": ["No estoy seguro, pero siempre puedes mirar por la ventana.", "Hace un día maravilloso."],
}

def obtener_respuesta(pregunta):
    if pregunta in respuestas_basicas:
        return random.choice(respuestas_basicas[pregunta])
    else:
        return "Lo siento, no entiendo esa pregunta."

def seleccionar_voz(engine):
    # Enumerar las voces disponibles
    voces = engine.getProperty('voices')
    # Seleccionar una voz específica (cambia el índice según la voz que desees)
    voz = voces[0]  # Por ejemplo, el primer índice
    engine.setProperty('voice', voz.id)

def hablar(texto):
    motor = pyttsx3.init()
    seleccionar_voz(motor)
    motor.setProperty('rate', 150)  # Puedes ajustar la velocidad de la voz según tu preferencia
    motor.say(texto)
    motor.runAndWait()

def main():
    while True:
        pregunta = input("Hazme una pregunta (o escribe 'salir' para terminar): ")
        if pregunta.lower() == "salir":
            print("¡Hasta luego!")
            break
        respuesta = obtener_respuesta(pregunta)
        print("Respuesta: ", respuesta)
        hablar(respuesta)

if __name__ == "__main__":
    main()

#hOLA!!!!