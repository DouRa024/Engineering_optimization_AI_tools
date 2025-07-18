import nltk
nltk.download('punkt')
import nltk
nltk.download('punkt_tab')

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import os
import logging
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredFileLoader,
    UnstructuredPowerPointLoader
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalEmbedding(Embeddings):
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()


def qa_agent(api_key, memory, uploaded_file, question, prompt=None):
    temp_file_path = None
    try:
        model = ChatOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0
        )

        # 保存上传文件到临时文件
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()
        temp_file_path = f"temp{file_ext}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        # 根据扩展名选择加载器
        if file_ext == ".pdf":
            loader = PyPDFLoader(temp_file_path)
        elif file_ext in [".docx", ".doc", ".xls", ".xlsx"]:
            loader = UnstructuredFileLoader(temp_file_path)
        elif file_ext in [".ppt", ".pptx"]:
            loader = UnstructuredPowerPointLoader(temp_file_path)
        elif file_ext == ".txt":
            loader = TextLoader(temp_file_path, encoding="utf-8")
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")

        docs = loader.load()

        # 文本切分
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "。", "！", "？", "，", "、", " "]
        )
        texts = splitter.split_documents(docs)

        # 本地向量模型
        sentence_model = SentenceTransformer("./text2vec-base-local")
        embeddings = LocalEmbedding(sentence_model)

        # 建立向量库
        vector_db = FAISS.from_documents(texts, embeddings)
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})

        # 拼接问题+prompt
        full_question = f"{prompt}\n\n问题是：{question}" if prompt else question

        # 创建对话检索链
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=model,
            retriever=retriever,
            memory=memory,
            return_source_documents=False,
            output_key="answer"
        )

        result = qa_chain({"question": full_question})

        return result

    except Exception as e:
        logger.error(f"QA Agent 运行错误: {e}")
        return {"answer": f"出错了: {e}"}

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
import streamlit as st
import pandas as pd
import json
import re
from langchain_openai import ChatOpenAI

PROMPT_TEMPLATE = """
你是一位数据分析助手，根据给定的数据回答问题。

数据示例（前5行）：
{sample_data}

请只用以下 JSON 格式回复：
- 文字回答：{{"answer": "<你的回答>"}}
- 表格回答：{{"table": {{"columns": [...], "data": [[...], ...]}}}}
- 条形图：{{"bar": {{"columns": [...], "data": [...]}}}}
- 折线图：{{"line": {{"columns": [...], "data": [...]}}}}
- 散点图：{{"scatter": {{"columns": [...], "data": [...]}}}}

问题是：
{query}
"""


def extract_json(text):
    pattern = r'(\{.*\})'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def dataframe_agent(api_key, df, query):
    model = ChatOpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        temperature=0
    )
    sample_data = df.head(50).to_json(orient="records", force_ascii=False)  # 取前50行
    prompt = PROMPT_TEMPLATE.format(sample_data=sample_data, query=query)
    response = model.call_as_llm(prompt)

    json_text = extract_json(response)
    if json_text:
        try:
            response_dict = json.loads(json_text)
        except Exception:
            response_dict = {"answer": response}
    else:
        response_dict = {"answer": response}
    return response_dict
