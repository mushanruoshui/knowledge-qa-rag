# src/splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """
    将文档列表切分成小块

    参数:
        documents: list of dict, 格式 [{"content": str, "source": str}, ...]
        chunk_size: 每个块的最大字符数
        chunk_overlap: 块之间的重叠字符数

    返回:
        list of dict, 每个块包含 {"content": str, "source": str, "chunk_id": int}
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
        length_function=len,
    )

    chunks = []
    for doc in documents:
        # 将单个文档切分成多个文本块
        split_texts = text_splitter.split_text(doc["content"])

        for i, text in enumerate(split_texts):
            # 过滤掉空字符串或只有空白字符的块
            if text.strip():
                chunks.append({
                    "content": text,
                    "source": doc["source"],
                    "chunk_id": i,
                })

    print(f"原始文档数: {len(documents)}, 切分后块数: {len(chunks)}")
    return chunks

if __name__ == "__main__":
    from loader import load_documents

    docs = load_documents()
    chunks = split_documents(docs)

    print("\n--- 示例块（第一个块）---")
    if chunks:
        print(f"来源: {chunks[0]['source']}")
        print(f"块ID: {chunks[0]['chunk_id']}")
        print(f"内容: {chunks[0]['content'][:200]}...")