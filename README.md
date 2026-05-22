# 📚 个人知识库问答助手

基于 RAG（检索增强生成）技术的个人知识库问答系统。

## 功能特点

- 支持多种文档格式：.txt, .pdf, .md, .docx
- 本地向量存储（Chroma）
- 使用智谱 AI 的 Embedding 和 GLM 模型
- 提供命令行和 Web 两种交互界面

## 技术栈

- LangChain：文档切分和流程编排
- Chroma：本地向量数据库
- 智谱 AI：Embedding + GLM-4 大模型
- Streamlit：Web 界面

## 模型下载
- 本项目使用 BAAI/bge-reranker-v2-m3 重排模型的本地部署版本
- 由于模型文件较大，请手动下载后放入 `./models/` 目录：
- 推荐访问官方网站进行下载:https://huggingface.co/BAAI/bge-reranker-v2-m3