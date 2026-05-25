# app.py
import os
os.environ['GRADIO_TEMP_DIR'] = r'E:\project_code\knowledge_qa\gradio_cache'

import gradio as gr
from src.vectorstore import load_vectorstore
from src.retriever import retrieve_relevant_chunks
from src.chain import generate_answer

# 全局加载向量库（只加载一次）
print("正在加载向量库...")
vectorstore = load_vectorstore("./chroma_db")
print("向量库加载完成！")


def rag_query(user_query, k=3):
    """处理用户查询，返回答案和检索到的片段"""
    # 检索
    chunks = retrieve_relevant_chunks(vectorstore, user_query, k=k, use_reranker=True)

    if not chunks:
        return "❌ 未找到相关内容，请尝试其他问题。", ""

    # 生成答案
    answer = generate_answer(user_query, chunks)

    # 格式化检索到的片段
    retrieved_text = ""
    for i, chunk in enumerate(chunks):
        score = chunk.get('rerank_score', 'N/A')
        content_preview = chunk['content'][:300]
        retrieved_text += f"\n【片段 {i + 1}】 (相关性分数: {score})\n{content_preview}...\n{'-' * 50}\n"

    return answer, retrieved_text


# 创建Gradio界面（修复版）
with gr.Blocks(title="RAG智能问答系统") as demo:
    gr.Markdown("""
    # 📚 RAG智能问答系统

    基于**检索增强生成**技术的本地知识库问答系统。

    ### 特性
    - 🔍 向量检索 + BGE重排序
    - 💡 支持TXT、PDF、Markdown、Word文档
    - 🚀 基于智谱AI GLM-4-Flash模型
    """)

    with gr.Row():
        with gr.Column(scale=3):
            question_input = gr.Textbox(
                label="💬 你的问题",
                placeholder="输入你的问题，例如：什么是RAG？",
                lines=2
            )
            k_slider = gr.Slider(
                minimum=1, maximum=10, value=3, step=1,
                label="检索文档块数量 (K值)",
                info="越大可能越全面，但也可能引入噪音"
            )
            submit_btn = gr.Button("🚀 提交问题", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("### 示例问题")
            example_questions = [
                "什么是RAG？",
                "RAG和微调有什么区别？",
                "向量检索的K值怎么选？"
            ]
            # 修复：不使用 _js 参数，改用简单的点击填充
            for q in example_questions:
                btn = gr.Button(q, size="sm")
                btn.click(
                    fn=lambda q=q: q,  # 返回问题文本
                    outputs=question_input  # 直接输出到输入框
                )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ✨ 系统回答")
            answer_output = gr.Textbox(label="", lines=8)
        with gr.Column():
            gr.Markdown("### 📖 检索到的相关内容")
            retrieved_output = gr.Textbox(label="", lines=8)

    submit_btn.click(
        fn=rag_query,
        inputs=[question_input, k_slider],
        outputs=[answer_output, retrieved_output]
    )

    gr.Markdown("""
    ---
    ### 📌 说明
    - 知识库包含：技术博客、FAQ、项目文档等
    - 重排模型：BAAI/bge-reranker-v2-m3
    - 生成模型：智谱AI GLM-4-Flash
    """)

if __name__ == "__main__":
    # 修复：将 theme 参数移到 launch() 中
    demo.launch(share=True, theme=gr.themes.Soft())