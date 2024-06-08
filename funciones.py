import spacy
import pyttsx3
import random
import json
import requests
from bs4 import BeautifulSoup

# Inicializa pyttsx3
engine = pyttsx3.init()

# Cargar el modelo de lenguaje de spaCy
nlp = spacy.load("en_core_web_sm")

def cargar_preguntas_respuestas():
    try:
        with open('preguntas_respuestas.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Preguntas y respuestas cargadas correctamente.")
        return data.get('preguntas', {})
    except FileNotFoundError:
        print("Archivo preguntas_respuestas.json no encontrado. Creando uno nuevo...")
        return {}

def guardar_preguntas_respuestas(preguntas_respuestas):
    with open('preguntas_respuestas.json', 'w', encoding='utf-8') as f:
        json.dump({'preguntas': preguntas_respuestas}, f, ensure_ascii=False, indent=4)

def normalizar_texto(texto):
    return texto.lower().strip()

def obtener_respuesta(pregunta, preguntas_respuestas):
    pregunta_normalizada = normalizar_texto(pregunta)
    print(f"Buscando respuesta para: {pregunta_normalizada}")
    for pregunta_guardada in preguntas_respuestas:
        if normalizar_texto(pregunta_guardada) == pregunta_normalizada:
            respuestas = preguntas_respuestas[pregunta_guardada]['respuestas']
            print(f"Respuestas encontradas: {respuestas}")
            return random.choice(respuestas) if respuestas else None
    return None

def listar_voces():
    voices = engine.getProperty('voices')
    for idx, voice in enumerate(voices):
        print(f"Voz {idx}: {voice.name}")

def seleccionar_voz(voice_id):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)

def hablar(texto, voice_id=None, talking=None):
    if voice_id is not None:
        seleccionar_voz(voice_id)
    engine.say(texto)
    engine.runAndWait()
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
        resultados = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd', limit=5)
        enlaces = soup.find_all('a', href=True, limit=5)
        respuestas = [resultado.text for resultado in resultados if resultado.text.strip()]
        urls = [enlace['href'] for enlace in enlaces if 'url?q=' in enlace['href']]
        
        # Filtrar las respuestas irrelevantes
        respuestas = [respuesta for respuesta in respuestas if len(respuesta.split()) > 2 and '?' not in respuesta]
        
        # Procesar URLs
        urls = [url.split('&')[0].replace('/url?q=', '') for url in urls]
        
        return respuestas, urls
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Google: {e}")
        return ["Lo siento, hubo un problema al intentar conectar con Google."], []

def buscar_en_bing(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"https://www.bing.com/search?q={query}", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = soup.find_all('li', class_='b_algo', limit=5)
        respuestas = [resultado.find('a').text for resultado in resultados if resultado.find('a') and resultado.find('a').text.strip()]
        urls = [resultado.find('a')['href'] for resultado in resultados if resultado.find('a')]
        
        # Filtrar las respuestas irrelevantes
        respuestas = [respuesta for respuesta in respuestas if len(respuesta.split()) > 2 and '?' not in respuesta]
        
        return respuestas, urls
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Bing: {e}")
        return ["Lo siento, hubo un problema al intentar conectar con Bing."], []

def extraer_informacion_completa(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer párrafos de la página
        parrafos = soup.find_all('p')
        texto_completo = ' '.join([p.text for p in parrafos if p.text.strip()])
        
        # Limitar el texto completo a una longitud razonable para evitar respuestas demasiado largas
        return texto_completo[:2000] if len(texto_completo) > 2000 else texto_completo
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con {url}: {e}")
        return "Lo siento, hubo un problema al intentar extraer información de la página."

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
        respuesta, urls = buscar_en_google(f"clima en {ciudad}")
    elif intencion in ["Hora", "Hora_en"]:
        ciudad = pregunta.split("en")[-1].strip() if "en" in pregunta else ""
        if ciudad:
            respuesta, urls = buscar_en_google(f"hora en {ciudad}")
        else:
            respuesta, urls = buscar_en_google("hora actual")
    else:
        respuestas_google, urls_google = buscar_en_google(pregunta)
        respuestas_bing, urls_bing = buscar_en_bing(pregunta)
        respuestas_combined = respuestas_google + respuestas_bing
        urls_combined = urls_google + urls_bing
        
        # Extraer información completa de los primeros enlaces
        respuesta_completa = None
        for url in urls_combined:
            respuesta_completa = extraer_informacion_completa(url)
            if respuesta_completa:
                break
        
        if respuesta_completa:
            respuesta = respuesta_completa
        else:
            respuesta = respuestas_combined[0] if respuestas_combined else "Lo siento, no tengo una respuesta para esa pregunta."

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

def compartir_curiosidad():
    curiosidades = [
        "¿Sabías que los koalas duermen hasta 22 horas al día?",
        "El corazón de un camarón está en su cabeza.",
    ]
    return random.choice(curiosidades)
