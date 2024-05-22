import pyttsx3
import random
import json
import requests
from bs4 import BeautifulSoup

def cargar_preguntas_respuestas():
    try:
        with open('preguntas_respuestas.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('preguntas', {})
    except FileNotFoundError:
        print("Archivo preguntas_respuestas.json no encontrado. Creando uno nuevo...")
        return {}

def guardar_preguntas_respuestas(preguntas_respuestas):
    with open('preguntas_respuestas.json', 'w', encoding='utf-8') as f:
        json.dump({'preguntas': preguntas_respuestas}, f, ensure_ascii=False, indent=4)

def obtener_respuesta(pregunta, preguntas_respuestas):
    pregunta = pregunta.lower()
    respuestas = []
    for key in preguntas_respuestas:
        if key.lower() in pregunta:
            respuestas.extend(preguntas_respuestas[key])
    return random.choice(respuestas) if respuestas else None

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

def retroalimentar_respuesta(respuesta_correcta, pregunta, preguntas_respuestas):
    nueva_respuesta = input(f"La respuesta \"{respuesta_correcta}\" no es correcta para la pregunta \"{pregunta}\". Por favor, introduce la respuesta correcta: ").strip()
    if pregunta in preguntas_respuestas:
        preguntas_respuestas[pregunta].append(nueva_respuesta)
    else:
        preguntas_respuestas[pregunta] = [nueva_respuesta]
    guardar_preguntas_respuestas(preguntas_respuestas)
    print("Nueva respuesta guardada.")

def buscar_en_google(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        resultado = soup.find('div', class_='BNeawe')
        if resultado:
            return resultado.text
        else:
            return "Lo siento, no pude encontrar una respuesta clara en Google."
    else:
        return "Lo siento, no pude obtener la información de Google."

def acciones_especiales(pregunta, preguntas_respuestas):
    respuesta = None
    if "clima" in pregunta:
        ciudad = pregunta.split("en")[-1].strip()
        respuesta = buscar_en_google(f"clima en {ciudad}")
    elif "hora" in pregunta:
        respuesta = buscar_en_google("hora actual")
    else:
        respuesta = buscar_en_google(pregunta)
    
    if respuesta and respuesta != "Lo siento, no pude encontrar una respuesta clara en Google.":
        if pregunta not in preguntas_respuestas:
            preguntas_respuestas[pregunta] = [respuesta]
        else:
            preguntas_respuestas[pregunta].append(respuesta)
        guardar_preguntas_respuestas(preguntas_respuestas)
    
    return respuesta

def guardar_pregunta_no_respondida(pregunta, preguntas_respuestas):
    pregunta = pregunta.strip()
    if pregunta not in preguntas_respuestas:
        preguntas_respuestas[pregunta] = ["Respuesta pendiente"]
    guardar_preguntas_respuestas(preguntas_respuestas)
    print(f"La pregunta '{pregunta}' se ha guardado para ser respondida más tarde.")
