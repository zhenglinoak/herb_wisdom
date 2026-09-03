from ai import LoadReRankerModel

def reranker(doc):
    q=doc['question']
    h=doc['history']
    c=[i.page_content for i in doc['context']]
    print(doc['context'])
    merge=[(q,i) for i in c]
    reranker_model=LoadReRankerModel.load_rerank_model()
    scores=reranker_model.compute_score(merge)
    r1=list(zip(scores,doc['context']))
    r2=sorted(r1,key=lambda x:x[0],reverse=True)
    r3=[i[1] for i in r2][:4]

    return {
        "context":r3,
        "history":h,
        "question":q,
    }