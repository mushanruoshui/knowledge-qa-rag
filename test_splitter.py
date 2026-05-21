# test_splitter.py
from src.loader import load_documents
from src.splitter import split_documents

if __name__ == "__main__":
    print("测试文档切分功能")

    print("\n加载文档...")
    docs = load_documents()

    if not docs:
        print("❌ 没有找到文档，请检查 data 目录")
        exit(1)

    print(f"\n步骤2: 切分文档...")
    # 2. 切分文档
    chunks = split_documents(docs)

    # 3. 显示结果
    print("\n步骤3: 显示结果...")
    print(f"\n📊 统计信息:")
    print(f"  原始文档数: {len(docs)}")
    print(f"  切分后块数: {len(chunks)}")

    if chunks:
        print(f"\n📄 第一个块示例:")
        print(f"  来源: {chunks[0]['source']}")
        print(f"  块ID: {chunks[0]['chunk_id']}")
        print(f"  内容长度: {len(chunks[0]['content'])} 字符")
        print(f"  内容预览: {chunks[0]['content'][:200]}...")

        # 统计每个文档的块数
        print(f"\n📈 每个文档的切分块数:")
        from collections import Counter

        source_counts = Counter(chunk['source'] for chunk in chunks)
        for source, count in source_counts.items():
            print(f"  {source}: {count} 个块")
    else:
        print("⚠️ 警告: 没有生成任何块！")

    print("\n✅ 测试完成")