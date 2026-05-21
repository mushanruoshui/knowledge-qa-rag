from .vectorstore import load_vectorstore

def retrieve_relevant_chunks(vectorstore, query, k=3,verbose=False):
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

    chunks = []
    for doc in results:
        chunks.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
        })

    if verbose:
        print(chunks)

    print(f"检索到 {len(chunks)} 个相关片段")
    return chunks
