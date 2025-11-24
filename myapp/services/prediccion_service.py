import requests
import os
from os import getenv

# FASTAPI_URL = "http://localhost:8001/predict_all" 
FASTAPI_URL = os.getenv("API_URL")


def obtener_predicciones(texto):
    try:
        response = requests.post(
            FASTAPI_URL,
            json={"text": texto},
            timeout=25
        )

        if response.status_code == 200:
            return response.json()

        return {"error": f"FastAPI respondió con código {response.status_code}"}

    except Exception as e:
        return {"error": f"No se pudo conectar a FastAPI: {str(e)}"}
