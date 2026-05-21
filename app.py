# app.py - Streamlit Web 界面
import streamlit as st
from src.vectorstore import load_vectorstore
from src.chain import rag_query

# 页面配置
st.set_page_config(
    page_title="个人知识库问答助手",
    page_icon="📚",
    layout="wide"
)

# 标题
st.title("📚 个人知识库问答助手")
st.markdown("基于 RAG（检索增强生成）技术，回答你文档中的问题")

# 初始化 session state（缓存向量库，避免每次提问都重新加载）
if "vectorstore" not in st.session_state:
    with st.spinner("正在加载知识库..."):
        try:
            st.session_state.vectorstore = load_vectorstore()
            st.success("✅ 知识库加载成功！")
        except Exception as e:
            st.error(f"❌ 知识库加载失败: {e}")
            st.info("请先运行 `python index.py` 构建向量库")
            st.stop()

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")
    k_value = st.slider(
        "检索文档块数量 (k)",
        min_value=1,
        max_value=10,
        value=3,
        help="数值越大，检索到的上下文越多，但可能引入噪音"
    )

    st.header("ℹ️ 使用说明")
    st.markdown("""
    1. 在下方输入问题
    2. 系统会从知识库中检索相关内容
    3. AI 基于检索结果生成答案

    **知识库文件位置**: `data/` 文件夹

    **支持格式**: .txt, .pdf, .md, .docx
    """)

    st.header("📊 知识库状态")
    st.info(f"当前检索参数: k = {k_value}")

# 主界面 - 聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "chunks" in message and message["chunks"]:
            with st.expander("📄 查看检索到的相关片段"):
                for i, chunk in enumerate(message["chunks"]):
                    st.markdown(f"**片段 {i + 1}** (来源: `{chunk['metadata']['source']}`)")
                    st.text(chunk["content"][:500] + ("..." if len(chunk["content"]) > 500 else ""))

# 输入框
if prompt := st.chat_input("请输入你的问题..."):
    # 显示用户问题
    with st.chat_message("user"):
        st.markdown(prompt)

    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 生成回答
    with st.chat_message("assistant"):
        with st.spinner("正在检索和生成答案..."):
            try:
                answer, chunks = rag_query(prompt, st.session_state.vectorstore, k=k_value)
                st.markdown(answer)

                # 显示检索片段（可折叠）
                if chunks:
                    with st.expander("📄 查看检索到的相关片段"):
                        for i, chunk in enumerate(chunks):
                            st.markdown(f"**片段 {i + 1}** (来源: `{chunk['metadata']['source']}`)")
                            st.text(chunk["content"][:500] + ("..." if len(chunk["content"]) > 500 else ""))

                # 添加助手消息到历史
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "chunks": chunks
                })
            except Exception as e:
                st.error(f"生成答案时出错: {e}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"抱歉，出错了: {e}",
                    "chunks": []
                })

# 底部清空按钮
with st.sidebar:
    st.divider()
    if st.button("🗑️ 清空对话历史"):
        st.session_state.messages = []
        st.rerun()