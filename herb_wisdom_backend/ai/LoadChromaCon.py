import os
from langchain_chroma import Chroma
from ai import LoadEmbeddingModel

class ChromaClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
        return cls._instance

    def get_client(self):
        if self._client is None:
            self._client = Chroma(
                persist_directory=os.getenv("CHROMA_PERSIST_DIR", r"/\data\herbal_medicine_data"),
                collection_name=os.getenv("CHROMA_COLLECTION_NAME", r"herbal_medicine_data"),
                embedding_function=LoadEmbeddingModel.load_embedding_model()
            )
        return self._client


def load_chroma_conn():
    return ChromaClient().get_client()

if __name__ == '__main__':
    import json

    # # 获取chroma全部数据
    # data = load_chroma_conn().get()
    #
    # # 导出为json文件
    # with open("D:\RAG_DATA\chroma_full_export.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=2)
    # print("导出完成，文件：chroma_full_export.json")
    #