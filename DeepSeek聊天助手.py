import datetime
import os
import streamlit as st
from langchain.memory import ConversationBufferMemory
from DSutils import get_Chat_respnse
from theme_manager import apply_theme  # 确保 theme_manager.py 中有 apply_theme 函数

apply_theme()  # 第一件事，注入当前主题CSS
st.set_page_config(
    page_title="DeepSeek智能聊天助手",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💬DeepSeek智能聊天助手")
api_key = os.getenv("DEEPSEEK_API_KEY")

if 'chat_memory' not in st.session_state:
    st.session_state["chat_memory"] = ConversationBufferMemory(chat_memory_key="history", return_messages=True)

    st.session_state["chat_messages"] = [{'role': 'ai', 'content': '我是你的智能AI助手，你可以向我提问任何问题'}]
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []
for message in st.session_state["chat_messages"]:
    st.chat_message(message['role']).write(message['content'])
creativity = st.slider("✨ 请输入聊天助手的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
prompt = st.chat_input()
if prompt:
    if not api_key:
        st.info('api密钥呢')
        st.stop()
    st.session_state["chat_messages"].append({'role': 'human', 'content': prompt})
    st.chat_message('human').write(prompt)

    with st.spinner('请稍等，我需要思考'):
        response = get_Chat_respnse(prompt, st.session_state["chat_memory"], creativity,api_key)

    msg = {'role': 'ai', 'content': response}
    st.session_state["chat_messages"].append(msg)
    st.chat_message('ai').write(response)
st.markdown("""
        <style>
        .footer {
            text-align: center;
            font-size: 12px;
            color: #888888;
            margin-top: 40px;
            padding-bottom: 20px;
        }
        </style>
        <div class="footer">
            © 2025 工程过程增效 AI 工具 | Powered by DeepSeek API | Developed by Luke Yang
        </div>
    """, unsafe_allow_html=True)
with st.sidebar:
    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        width: 350px !important;
        min-width: 350px !important;
        max-width: 350px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if "theme" not in st.session_state:
        st.session_state.theme = "🌞明亮模式"

    selected_theme = st.selectbox("🎨 主题切换", ["🌞明亮模式", "🌚暗黑模式"],
                                  index=["🌞明亮模式", "🌚暗黑模式"].index(st.session_state.theme))
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.markdown("#### 用户信息")
    if "username" not in st.session_state:
        st.session_state.username = "登山者"

    user_input = st.text_input("👤 用户名", value=st.session_state.username, key="username_input")
    st.session_state.username = user_input

    st.markdown(f"""
    <div style='margin-top: -10px; margin-bottom: 15px; font-size: 16px;'>
        👋 欢迎回来，<b>{st.session_state.username}</b>！
    </div>
    """, unsafe_allow_html=True)

    now = datetime.datetime.now()
    st.markdown(f"<div style='color: gray;'>🕙 今天是：{now.strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🛠️ 帮助与支持")
    st.markdown("[📚 使用文档](https://api-docs.deepseek.com/)")
    st.markdown("[📈 账号流量](https://platform.deepseek.com/usage)")
    st.markdown("[💬 微信公众号](https://mp.weixin.qq.com/s/49K4_GBv9Eu9Pfr0lWadQw)")
    st.markdown("---")

    is_dark = st.session_state.theme == "🌚暗黑模式"
    title_color = "#FFFFFF" if is_dark else "#000000"
    subtitle_color = "#AAAAAA" if is_dark else "#999999"
    st.image("图片.png", use_container_width=True)

    import base64

    with open("static/logo_font.ttf", "rb") as f:
        font_data = f.read()

    font_base64 = base64.b64encode(font_data).decode()
    st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'logo_font';
        src: url(data:font/truetype;charset=utf-8;base64,{font_base64}) format('truetype');
    }}
    .custom-title {{
        font-family: 'logo_font';
        font-size: 18px;
        font-weight:regular;
        color: {title_color};
        text-align: center;
        letter-spacing: 3px;
        margin-top: 20px;
        margin-bottom: 0px;
    }}
    </style>

    <div class="custom-title">
        工程过程增效AI工具
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""

    <div style='text-align: center; color: {subtitle_color}; font-size: 12px; margin-bottom: 0px;'>
        Based on DeepSeek | Version V-0.1
    </div>
    """, unsafe_allow_html=True)