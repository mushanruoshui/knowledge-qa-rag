# src/vectorstore.py
import os
from dotenv import load_dotenv
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_chroma import Chroma  # 改用新的包

load_dotenv()


def get_embeddings():
    """获取智谱AI的Embedding模型"""
    return ZhipuAIEmbeddings(
        model="embedding-3",
        api_key=os.getenv("ZHIPU_API_KEY"),
    )


def create_vectorstore(chunks, persist_directory="./chroma_db"):
    """将切分好的文档块向量化并存入Chroma"""
    texts = [chunk["content"] for chunk in chunks]
    metadatas = [
        {"source": chunk["source"], "chunk_id": chunk["chunk_id"]}
        for chunk in chunks
    ]

    embeddings = get_embeddings()

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=persist_directory,
    )

    print(f"✓ 向量库已创建，共 {len(texts)} 个向量，保存在 {persist_directory}")
    return vectorstore


def load_vectorstore(persist_directory="./chroma_db"):
    """从磁盘加载已有的向量库"""
    embeddings = get_embeddings()
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
    print(f"✓ 向量库已加载：{persist_directory}")
    return vectorstore