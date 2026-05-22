from src.vectorstore import load_vectorstore
from src.retriever import retrieve_relevant_chunks

# 加载已有向量库
vectorstore = load_vectorstore("./chroma_db")

# 测试查询
query = "什么是RAG？"
chunks = retrieve_relevant_chunks(vectorstore, query, k=3, verbose=True, use_reranker=True)

print("\n最终返回的chunks:")
for i, chunk in enumerate(chunks):
    print(f"{i+1}. {chunk['content'][:100]}...")
    if "rerank_score" in chunk:
        print(f"   重排分数: {chunk['rerank_score']:.4f}")