import shutil
import os
from src.loader import load_documents
from src.splitter import split_documents
from src.vectorstore import create_vectorstore

def main():
    print("=" * 50)
    print("开始构建知识库索引...")
    print("=" * 50)

    # 可选：清空旧的向量库（完全重建）
    persist_dir = "./chroma_db"
    if os.path.exists(persist_dir):
        print(f"\n检测到旧向量库，正在清空...")
        shutil.rmtree(persist_dir)
    # 1. 加载文档
    print("\n[1/3] 加载文档...")
    docs = load_documents()

    if not docs:
        print("错误: data目录下没有找到txt或pdf文件")
        return

    # 2. 切分文档
    print("\n[2/3] 切分文档...")
    chunks = split_documents(docs, chunk_size=500, chunk_overlap=50)

    if not chunks:
        print("错误: 切分后没有有效内容")
        return

    print("\n[3/3] 向量化并存储...")
    vectorstore = create_vectorstore(chunks)

    print("\n" + "=" * 50)
    print("✓ 索引构建完成！")
    print(f"  文档数: {len(docs)}")
    print(f"  切分块数: {len(chunks)}")
    print(f"  存储位置: ./chroma_db")
    print("=" * 50)


if __name__ == "__main__":
    main()