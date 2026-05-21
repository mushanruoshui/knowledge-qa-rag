# src/loader.py
import os
from pypdf import PdfReader


def load_documents(data_dir: str = "data"):
    """
    读取 data 目录下的所有 .txt、.pdf、.md、.docx 文件
    返回: list of dict, 每个 dict 包含 {"content": str, "source": str}
    """
    documents = []

    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, data_dir)

            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                documents.append({
                    "content": content,
                    "source": relative_path  # 使用相对路径，保持一致性
                })
                print(f"✓ 已加载: {relative_path}")

            elif filename.endswith(".pdf"):
                try:
                    reader = PdfReader(filepath)
                    text_pages = []
                    for page_num, page in enumerate(reader.pages, 1):
                        try:
                            text = page.extract_text()
                            if text:
                                text_pages.append(text)
                            else:
                                print(f"  警告: {filename} 第{page_num}页无文字（可能是扫描件）")
                        except Exception as e:
                            print(f"  警告: {filename} 第{page_num}页解析失败: {e}")
                    content = "\n".join(text_pages)
                    if not content.strip():
                        print(f"  警告: {filename} 没有提取到有效文字，已跳过")
                        continue

                    documents.append({
                        "content": content,
                        "source": relative_path
                    })
                    print(f"✓ 已加载: {relative_path}")

                except Exception as e:
                    print(f"  错误: 无法读取 {filename}: {e}")
                    continue

            elif filename.endswith(".md"):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    documents.append({
                        "content": content,
                        "source": relative_path
                    })
                    print(f"✓ 已加载: {relative_path}")

                except Exception as e:
                    print(f"  错误: 无法读取 {filename}: {e}")
                    continue

            elif filename.endswith(".docx"):
                try:
                    from docx import Document
                    doc = Document(filepath)
                    content = "\n".join([para.text for para in doc.paragraphs])

                    documents.append({
                        "content": content,
                        "source": relative_path
                    })
                    print(f"✓ 已加载: {relative_path}")

                except ImportError:
                    print(f"  错误: 需要安装 python-docx 来读取 {filename}")
                    print(f"  请运行: pip install python-docx")
                    continue
                except Exception as e:
                    print(f"  错误: 无法读取 {filename}: {e}")
                    continue

    print(f"共加载 {len(documents)} 个文档")
    return documents