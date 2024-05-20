import pyttsx3
import random
import datetime

def cargar_preguntas_respuestas():
    with open('preguntas.txt', 'r', encoding='utf-8') as f_preguntas:
        preguntas = [linea.strip() for linea in f_preguntas.readlines()]
    with open('respuestas.txt', 'r', encoding='utf-8') as f_respuestas:
        respuestas = [linea.strip() for linea in f_respuestas.readlines()]
    return preguntas, respuestas

def obtener_respuesta(pregunta, preguntas, respuestas):
    pregunta = pregunta.lower()
    for i, key in enumerate(preguntas):
        if key.lower() in pregunta:
            return random.choice(respuestas[i].split('|'))
    return "Lo siento, no entiendo esa pregunta."

def listar_voces():
    motor = pyttsx3.init()
    voces = motor.getProperty('voices')
    for i, voz in enumerate(voces):
        print(f"Voz {i}: {voz.name}")
    return voces

def seleccionar_voz_por_indice(engine, indice):
    voces = engine.getProperty('voices')
    if 0 <= indice < len(voces):
        engine.setProperty('voice', voces[indice].id)
        return voces[indice].id
    else:
        raise IndexError("Índice de voz fuera de rango")

def confirmar_voz(voz_id, mensaje="Estas seguro? (escribe 'si' para confirmar): "):
    motor = pyttsx3.init()
    motor.setProperty('voice', voz_id)
    motor.setProperty('rate', 150)
    motor.say(mensaje)
    motor.runAndWait()
    confirmacion = input(mensaje)
    return confirmacion.lower() == 'si'

def guardar_voz_seleccionada(voz_id):
    with open('voz_seleccionada.txt', 'w', encoding='utf-8') as f:
        f.write(voz_id)

def cargar_voz_seleccionada():
    try:
        with open('voz_seleccionada.txt', 'r', encoding='utf-8') as f:
            voz_id = f.read().strip()
        return voz_id
    except FileNotFoundError:
        return None

def hablar(texto, voz_id=None):
    motor = pyttsx3.init()
    if voz_id:
        motor.setProperty('voice', voz_id)
    motor.setProperty('rate', 150)
    motor.say(texto)
    motor.runAndWait()
