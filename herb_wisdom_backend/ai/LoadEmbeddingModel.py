import os
from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance

    def get_model(self):
        if self._model is None:
            device = os.getenv("EMBEDDING_DEVICE", "cpu")
            self._model = HuggingFaceEmbeddings(
                model_name=os.getenv("EMBEDDING_MODEL_PATH", r"D:\Model\models\paraphrase-multilingual-MiniLM-L12-v2"),
                model_kwargs={"device": device, "local_files_only": True},
            )
        return self._model


def load_embedding_model():
    return EmbeddingModel().get_model()