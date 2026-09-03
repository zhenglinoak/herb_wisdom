from langchain_core.documents import Document
d1 = [
    Document(id="1", page_content="猪肾可以治疗肾虚遗精"),
    Document(id="2", page_content="羊肾治疗肾虚腰痛"),
    Document(id="3", page_content="甘薯滋养肾阴"),
    Document(id="4", page_content="人乳益肾补虚")
]

d2 = [
    Document(id="1", page_content="猪肾可以治疗肾虚遗精"),
    Document(id="2", page_content="羊肾治疗肾虚腰痛"),
    Document(id="5", page_content="甘薯滋养肾阴"),
    Document(id="6", page_content="人乳益肾补虚")
]


def f1(o):
    # 计算RRF得分
    # {文档id:RRF得分}
    l1={}
    for index, item in enumerate(o,start=1):
        l1[item.id]=1/(60+index)
    return l1
def rrf(vector_result,bm25_result):
    # 计算RRF得分
    r1=f1(vector_result)
    r2=f1(bm25_result)

    keys=set(r1.keys()).union(set(r2.keys()))
    l1={}
    for key in keys:
        l1[key]=r1.get(key,0)+r2.get(key,0)
    l2=dict(sorted(l1.items(),key=lambda x:x[1],reverse=True))
    l2_keys=list(l2.keys())
    total_result=vector_result+bm25_result
    l3 = []
    for i in l2_keys:
        for j in total_result:
            if i == j.id and j not in l3:
                l3.append(j)
    return l3

if __name__ == '__main__':
    print(rrf(d1, d2))
