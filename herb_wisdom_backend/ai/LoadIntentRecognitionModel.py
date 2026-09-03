import os
from langchain_ollama import ChatOllama

class IntentRecognitionModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance

    def get_model(self):
        if self._model is None:
            self._model = ChatOllama(
                model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            )
        return self._model


def load_intent_recognition_model():
    return IntentRecognitionModel().get_model()