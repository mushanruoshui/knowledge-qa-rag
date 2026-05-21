# main.py - 命令行问答界面
from src.vectorstore import load_vectorstore
from src.chain import rag_query


def main():
    print("=" * 50)
    print("个人知识库问答助手")
    print("=" * 50)

    # 加载向量库
    print("\n正在加载向量库...")
    try:
        vectorstore = load_vectorstore()
    except Exception as e:
        print(f"加载失败: {e}")
        print("请先运行 index.py 构建向量库")
        return

    print("知识库已就绪！输入问题开始问答（输入 q 退出）\n")

    while True:
        query = input("\n🤔 你: ").strip()

        if query.lower() in ["q", "quit", "exit"]:
            print("再见！")
            break

        if not query:
            print("请输入问题")
            continue

        # 执行 RAG 问答
        rag_query(query, vectorstore, k=5)


if __name__ == "__main__":
    main()