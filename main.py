import tkinter as tk
import pyttsx3
from tkinter import ttk
import threading
import multiprocessing
import time
from funciones import (
    cargar_preguntas_respuestas,
    obtener_respuesta,
    listar_voces,
    seleccionar_voz,
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
    def __init__(self, talking, queue):
        super().__init__()
        self.talking = talking
        self.queue = queue
        self.title("Talking Bot")
        self.geometry("400x300")
        self.nombre = None
        self.create_widgets()
        self.engine = pyttsx3.init()
        self.engine.connect('started-utterance', self.on_speak_start)
        self.engine.connect('finished-utterance', self.on_speak_end)
        listar_voces()
        self.voice_id = 0  # Puedes cambiar esto a la voz que desees usar
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

    def on_speak_start(self, name):
        self.talking.value = 1

    def on_speak_end(self, name, completed):
        self.talking.value = 0

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
                threading.Thread(target=self.speak_text, args=(respuesta,)).start()
                for letter in respuesta:
                    self.queue.put(letter)
                    time.sleep(0.1)  # Simula el tiempo de pronunciación de cada letra
            self.entry.delete(0, tk.END)

    def speak_event(self, event):
        self.speak()

    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_response(self, pregunta):
        print("Verificando si la pregunta tiene una respuesta almacenada...")
        respuesta = obtener_respuesta(pregunta, self.preguntas_respuestas)
        if respuesta:
            print(f"Respuesta encontrada en el archivo JSON: {respuesta}")
            return respuesta

        print("No se encontró respuesta en el archivo JSON. Buscando en Google y Bing...")
        respuesta = acciones_especiales(pregunta, self.preguntas_respuestas)
        if respuesta:
            return respuesta

        guardar_pregunta_no_respondida(pregunta, self.preguntas_respuestas)
        return "Lo siento, no tengo una respuesta para esa pregunta."

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

if __name__ == "__main__":
    talking = multiprocessing.Value('i', 0)
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=face_animation, args=(talking, queue))
    p.start()

    app = TalkingBot(talking, queue)
    app.mainloop()
    p.terminate()
