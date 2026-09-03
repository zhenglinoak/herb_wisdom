import os
from FlagEmbedding import FlagReranker

class ReRankerModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance

    def get_model(self):
        if self._model is None:
            self._model = FlagReranker(
                model_name_or_path=os.getenv("RERANKER_MODEL_PATH", r"D:\Model\models\bge-reranker-large"),
                use_fp16=os.getenv("RERANKER_USE_FP16", "True").lower() == "true",
                devices=os.getenv("RERANKER_DEVICE", "cpu"),
            )
        return self._model


def load_rerank_model():
    return ReRankerModel().get_model()