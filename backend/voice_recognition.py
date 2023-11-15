import speech_recognition as sr


def reconocimiento_audio(idioma: str) -> str:
    """Traductor de audio a texto para inglés y español

    Args:
        idioma (str): Parametro que indica el idioma del audio que va a ingresar

    Returns:
        audio_reconocido (str): Texto generado del audio recibido en el idioma correspondiente.
    """

    recognizer = sr.Recognizer()
    # Listening to our microphone
    with sr.Microphone() as source:
        print("Please start talking...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        # Translating audio to text
        if idioma.lower() == "spanish":
            audio_reconocido = recognizer.recognize_google(audio, language="es-ES")
        elif idioma.lower() == "english":
            audio_reconocido = recognizer.recognize_google(audio, language="en-US")
        else:
            audio_reconocido = "Language not recognized in database"

    except sr.UnknownValueError:
        if idioma.lower() == "spanish":
            audio_reconocido = "Audio no reconocido. Intente de nuevo."
        elif idioma.lower() == "english":
            audio_reconocido = "Audio was not recognized. Try again."

    except sr.RequestError as e:
        audio_reconocido = f"Request Error: {e}"

    finally:
        return audio_reconocido


# Pruebas
if __name__ == "__main__":
    reconocimiento_audio("spanish")
    reconocimiento_audio("english")
