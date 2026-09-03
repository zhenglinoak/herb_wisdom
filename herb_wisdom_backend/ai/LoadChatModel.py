from langchain_ollama import ChatOllama
import time
from chat.dao import HistoryDao
from chat.util import ChromaUtil
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ChatModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance

    def get_model(self):
        if self._model is None:
            # self._model = ChatOpenAI(
            #     api_key=os.getenv("DASHSCOPE_API_KEY"),
            #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            #     model="qwen3.7-plus",
            # )
            self._model = ChatOllama(
                model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            )
        return self._model


def load_chat_model():
    return ChatModel().get_model()


if __name__ == '__main__':
    for i in load_chat_model().stream("hi"):
        print(i.content, end="", flush=True)