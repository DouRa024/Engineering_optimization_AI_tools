import streamlit as st
import os
import requests
import datetime
from theme_manager import apply_theme
apply_theme()
import streamlit as st
import os
import requests
from datetime import datetime
from theme_manager import apply_theme



API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/beta/v1/chat/completions"

st.set_page_config(page_title="工程项目内容生成器", page_icon="🛠️",layout="wide")
st.title("🛠️ 工程项目内容生成器")

# 自定义样式，标题左对齐，字体大小统一
st.markdown("""
<style>
    .stTextInput > div > div > input, .stTextArea > div > textarea {
        font-size: 16px;
    }
    .stButton > button {
        font-size: 16px;
    }
    .output-box {
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        white-space: pre-wrap;
        font-size: 16px;
        line-height: 1.5em;
    }
    /* 标题左对齐 */
    .streamlit-expanderHeader, h2 {
        text-align: left !important;
    }
    /* tab内容区域内标题 */
    .css-1v0mbdj h2 {
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)

# 五个模块的输入字段
TABS = {
    "工程项目汇报PPT提纲": [
        ("项目名称", "请输入项目名称"),
        ("项目目标", "该项目旨在……"),
        ("实施时间", "2024年5月至2025年1月"),
        ("技术路线/亮点", "例如：采用BIM+AI……"),
        ("成果与价值", "例如：提升了效率，节省了成本……")
    ],
    "技术方案/可研报告草稿": [
        ("项目名称", "请输入项目名称"),
        ("技术背景", "请输入技术背景"),
        ("主要技术方案", "核心思路与步骤……"),
        ("风险与应对", "如：施工阶段可能遇到的……"),
        ("预期效果", "请输入成果预期")
    ],
    "招标文件条款草拟": [
        ("项目名称", "请输入项目名称"),
        ("采购内容", "请输入采购内容"),
        ("技术/服务要求", "例如：须满足XXX标准"),
        ("合同条款关键点", "例如：付款节点、验收标准"),
        ("投标人资质要求", "请输入资质条件")
    ],
    "项目总结/周报月报": [
        ("项目名称", "请输入项目名称"),
        ("时间范围", "例如：2025年6月"),
        ("关键进展", "例如：完成结构施工"),
        ("存在问题及改进", "请输入问题与对策"),
        ("下阶段计划", "请输入计划")
    ],
    "工程术语浅化": [
        ("术语/段落", "请输入复杂术语或技术段落"),
        ("目标对象", "如：普通公众、学生、非专业领导")
    ]
}

# 对应的 prompt 模板，代码里隐藏，用户看不到
PROMPT_TEMPLATES = {
    "工程项目汇报PPT提纲": """请根据以下信息生成“工程项目汇报PPT提纲”，
要求内容结构清晰、条理分明、逻辑合理：

项目名称：{项目名称}
项目目标：{项目目标}
实施时间：{实施时间}
技术路线/亮点：{技术路线_亮点}
成果与价值：{成果与价值}

请基于上述内容生成完整PPT提纲，包含章节和主要内容要点。
""",
    "技术方案/可研报告草稿": """请根据以下信息生成“技术方案/可研报告草稿”，
内容要求详实，结构合理，突出关键技术与风险管控：

项目名称：{项目名称}
技术背景：{技术背景}
主要技术方案：{主要技术方案}
风险与应对：{风险与应对}
预期效果：{预期效果}

请完整撰写草稿内容。
""",
    "招标文件条款草拟": """请根据以下信息起草“招标文件条款”，
重点突出采购要求、技术标准和合同关键条款：

项目名称：{项目名称}
采购内容：{采购内容}
技术/服务要求：{技术_服务要求}
合同条款关键点：{合同条款关键点}
投标人资质要求：{投标人资质要求}

请形成条款草案，条理清晰，表达规范。
""",
    "项目总结/周报月报": """请根据以下信息撰写“项目总结/周报月报”，
内容涵盖进展、问题及下一步计划：

项目名称：{项目名称}
时间范围：{时间范围}
关键进展：{关键进展}
存在问题及改进：{存在问题及改进}
下阶段计划：{下阶段计划}

请形成总结报告，条理明晰，语言简洁。
""",
    "工程术语浅化": """请根据以下信息将复杂的工程术语或技术段落浅显化，
以便目标对象理解：

术语/段落：{术语_段落}
目标对象：{目标对象}

请用通俗易懂的语言解释。
"""
}

# 初始化历史记录，确保是字典，且每个tab下是列表，避免索引错误
if 'history' not in st.session_state or not isinstance(st.session_state['history'], dict):
    st.session_state['history'] = {k: [] for k in TABS.keys()}
for tab_key in TABS.keys():
    if tab_key not in st.session_state['history'] or not isinstance(st.session_state['history'][tab_key], list):
        st.session_state['history'][tab_key] = []

tabs = st.tabs(list(TABS.keys()))

for i, tab_name in enumerate(TABS.keys()):
    with tabs[i]:
        st.header(f"{tab_name}")
        st.info("📌 推荐填写详细信息；如时间紧可粘贴整体描述。若两者都填写，优先使用详细填空。")

        with st.expander("✍️ 点击即可使用详细填空，将会给你更加结构化的输出", expanded=False):
            inputs = {}
            for label, placeholder in TABS[tab_name]:
                key_name = label.replace("/", "_").replace(" ", "_")
                if any(keyword in label for keyword in ["段落", "背景", "亮点", "方案", "问题"]):
                    value = st.text_area(label, placeholder=placeholder, key=f"{tab_name}_{key_name}")
                else:
                    value = st.text_input(label, placeholder=placeholder, key=f"{tab_name}_{key_name}")
                inputs[key_name] = value

        st.markdown("<p style='margin-top:15px;'>🔁 如果不想逐项填写，可将已有内容直接粘贴至下方：</p>", unsafe_allow_html=True)
        free_text = st.text_area(f"📋 粘贴项目相关描述（可选）", height=200,
                                placeholder="例如：本项目为XXX，旨在解决XXX问题……", key=f"{tab_name}_free_text")

        if st.button(f"🚀 生成内容", key=f"{tab_name}_generate"):
            # 构造 prompt
            if any(v.strip() for v in inputs.values()):
                try:
                    final_prompt = PROMPT_TEMPLATES[tab_name].format(**inputs)
                except KeyError as e:
                    st.error(f"模板占位符替换错误，缺少字段: {e}")
                    continue
            elif free_text.strip():
                final_prompt = f"请根据以下描述内容生成“{tab_name}”内容，要求内容结构清晰、条理分明、逻辑合理：\n{free_text.strip()}"
            else:
                st.warning("⚠️ 请至少填写一项或粘贴文本")
                continue

            with st.spinner("⏳ 正在分析，请稍后..."):
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                }
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是资深工程项目专家，擅长撰写项目材料。"},
                        {"role": "user", "content": final_prompt}
                    ],
                    "temperature": 0.7
                }

                try:
                    response = requests.post(API_URL, headers=headers, json=payload)
                    response.raise_for_status()
                    result = response.json()["choices"][0]["message"]["content"]

                    st.markdown("### 🎯 生成内容：")
                    st.markdown(f"<div class='output-box'>{result.replace(chr(10), '<br>')}</div>",
                                unsafe_allow_html=True)

                    # 保存历史
                    st.session_state['history'][tab_name].insert(0, {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "output": result
                    })

                except Exception as e:
                    st.error(f"❌ 生成失败：{e}")

        # 展示历史记录
        with st.expander("📜 历史记录", expanded=False):
            hist = st.session_state['history'][tab_name]
            if not hist:
                st.write("暂无历史记录")
            for item in hist:
                st.markdown(f"**[{item['time']}]**")
                st.markdown(item['output'])
                st.markdown("---")

with st.sidebar:
    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        width: 350px !important;
        min-width: 150px !important;
        max-width: 550px !important;
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

    st.markdown("## 🛠️ 帮助与支持")
    st.markdown("[📚 使用文档](https://api-docs.deepseek.com/)")
    st.markdown("[📈 账号流量](https://platform.deepseek.com/usage)")
    st.markdown("[💬 微信公众号](https://mp.weixin.qq.com/s/49K4_GBv9Eu9Pfr0lWadQw)")
    now = datetime.now()
    st.markdown(
        f"<div style='color: gray;margin-top: -0px; margin-bottom: -805px;'>🕙 今天是：{now.strftime('%Y-%m-%d')}</div>",
        unsafe_allow_html=True)
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
        margin-top: -5px;
        margin-bottom: -25px;
    }}
    </style>

    <div class="custom-title">
        工程过程增效AI工具
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""

    <div style='text-align: center; color: {subtitle_color}; font-size: 12px; margin-bottom: -40px;'>
        Based on DeepSeek | Version V-0.1
    </div>
    """, unsafe_allow_html=True)