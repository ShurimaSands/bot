import tkinter as tk
from tkinter import ttk
import threading
import time
import datetime
import pyttsx3
import multiprocessing
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
    guardar_pregunta_no_respondida,
    cargar_usuarios,
    guardar_usuarios,
    saludar_usuario,
   
    compartir_curiosidad,
    buscar_en_google,
    buscar_en_bing,
    guardar_preguntas_respuestas
)
from face import face_animation

class TalkingBot(tk.Tk):
    def __init__(self, talking):
        super().__init__()
        self.talking = talking
        self.title("Talking Bot")
        self.geometry("400x300")
        self.nombre = None
        self.create_widgets()
        self.engine = pyttsx3.init()
        self.voice_id = cargar_voz_seleccionada()
        if not self.voice_id:
            self.select_voice()
        self.preguntas_respuestas = cargar_preguntas_respuestas()
        self.usuarios = cargar_usuarios()
        self.get_user_name()
        self.respuestas_dadas = set()

    def create_widgets(self):
        self.entry = ttk.Entry(self)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.speak_event)
        self.button = ttk.Button(self, text="Hablar", command=self.speak)
        self.button.pack()

        self.text_area = tk.Text(self, height=10, width=50)
        self.text_area.pack(pady=10)

    def display_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def speak(self):
        if self.nombre is None:
            self.get_user_name()
            return
        
        text = self.entry.get()
        if text:
            self.display_message(f"{self.nombre}: {text}")
            respuesta = self.get_response(text)
            if respuesta:
                self.display_message(f"Bot: {respuesta}")
                duration = self.get_speech_duration(respuesta)
                self.talking.value = 1
                threading.Thread(target=self.speak_text, args=(respuesta,)).start()
            self.entry.delete(0, tk.END)

    def speak_event(self, event):
        self.speak()

    def speak_text(self, text):
        hablar(text, self.voice_id, self.talking)
        self.talking.value = 0

    def get_speech_duration(self, text):
        words_per_minute = 130
        words = len(text.split())
        return words / words_per_minute * 60

    def select_voice(self):
        print("Voces disponibles:")
        voces = listar_voces()
        while True:
            try:
                indice = int(input("Elige el número de la voz que quieres utilizar: "))
                self.voice_id = seleccionar_voz_por_indice(self.engine, indice)
                if confirmar_voz(self.voice_id):
                    guardar_voz_seleccionada(self.voice_id)
                    break
                else:
                    print("Selección de voz no confirmada. Inténtalo de nuevo.")
            except (IndexError, ValueError) as e:
                print(f"Error: {e}. Por favor, elige un número válido.")

    def get_user_name(self):
        self.name_window = tk.Toplevel(self)
        self.name_window.title("Nombre del usuario")
        self.name_window.geometry("300x100")
        
        self.name_label = tk.Label(self.name_window, text="Por favor, dime tu nombre:")
        self.name_label.pack(pady=10)
        
        self.name_entry = ttk.Entry(self.name_window)
        self.name_entry.pack(pady=5)
        
        self.name_button = ttk.Button(self.name_window, text="Guardar", command=self.save_user_name)
        self.name_button.pack(pady=5)
        
    def save_user_name(self):
        self.nombre = self.name_entry.get().strip()
        if self.nombre:
            self.usuarios[self.nombre] = {'nombre': self.nombre}
            guardar_usuarios(self.usuarios)
            saludo_inicial = saludar_usuario(self.nombre)
            self.display_message(saludo_inicial)
            hablar(saludo_inicial, self.voice_id, self.talking)
            self.name_window.destroy()

    def get_response(self, pregunta):
        # Verificar si la pregunta ya tiene una respuesta almacenada
        print("Verificando si la pregunta tiene una respuesta almacenada...")
        respuesta = obtener_respuesta(pregunta, self.preguntas_respuestas)
        if respuesta:
            print(f"Respuesta encontrada en el archivo JSON: {respuesta}")
            return respuesta

        # Si no se encuentra respuesta en el archivo JSON, buscar en Google y Bing
        print("No se encontró respuesta en el archivo JSON. Buscando en Google y Bing...")
        respuestas_google = buscar_en_google(pregunta)
        respuestas_bing = buscar_en_bing(pregunta)
        posibles_respuestas = respuestas_google + respuestas_bing

        for respuesta in posibles_respuestas:
            if respuesta not in self.respuestas_dadas:
                self.respuestas_dadas.add(respuesta)
                # Guardar la nueva pregunta y respuesta en el archivo JSON
                if pregunta not in self.preguntas_respuestas:
                    self.preguntas_respuestas[pregunta] = {'respuestas': [respuesta]}
                else:
                    self.preguntas_respuestas[pregunta]['respuestas'].append(respuesta)
                guardar_preguntas_respuestas(self.preguntas_respuestas)
                return respuesta

        # Si todas las respuestas ya han sido dadas, usar una predeterminada
        guardar_pregunta_no_respondida(pregunta, self.preguntas_respuestas)
        return "Lo siento, no tengo una respuesta para esa pregunta."

if __name__ == "__main__":
    talking = multiprocessing.Value('i', 0)
    p = multiprocessing.Process(target=face_animation, args=(talking,))
    p.start()

    app = TalkingBot(talking)
    app.mainloop()
    p.terminate()
