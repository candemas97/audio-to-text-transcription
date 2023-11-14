# python3 -m venv venv
# source venv/bin/activate

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from backend import voice_recognition

app = FastAPI()

templates = Jinja2Templates(directory="./frontend")


@app.get("/", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Audio en español a transcribir
@app.websocket("/listen-es")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Revisa que se tengan permisos de micrófono en el pc

    try:
        # await websocket.send_text(
        #     "Connection established!"
        # )  # Probar que se generó conexión

        # while True: # Si se quiere varias veces usar el while
        try:
            await websocket.receive_bytes()  # Hace que se imprima texto en frontend

            print(
                "Por favor empieza a hablar lo que quieres transcribir"
            )  # Esto es para consola, se puede quitar

            # Indica en pantalla que ya puede empezar a hablar
            await websocket.send_text(
                "Por favor empieza a hablar lo que quieres transcribir..."
            )
            # Se traduce lo hablado a texto
            audio_reconocido = voice_recognition.reconocimiento_audio("spanish")

            # Se envía el texto reconocido de vuelta
            await websocket.send_text(audio_reconocido)

            print(audio_reconocido)

        except Exception as e:
            print(f"Error during speech recognition: {e}")

    except Exception as e:
        raise Exception(f"Could not process audio: {e}")
    finally:
        await websocket.close()  # Se cierra


# Audio en inglés a transcribir
@app.websocket("/listen-en")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Revisa que se tengan permisos de micrófono en el pc

    try:
        # await websocket.send_text(
        #     "Connection established!"
        # )  # Mostramos que se generó conexión

        # while True: # Si se quiere varias veces usar el while
        try:
            await websocket.receive_bytes()  # Hace que se imprima texto en frontend

            print(
                "Start talking what you want to transcribe"
            )  # Esto es para consola, se puede quitar

            # Indica en pantalla que ya puede empezar a hablar
            await websocket.send_text(
                "Please start talking what you want to transcribe..."
            )
            # Se traduce lo hablado a texto
            audio_reconocido = voice_recognition.reconocimiento_audio("english")

            # Se envía el texto reconocido de vuelta
            await websocket.send_text(audio_reconocido)

            print(audio_reconocido)

        except Exception as e:
            print(f"Error during speech recognition: {e}")

    except Exception as e:
        raise Exception(f"Could not process audio: {e}")
    finally:
        await websocket.close()  # Se cierra


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)  # Prueba en el sistema
