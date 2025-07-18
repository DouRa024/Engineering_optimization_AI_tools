import os
import memory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template="""
    你是智能AI助手。
    对话历史:
    {history}
    用户输入:
    {input}
    请给出回复：
    """
)
def get_Chat_respnse(prompt, memory, creativity, api_key):
    model = ChatOpenAI(
        api_key=api_key,
        temperature=creativity,
        model_name="deepseek-chat",
        base_url="https://api.deepseek.com/v1",
    )
    chain = ConversationChain(llm=model, memory=memory, prompt=prompt_template)

    response = chain.invoke({'input': prompt})
    return response['response']