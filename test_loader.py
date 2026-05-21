# test_loader.py
from src.loader import load_documents

docs = load_documents()
print(f"共加载 {len(docs)} 个文档")
for doc in docs:
    print(f"来源: {doc['source']}, 内容长度: {len(doc['content'])} 字符")