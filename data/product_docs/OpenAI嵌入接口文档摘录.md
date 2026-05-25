# OpenAI Embeddings API 文档摘录

## 接口说明

`POST https://api.openai.com/v1/embeddings`

该接口用于将输入文本转换为向量表示（Embedding），可用于语义搜索、文本聚类、相似度计算等下游任务。

## 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| model | string | 必填，模型名称，如 `text-embedding-3-small` |
| input | string / array | 必填，待编码的文本或文本数组 |
| dimensions | integer | 可选，指定输出向量的维度（仅部分模型支持） |

## 示例请求

```json
{
  "input": "The food was delicious and the waiter...",
  "model": "text-embedding-3-small",
  "encoding_format": "float"
}
```

## 返回结构

返回的 `data` 数组中每个元素包含 `embedding`（浮点数数组）、`index`（对应输入顺序）和 `object`（固定值 `"embedding"`）字段。`usage` 字段包含本次请求消耗的 token 数量。

`text-embedding-3-small` 默认输出 1536 维向量，`text-embedding-3-large` 默认输出 3072 维向量。
