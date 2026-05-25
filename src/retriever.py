from .vectorstore import load_vectorstore
from sentence_transformers import CrossEncoder

_reranker = None

def get_reranker():
    """
    懒加载重排模型
    """
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder('E:\project_code\knowledge_qa\model', max_length=512)
    return _reranker

def retrieve_relevant_chunks(vectorstore, query, k=3,verbose=False,use_reranker=True):
    """
    检索与问题最相关的 k 个文档块

    参数:
        vectorstore: Chroma 向量库对象
        query: 用户问题
        k: 返回的文档块数量
    返回:
        list of dict, 包含 content 和 metadata
    """
    results = vectorstore.similarity_search(query, k=k)

    if not use_reranker:
        results = vectorstore.similarity_search(query,k=k)
        chunks = [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
        print(f"向量检索（无重排）返回 {len(chunks)} 个片段")
        return chunks

    k_candidate = min(10, vectorstore._collection.count())
    results = vectorstore.similarity_search(query, k=k_candidate)

    if not results:
        return []

    # 第二步：准备重排输入 [(query, doc), ...]
    pairs = [(query, doc.page_content) for doc in results]

    # 第三步：用Cross-Encoder打分
    reranker = get_reranker()
    scores = reranker.predict(pairs)  # 返回每个pair的相关性分数

    # 第四步：按分数排序，取top-k
    scored_results = list(zip(results, scores))

    scored_results.sort(key=lambda x: x[1], reverse=True)  # 按分数降序
    top_results = scored_results[:k]

    # 第五步：格式化返回
    chunks = []
    for doc, score in top_results:
        chunks.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "rerank_score": float(score)  # 可选，方便调试
        })

    if verbose:
        print(f"\n重排后Top-{k}结果（分数越高越相关）：")
        for i, chunk in enumerate(chunks):
            print(f"{i + 1}. 分数={chunk['rerank_score']:.4f} | {chunk['content'][:80]}...")

    print(f"向量检索召回 {len(results)} 个候选 → 重排后返回 {len(chunks)} 个片段")
    return chunks
