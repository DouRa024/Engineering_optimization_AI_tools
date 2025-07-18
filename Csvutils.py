import streamlit as st
import pandas as pd
import json
import re
from langchain_openai import ChatOpenAI
import os
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
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        temperature=0
    )
    sample_data = df.head(50).to_json(orient="records", force_ascii=False)  # 取前5行
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