import datetime
import threading
import time
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
    responder_con_emocion,
    compartir_curiosidad
)
import pyttsx3
import tkinter as tk
from tkinter import ttk

class TalkingBot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Talking Bot")
        self.geometry("500x600")
        self.create_widgets()
        self.engine = pyttsx3.init()
        self.voice_id = cargar_voz_seleccionada()
        if not self.voice_id:
            self.select_voice()
        self.preguntas_respuestas = cargar_preguntas_respuestas()
        self.usuarios = cargar_usuarios()
        self.get_user_name()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        # Draw the face
        self.canvas.create_oval(100, 50, 300, 300, fill="yellow", outline="black")

        # Draw the eyes
        self.canvas.create_oval(160, 120, 180, 140, fill="black", outline="black")
        self.canvas.create_oval(220, 120, 240, 140, fill="black", outline="black")

        # Draw the mouth
        self.mouth = self.canvas.create_line(160, 220, 240, 220, fill="black", width=5)

        # Entry and button for user input
        self.entry = ttk.Entry(self)
        self.entry.pack(pady=10)
        self.button = ttk.Button(self, text="Hablar", command=self.speak)
        self.button.pack()

        self.text_area = tk.Text(self, height=10, width=50)
        self.text_area.pack(pady=10)

    def display_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def move_mouth(self, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            self.canvas.coords(self.mouth, 160, 220, 240, 230)
            time.sleep(0.2)
            self.canvas.coords(self.mouth, 160, 220, 240, 220)
            time.sleep(0.2)

    def speak(self):
        text = self.entry.get()
        if text:
            self.display_message(f"{self.nombre}: {text}")
            respuesta = self.get_response(text)
            if respuesta:
                self.display_message(f"Bot: {respuesta}")
                duration = self.get_speech_duration(respuesta)
                threading.Thread(target=self.move_mouth, args=(duration,)).start()
                threading.Thread(target=hablar, args=(respuesta, self.voice_id)).start()
            self.entry.delete(0, tk.END)

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
            hablar(saludo_inicial, self.voice_id)
            self.name_window.destroy()

    def get_response(self, pregunta):
        respuesta = obtener_respuesta(pregunta, self.preguntas_respuestas)
        if respuesta:
            return respuesta.format(datetime.datetime.now().strftime("%H:%M"))
        else:
            respuesta_especial = acciones_especiales(pregunta, self.preguntas_respuestas)
            if respuesta_especial:
                return respuesta_especial
            else:
                guardar_pregunta_no_respondida(pregunta, self.preguntas_respuestas)
                return "Lo siento, no tengo una respuesta para esa pregunta."

if __name__ == "__main__":
    app = TalkingBot()
    app.mainloop()
