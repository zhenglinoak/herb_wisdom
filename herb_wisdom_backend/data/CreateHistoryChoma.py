import chromadb
import uuid
import time
from FlagEmbedding import FlagAutoModel

start = time.time()

client = chromadb.PersistentClient(path="./chat_memory_db")

collection = client.get_or_create_collection(
    name="chat_history",
    metadata={"hnsw:space": "cosine"}
)

# raw_records = [
#     {"history_id": 26, "question": "hi", "user_name": "zz", "parent_id": 0, "answer": "Hello! How can I assist you today?"},
#     {"history_id": 27, "question": "thank you", "user_name": "zz", "parent_id": 0, "answer": "You're welcome! If you have any questions or need further assistance, feel free to ask!"},
#     {"history_id": 28, "question": "hi", "user_name": "11", "parent_id": 0, "answer": "Hello! How can I assist you today?"},
#     {"history_id": 29, "question": "亲", "user_name": "11", "parent_id": 0, "answer": "您好！有什么可以帮助您的吗？"}
# ]
#
#
#
# ids = []
# metadatas = []
# document = []
# for i in raw_records:
#     docx = f"User: {i['question']}\nAI: {i['answer']}"
#     metadata = {
#         "user_name": i['user_name'],
#         "parent_id": i['parent_id'],
#         "history_id": i['history_id'],
#     }
#     unique_id = str(uuid.uuid4())
#     ids.append(unique_id)
#     document.append(docx)
#     metadatas.append(metadata)
#
#
#
# collection.add(
#     ids=ids,
#     documents=document,
#     metadatas=metadatas,
# )
# results = collection.query(
#     query_texts=["redis"],
#     n_results=3,  # 只取最相关的3条作为上下文
#     where={"user_name": "zz"}  # 只查当前用户的历史
# )

print(collection.get())
print(collection.invo)

# print(results)

end = time.time()
sec = end - start
m = int(sec // 60)
s = sec % 60
print(f"用时：{m}分{s:.2f}秒")