
# Talking Bot

Talking Bot es una aplicación interactiva que utiliza reconocimiento de voz y animaciones gráficas para responder a preguntas y realizar diversas acciones. La aplicación está construida con Python y utiliza varias bibliotecas para su funcionalidad.

## Características

- **Interfaz de usuario**: Interfaz gráfica construida con `tkinter`.
- **Síntesis de voz**: Utiliza `pyttsx3` para generar respuestas habladas.
- **Animaciones faciales**: Animaciones en 3D utilizando `pygame` y `PyOpenGL`.
- **Búsqueda de información**: Integra funcionalidades para buscar información en Google y Bing.
- **Procesamiento de lenguaje natural**: Utiliza `spacy` para procesar y entender el lenguaje natural.

## Requisitos

Asegúrate de tener Python 3 instalado en tu sistema. Luego, instala las siguientes dependencias:

```bash
pip install pyttsx3 pygame PyOpenGL numpy spacy requests beautifulsoup4
```

Luego de instalar las librerias debes ejecutar en consola el siguiente codigo:
```
python -m spacy download en_core_web_sm
```

## Archivos

- `main.py`: Archivo principal que inicia la aplicación y maneja la interfaz de usuario.
- `funciones.py`: Contiene varias funciones de utilidad para cargar datos, procesar preguntas, buscar información, etc.
- `face.py`: Maneja las animaciones faciales en 3D.
- `preguntas_respuestas.json`: Archivo JSON que almacena las preguntas y respuestas predefinidas.
- `usuarios.json`: Archivo JSON que almacena la información de los usuarios.

## Ejecución

Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
python main.py
```

## Uso

1. Al iniciar la aplicación, se abrirá una ventana GUI.
2. Introduce tu nombre en la ventana emergente.
3. Escribe una pregunta en el campo de entrada de texto y presiona "Hablar" para obtener una respuesta.
4. El bot responderá utilizando síntesis de voz y mostrará la respuesta en la ventana.

## Contribución

Si deseas contribuir a este proyecto, sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature-nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -m 'Agrega nueva característica'`).
4. Sube tus cambios (`git push origin feature-nueva-caracteristica`).
5. Abre un pull request.

## Licencia

Este proyecto está bajo la licencia de Pragmir.

## QUE TE DIVIERTAS

---

¡Gracias por usar Talking Bot!
