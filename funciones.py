import spacy
import pyttsx3
import random
import json
import requests
from bs4 import BeautifulSoup

# Cargar el modelo de lenguaje de spaCy
nlp = spacy.load("en_core_web_sm")

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
            respuestas.extend(preguntas_respuestas[key]['respuestas'])
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

def hablar(texto, voz_id=None, talking=None):
    motor = pyttsx3.init()
    if voz_id:
        motor.setProperty('voice', voz_id)
    motor.setProperty('rate', 150)
    if talking is not None:
        talking.value = 1
    motor.say(texto)
    motor.runAndWait()
    if talking is not None:
        talking.value = 0

def agregar_pregunta_respuesta(preguntas_respuestas):
    nueva_pregunta = input("Introduce la nueva pregunta: ").strip()
    nueva_respuesta = input("Introduce la respuesta para esa pregunta: ").strip()
    doc = nlp(nueva_pregunta)
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    if nueva_pregunta in preguntas_respuestas:
        preguntas_respuestas[nueva_pregunta]['respuestas'].append(nueva_respuesta)
        preguntas_respuestas[nueva_pregunta]['entidades'] = entidades
    else:
        preguntas_respuestas[nueva_pregunta] = {
            'respuestas': [nueva_respuesta],
            'entidades': entidades
        }
    guardar_preguntas_respuestas(preguntas_respuestas)
    print("Nueva pregunta y respuesta guardadas.")

def retroalimentar_respuesta(respuesta_correcta, pregunta, preguntas_respuestas):
    nueva_respuesta = input(f"La respuesta \"{respuesta_correcta}\" no es correcta para la pregunta \"{pregunta}\". Por favor, introduce la respuesta correcta: ").strip()
    if pregunta in preguntas_respuestas:
        preguntas_respuestas[pregunta]['respuestas'].append(nueva_respuesta)
    else:
        preguntas_respuestas[pregunta] = {
            'respuestas': [nueva_respuesta],
            'entidades': []
        }
    guardar_preguntas_respuestas(preguntas_respuestas)
    print("Nueva respuesta guardada.")

def buscar_en_google(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        if resultados:
            return resultados[0].text
        else:
            return "Lo siento, no pude encontrar una respuesta clara en Google."
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Google: {e}")
        return "Lo siento, hubo un problema al intentar conectar con Google."
    
def buscar_en_bing(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"https://www.bing.com/search?q={query}", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = soup.find_all('li', class_='b_algo')
        if resultados:
            return resultados[0].find('a').text
        else:
            return "Lo siento, no pude encontrar una respuesta clara en Bing."
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Bing: {e}")
        return "Lo siento, hubo un problema al intentar conectar con Bing."
    

from spacy.matcher import Matcher

def clasificar_intencion(doc):
    matcher = Matcher(nlp.vocab)
    patron_clima = [{"LOWER": "clima"}, {"LOWER": "en"}]
    patron_hora = [{"LOWER": "qué"}, {"LOWER": "hora"}, {"LOWER": "es"}]
    patron_hora_en = [{"LOWER": "hora"}, {"LOWER": "en"}]
    matcher.add("Clima", [patron_clima])
    matcher.add("Hora", [patron_hora])
    matcher.add("Hora_en", [patron_hora_en])
    matches = matcher(doc)
    if matches:
        for match_id, start, end in matches:
            span = doc[start:end]
            return nlp.vocab.strings[match_id]
    return "Desconocido"

def acciones_especiales(pregunta, preguntas_respuestas):
    respuesta = None
    doc = nlp(pregunta)
    intencion = clasificar_intencion(doc)
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    print("Intención:", intencion)
    print("Entidades reconocidas:", entidades)

    if intencion == "Clima":
        ciudad = pregunta.split("en")[-1].strip()
        respuesta = buscar_en_google(f"clima en {ciudad}")
    elif intencion in ["Hora", "Hora_en"]:
        ciudad = pregunta.split("en")[-1].strip() if "en" in pregunta else ""
        if ciudad:
            respuesta = buscar_en_google(f"hora en {ciudad}")
        else:
            respuesta = buscar_en_google("hora actual")
    else:
        respuesta_google = buscar_en_google(pregunta)
        respuesta_bing = buscar_en_bing(pregunta)
        respuesta = f" {respuesta_google}\nBing dice: {respuesta_bing}"
    
    if intencion == "Desconocido" and respuesta:
        if pregunta not in preguntas_respuestas:
            preguntas_respuestas[pregunta] = {
                'respuestas': [respuesta],
                'entidades': entidades
            }
        else:
            preguntas_respuestas[pregunta]['respuestas'].append(respuesta)
        guardar_preguntas_respuestas(preguntas_respuestas)
    
    return respuesta

def guardar_pregunta_no_respondida(pregunta, preguntas_respuestas):
    pregunta = pregunta.strip()
    if pregunta not in preguntas_respuestas:
        preguntas_respuestas[pregunta] = {
            'respuestas': ["Respuesta pendiente"],
            'entidades': []
        }
    guardar_preguntas_respuestas(preguntas_respuestas)
    print(f"La pregunta '{pregunta}' se ha guardado para ser respondida más tarde.")

# Nuevas funciones para interacciones adicionales
def cargar_usuarios():
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
        return usuarios
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

def obtener_nombre_usuario(usuarios):
    nombre = input("Por favor, dime tu nombre: ").strip()
    if nombre not in usuarios:
        usuarios[nombre] = {'nombre': nombre}
        guardar_usuarios(usuarios)
    return nombre

def saludar_usuario(nombre):
    return f"¡Hola, {nombre}! ¿Cómo puedo ayudarte hoy?"

def responder_con_emocion(texto, emocion):
    respuestas = {
        'feliz': [f"¡{texto}!", f"¡Genial! {texto}"],
        'triste': [f"Lamento oír eso, pero {texto}.", f"Lo siento, {texto}"],
        'emocionado': [f"¡Wow! {texto}!", f"¡Increíble! {texto}"],
    }
    return random.choice(respuestas.get(emocion, [texto]))

def compartir_curiosidad():
    curiosidades = [
        "¿Sabías que los koalas duermen hasta 22 horas al día?",
        "El corazón de un camarón está en su cabeza.",
    ]
    return random.choice(curiosidades)