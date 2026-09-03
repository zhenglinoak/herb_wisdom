import os
import json
import glob
from langchain_core.documents import Document
from langchain_chroma import Chroma
from ai import LoadEmbeddingModel
def build():
    # --- 1. 配置路径 ---
    JSON_DIR = os.getenv("RAG_DATA_DIR", r"D:\RAG_DATA\herb_dataset")
    PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", r"/\data\herbal_medicine_data")
    COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "herbal_medicine_data")
    BATCH_SIZE = 500  # 每批写入数据库的文档数量

    # --- 2. 读取并处理数据 ---
    documents = []
    json_files = glob.glob(os.path.join(JSON_DIR, "*.json"))
    print(f"正在扫描文件夹，共发现 {len(json_files)} 个药材文件...")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            drug_name = data.get("药物", "未知药物")
            treatments = data.get("治疗", [])

            for item in treatments:
                disease = item.get("疾病", "").strip()
                usage = item.get("用法", "")

                # 1. 过滤掉没有疾病名的无效数据
                if not disease:
                    continue

                # 2. 核心防御：处理用法为 null、字符串、列表三种情况
                if usage is None or (isinstance(usage, str) and not usage.strip()):
                    # 情况A：用法为空，只记录功效
                    content = f"药材【{drug_name}】具有【{disease}】的功效。"
                elif isinstance(usage, list):
                    # 情况B：用法是列表（多个方子），将其合并为清晰的文本
                    usage_text = "\n".join([f"方子{i + 1}：{u}" for i, u in enumerate(usage)])
                    content = f"药材【{drug_name}】可以治疗【{disease}】，有以下具体用法：\n{usage_text}"
                else:
                    # 情况C：正常的字符串用法
                    content = f"药材【{drug_name}】可以治疗【{disease}】，具体用法是：{usage}"

                # 3. 封装成 Document
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": os.path.basename(file_path),
                        "drug_name": drug_name,
                        "disease": disease
                    }
                )
                documents.append(doc)

        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")

    print(f"数据处理完成，共生成 {len(documents)} 条有效知识条目。")

    # --- 3. 存入 Chroma 数据库 ---
    if not documents:
        print("没有读取到任何有效数据，请检查JSON文件格式或路径。")
        return

    try:
        print(f"正在初始化数据库: {PERSIST_DIR} ...")
        # 取或创建集合，并清空旧数据，防止重复运行产生冗余
        embedding_function = LoadEmbeddingModel.load_embedding_model()
        db = Chroma(
            persist_directory=PERSIST_DIR,
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_function,
            collection_metadata={"hnsw:space": "cosine"}
        )


        # 分批写入，防止内存溢出
        for i in range(0, len(documents), BATCH_SIZE):
            batch = documents[i : i + BATCH_SIZE]
            db.add_documents(batch)
            print(f"   已写入 {min(i + BATCH_SIZE, len(documents))} / {len(documents)} 条...")

        print("数据构建全部完成！")

    except Exception as e:
        print(f"数据构建失败: {e}")

# 执行构建

# build()
#
eb=LoadEmbeddingModel.load_embedding_model()
vector=Chroma(
    persist_directory=r"D:\Project1\final_rag\data\herbal_medicine_data",
    collection_name=r"herbal_medicine_data",
    embedding_function=eb,
)

#
retriever=vector.as_retriever(search_kwargs={"k":10})
query = "肾虚怎么办？"

# 2. 调用 retriever 进行检索
# invoke 返回的是一个 Document 对象的列表
docs = retriever.invoke(query)
print(docs)

# # retriever_with_filter = vector.as_retriever(
# #     search_kwargs={
# #         "k": 5,
# #         "filter": {"disease": "痔疮"}  # 限定只在这个药里找
# #     }
# # )
# # docs = retriever_with_filter.invoke(query)
# # print(docs)
# # 检查数据库中是否有“酢浆草”的数据
# herb_retriever = vector.as_retriever(
#     search_kwargs={
#         "k": 10,
#         "filter": {"drug_name": "酢浆草"}  # 强制只查酢浆草
#     }
# )
# docs = herb_retriever.invoke("痔疮出血怎么办？")
#
# print(f"检索到 {len(docs)} 条关于【酢浆草】的记录：")
# for doc in docs:
#     print(doc.page_content)