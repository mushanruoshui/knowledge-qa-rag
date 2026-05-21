# src/chain.py
import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

load_dotenv()

client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))


def build_prompt(query, context_chunks):
    context = "\n\n---\n\n".join([chunk["content"] for chunk in context_chunks])

    prompt = f"""你是一个专业的助手，请根据以下参考资料回答用户的问题。

【参考资料】
{context}

【用户问题】
{query}

【回答要求】
- 如果参考资料中有相关信息，请基于这些信息回答
- 如果参考资料中没有相关信息，请明确告知用户"知识库中没有找到相关信息"
- 回答要简洁、准确

【你的回答】"""

    return prompt


def generate_answer(query, context_chunks):
    prompt = build_prompt(query, context_chunks)

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content


def rag_query(query, vectorstore, k=3):
    """返回 (answer, chunks) 元组，供 Web 界面使用"""
    from .retriever import retrieve_relevant_chunks

    chunks = retrieve_relevant_chunks(vectorstore, query, k)

    if not chunks:
        return "未检索到相关文档片段", []

    answer = generate_answer(query, chunks)
    return answer, chunks