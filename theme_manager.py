# theme_manager.py

import streamlit as st
def apply_theme():
    theme = st.session_state.get("theme", "🌞明亮模式")

    if theme == "🌚暗黑模式":
        st.markdown("""
        <style>
            /* 全局背景和字体 */
            body, .stApp {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
            }

            /* 侧边栏背景和字体 */
            section[data-testid="stSidebar"] {
                background-color: #2E2E2E !important;
                color: #FFFFFF !important;
            }
            section[data-testid="stSidebar"] * {
                color: #FFFFFF !important;
            }

            /* 输入框样式 */
            .stTextInput > div > div > input {
                background-color: #444444 !important;
                color: #FFFFFF !important;
                border: 1px solid #888888 !important;
            }

            /* 选择框样式 */
            .stSelectbox > div > div {
                background-color: #444444 !important;
                color: #FFFFFF !important;
                border: 1px solid #888888 !important;
            }
            /* 自定义字体标题在暗黑模式下变白 */
            .custom-title1 {
                color: #FFFFFF !important;
            }
            /* slider 标签和数值文字 */
            label, div[data-baseweb="slider"] {
                color: #FFFFFF !important;
            }

            /* Markdown 文本 */
            .stMarkdown {
                color: #FFFFFF !important;
            }

            /* info-text 区块特殊处理，保证文字黑色 */
            .info-text {
                background-color: #e6f4ff !important;
                border-left: 6px solid #1e90ff !important;
                border-radius: 6px !important;
                padding: 12px 16px !important;
                width: 660px !important;
                margin-bottom: 20px !important;
            }
            .info-text span {
                color: #000000 !important;
                font-size: 15px !important;
                text-align: center !important;
            }

            /* 所有按钮文字颜色 */
            button, button > div, button > span {
                color: #eeeeee !important;
                font-weight: 600 !important;
            }
            
            /* 按钮背景 */
            button {
                background-color: #333333 !important;
                border: 1px solid #555555 !important;
                border-radius: 6px !important;
            }
            
            /* 鼠标悬浮时按钮背景变亮 */
            button:hover {
                background-color: #555555 !important;
                color: #ffffff !important;
}

            /* 新增：tab 标题文字颜色 */
            div[data-testid="stTabs"] button[role="tab"] {
                color: #eee !important;
            }

            /* 新增：选中tab背景和文字加粗 */
            div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
                background-color: #444 !important;
                color: #fff !important;
                font-weight: 600;
            }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
            /* 明亮模式可按需自定义，或者留空用默认 */
        </style>
        """, unsafe_allow_html=True)
