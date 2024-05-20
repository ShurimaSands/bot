import pyttsx3
import random
import datetime
import json

def cargar_preguntas_respuestas():
    try:
        with open('preguntas_respuestas.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['preguntas']
    except FileNotFoundError:
        print("Archivo preguntas_respuestas.json no encontrado. Creando uno nuevo...")
        return {}

def guardar_preguntas_respuestas(preguntas_respuestas):
    with open('preguntas_respuestas.json', 'w', encoding='utf-8') as f:
        json.dump({'preguntas': preguntas_respuestas}, f, ensure_ascii=False, indent=4)

def obtener_respuesta(pregunta, preguntas_respuestas):
    pregunta = pregunta.lower()
    for key in preguntas_respuestas:
        if key.lower() in pregunta:
            return random.choice(preguntas_respuestas[key])
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

def agregar_pregunta_respuesta(preguntas_respuestas):
    nueva_pregunta = input("Introduce la nueva pregunta: ").strip()
    nueva_respuesta = input("Introduce la respuesta para esa pregunta: ").strip()
    if nueva_pregunta in preguntas_respuestas:
        preguntas_respuestas[nueva_pregunta].append(nueva_respuesta)
    else:
        preguntas_respuestas[nueva_pregunta] = [nueva_respuesta]
    guardar_preguntas_respuestas(preguntas_respuestas)
    print("Nueva pregunta y respuesta guardadas.")



def obtener_respuesta(pregunta, preguntas_respuestas):
    pregunta = pregunta.lower()
    respuestas = []
    for key in preguntas_respuestas:
        if key.lower() in pregunta:
            respuestas.extend(preguntas_respuestas[key])  # Agregamos las respuestas para esta pregunta
    if respuestas:
        return random.choice(respuestas)  # Devolvemos una respuesta aleatoria
    else:
        return None  # Si no se encontró una respuesta, devolvemos None


def retroalimentar_respuesta(respuesta_correcta, pregunta, preguntas_respuestas):
    nueva_respuesta = input(f"La respuesta \"{respuesta_correcta}\" no es correcta para la pregunta \"{pregunta}\". Por favor, introduce la respuesta correcta: ").strip()
    if pregunta in preguntas_respuestas:
        preguntas_respuestas[pregunta].append(nueva_respuesta)
    else:
        preguntas_respuestas[pregunta] = [nueva_respuesta]
    guardar_preguntas_respuestas(preguntas_respuestas)
    print("Nueva respuesta guardada.")
