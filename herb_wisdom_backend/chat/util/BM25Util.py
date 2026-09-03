import jieba
from  langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from ai import LoadChromaCon

# 中医药 RAG 安全停用词表
MEDICAL_STOP_WORDS = set([
    # 1. 纯语气词和助词（对语义无影响）
    "的", "了", "着", "过", "吗", "呢", "吧", "啊", "哦", "呀", "哈", "嘛", "呗",

    # 2. 无意义的标点符号（分词时可能会带出来）
    "，", "。", "！", "？", "；", "：", "、", "“", "”", "‘", "’", "（", "）", "【", "】",

    # 3. 极高频且无医学价值的代词
    "我", "你", "他", "她", "它", "我们", "你们", "他们", "她们", "自己", "别人",

    # 4. 纯连接词（在短文本检索中价值极低）
    "和", "与", "及", "并", "且", "而", "或", "或者", "又", "也", "都", "还",
])
def tokenize(text):
    r1=jieba.cut(text)
    return [item for item in r1 if item.strip() not in MEDICAL_STOP_WORDS and len(item.strip()) >= 1]
def bm25_retriever(vector,question,k=10):
    # 拿到向量数据库里的所有数据
    r1=vector.get()

    # 将内容分类
    ids=r1['ids']
    documents=r1['documents']
    metadatas=r1['metadatas']

    # 把数据封装成Document对象
    doc=[Document(id=ids[i],page_content=documents[i],metadata=metadatas[i]) for i in range(len(documents))]
    # 对每个文档进行分词
    r1=[tokenize(i) for i in documents]
    r2=BM25Okapi(r1)
    r3=r2.get_scores(tokenize(question))
    r4=list(zip(r3,doc))
    r5=sorted(r4,key=lambda x:x[0],reverse=True)[:k]
    r6=[i[1] for i in r5]
    return r6
if __name__ == '__main__':
    vector = LoadChromaCon.load_chroma_conn()
    bm25_retriever(vector,"肾虚")






