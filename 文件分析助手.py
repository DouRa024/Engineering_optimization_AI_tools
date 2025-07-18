import datetime
import os
from theme_manager import apply_theme  # 确保 theme_manager.py 中有 apply_theme 函数
import streamlit as st
from langchain.memory import ConversationBufferMemory
from Fileutils import qa_agent
apply_theme()  # 注入主题CSS
import time

tab1, tab2 = st.tabs(["📑 文件智能问答", "📊 CSV数据分析"])
with tab1:
    apply_theme()
    st.set_page_config(
        page_title="智能文件分析助手",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("📑文件智能问答")

    api_key = os.getenv("DEEPSEEK_API_KEY")

    # 角色和对应prompt（内容暂空，后续填充）
    roles_prompts = {
        "🗓️ 施工计划员 ": "你是一位经验丰富的施工计划工程师，擅长制定施工进度计划，识别关键路径，优化资源配置。请根据上传文件内容，识别施工阶段安排、工期控制风险，并提供合理建议。",
        "🏗️ 结构工程师 ": "你是一位资深结构工程师，精通混凝土、钢结构等结构体系。请根据上传的内容，从结构设计合理性、安全性、施工可行性等方面给出专业解读和建议。",
        "🧠 项目策划师 ": "你是一名专业的项目策划顾问，善于从项目背景、风险、投资收益、周期等维度提出战略性建议。请结合文档内容识别潜在问题并优化方案。",
        "🛠️ 设备运维专家 ": "你是一名设备管理与维护专家，熟悉各类工程设备运维策略。请结合上传文档，从保养周期、故障预警、数字化运维等方面提出建议。",
        "📐 建筑信息建模师 ": "你是一名BIM建模专家，擅长使用Revit、Navisworks等软件进行构件建模、模型校审、管综优化。请依据文档内容识别建模需求、查找冲突、评估模型质量，并提出优化建议。",
        "📋 造价工程师 ": "你是一位经验丰富的造价工程师，擅长识别清单项目、编制预算、分析价格构成。请结合文档内容回答与成本估算、计价规范、材料价格、工程量等相关的问题。",
        "🔎 投标专员 ":  "你是一位经验丰富的投标专员，擅长解读招标文件、准备投标文件、编制商务标和技术标，并确保合规性和竞争力。请根据文件内容和用户提问，提供清晰、专业的招标策略建议。",
        "📊 招标专员 ": "你是一位招投标领域专家，请根据用户上传的材料，识别适合的招标方式、关键条款、评分标准，并提供改进建议或模板参考。",
        "🚧 安全工程师 ": "你是一位工程项目的安全工程师，擅长识别施工过程中的安全风险、制定应急预案、审核专项方案。请根据用户提供的内容，指出存在的隐患并给出防控建议。",
        "🔬 质量管理专员 ": "你是一位负责施工质量管理的工程师，请根据文档内容分析施工工艺、验收标准、检验批次，指出可能影响质量的问题，并提出整改建议。",
        "🛰️ 智慧工地运营官 ": "你是智慧工地领域的专家，擅长部署传感器、数据看板、AI识别等技术。请结合用户材料提出数字化升级方案或分析智慧工地运行效果。",
        "🏗️ 建筑设计师 ": "你是一位专业的建筑设计师，擅长空间布局、立面设计、建筑美学及规范审查。请根据用户上传的设计说明或图纸，为建筑方案合理性、美观性及规范性提出专业建议。",
        "🧱 结构设计工程师 ": "你是一名结构设计工程师，精通钢筋混凝土、钢结构、装配式结构等设计规范，擅长结构计算与施工图纸审查。请根据用户提供的文档内容，分析结构设计是否合理、是否满足承载力与安全要求。",
        "🔌 机电设计工程师 ": "你是一位机电设计工程师，熟悉电气、给排水、暖通等专业设计规范，擅长协调建筑与设备空间布置。请根据文档内容，为机电系统设计提供技术支持与优化建议。",
        "🧯 消防设计专员 ": "你是一位消防系统设计人员，精通消防规范与布置原则，擅长分析喷淋系统、火灾报警系统及疏散设计的合理性。请根据文件内容判断设计是否满足国家与地方消防规范。",
        "🖼️ 室内设计师 ": "你是一名室内设计师，擅长空间氛围营造、材质搭配与人体工程学应用。请根据提供的平面布置或设计说明，为室内功能分区、美学与实用性提供建议。",
        "🌳 景观设计师 ": "你是一位景观设计师，擅长户外空间设计、绿化配置与环境融合。请根据设计文本或总平面图内容，为景观构思的实用性与美观性提供意见。",
        "🧊 暖通空调设计工程师 ": "你是一位暖通设计专家，精通通风系统、冷热源设计与负荷计算。请根据项目文档评估系统是否满足舒适性、节能与规范要求。",
        "📡 弱电/智能化设计师 ": "你是一名弱电智能化设计工程师，熟悉综合布线、安防、楼宇自动化等子系统。请根据设计文件评估系统集成性、合理性与未来扩展性。",
        "🙋‍♂️ 默认问答 ": None  # 这个角色用原来方式调用，不传prompt
    }

    if 'role_select_2' not in st.session_state:
        st.session_state.role_select_2 = list(roles_prompts.keys())[0]
    if 'role_switching_2' not in st.session_state:
        st.session_state.role_switching_2 = False
    if 'role_switch_info_2' not in st.session_state:
        st.session_state.role_switch_info_2 = ""


    def on_role_change_2():
        st.session_state.role_switching_2 = True
        st.session_state.role_select_2 = st.session_state.role_temp_2
        st.session_state.role_switch_info_2 = ""


    selected_role_2 = st.selectbox(
        "👥 选择你的角色",
        options=list(roles_prompts.keys()),
        index=list(roles_prompts.keys()).index(st.session_state.role_select_2),
        key="role_temp_2",
        on_change=on_role_change_2,
    )

    if st.session_state.role_switching_2:
        with st.spinner("⏳ 正在切换角色，请稍候..."):
            time.sleep(1.2)
        st.session_state.role_switching_2 = False
        st.session_state.role_switch_info_2 = f'✅ 已成功切换角色“{st.session_state.role_select_2}”'

    if st.session_state.role_switch_info_2:
        st.info(st.session_state.role_switch_info_2)

    # 初始化会话状态
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key='chat_history',  # 一定要是这个
            output_key='answer'
        )
    if 'chat_history' not in st.session_state:
        st.session_state["chat_history"] = []

    # **界面布局：上传框和输入框左右分栏，比例1:1**
    col1, col2 = st.columns(2)

    with col1:
        # 注入自定义样式
        st.markdown(
            """
            <style>
            .custom-uploader section {
                border: 2px dashed #aaa;
                padding: 20px;
                border-radius: 12px;
                background-color: #f9f9f9;
                transition: background-color 0.3s ease;
            }
            .custom-uploader section:hover {
                background-color: #f1f1f1;
            }
            .custom-uploader label {
                font-weight: bold;
                font-size: 16px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # 包裹上传器并美化
        st.markdown('<div class="custom-uploader">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "📂 请上传文件（支持 Word、Excel、PPT、PDF、TXT 格式）：",
            type=["pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "txt"],
            help="支持多种办公文档格式"
        )

        if uploaded_file:
            st.success(
                f"✅ 文件已上传: **{uploaded_file.name}**",
                icon="📄"
            )
        else:
            st.info("请先上传文件，才能提问哦~", icon="ℹ️")


    with col2:
        with st.form(key="question_form"):
            st.markdown("##### ❓ 提问我任何关于文件的问题吧")
            question = st.text_area(
                label="",
                placeholder="请上传文件后输入你的问题…",
                help="输入完问题后，点击下方按钮提交",
                height=100,
            )
            submit_button = st.form_submit_button("📤 提交问题")

    if not uploaded_file and submit_button:
        st.info("请先上传文件，再提问哦")


    def init_session_state():
        if "selected_role" not in st.session_state:
            st.session_state.selected_role = list(roles_prompts.keys())[0]
        # 其他初始化...


    init_session_state()
    if uploaded_file and question and submit_button and api_key:
        with st.spinner("⏳ 请稍后，让我读一下你的文件"):

            prompt_for_role = roles_prompts[st.session_state.selected_role]

            if prompt_for_role is None:
                # 不传 prompt，调用原函数
                response = qa_agent(api_key, st.session_state["memory"], uploaded_file, question)
            else:
                # 传入 prompt
                response = qa_agent(
                    api_key,
                    st.session_state.memory,
                    uploaded_file,
                    question,
                    prompt_for_role
                )

        # 处理响应
        if 'answer' in response:
            answer = response['answer']
        elif 'text' in response:
            answer = response['text']
        elif 'result' in response:
            answer = response['result']
        else:
            st.error(f"❌ 无法获取答案，响应结构: {list(response.keys())}")
            answer = "抱歉，无法获取答案"

        st.markdown('---')
        st.markdown('#### 💡 以下是我的见解：')
        st.write(answer)
        st.markdown('---')

        # 更新聊天历史
        if 'chat_history' in response:
            st.session_state["chat_history"] = response['chat_history']
        else:
            # 这里同步更新 memory 中的对话记录，保持一致即可
            st.session_state.memory.chat_memory.add_user_message(question)
            st.session_state.memory.chat_memory.add_ai_message(response.get('answer', ''))

    # 聊天历史展示，放到独立区域，整洁分割
    if 'chat_history' in st.session_state and st.session_state["chat_history"]:
        with st.expander("🕰️ 点击查看历史记录"):
            for i in range(0, len(st.session_state["chat_history"]), 2):
                human_message = st.session_state["chat_history"][i]
                ai_message = st.session_state["chat_history"][i + 1] if i + 1 < len(st.session_state["chat_history"]) else None

                st.markdown(f"**你:** {human_message.content if hasattr(human_message, 'content') else human_message}")
                if ai_message:
                    st.markdown(f"**AI:** {ai_message.content if hasattr(ai_message, 'content') else ai_message}")

                if i < len(st.session_state["chat_history"]) - 2:
                    st.markdown("---")
with tab2:
    import pandas as pd
    import plotly.express as px
    from Csvutils import dataframe_agent

    st.title("📊 CSV数据分析智能工具")

    # 初始化 CSV 历史记录
    if "csv_history" not in st.session_state:
        st.session_state["csv_history"] = []


    def create_chart(input_data, chart_type):
        df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
        if chart_type == "bar":
            df_data.set_index(input_data["columns"][0], inplace=True)
            st.bar_chart(df_data)
        elif chart_type == "line":
            df_data.set_index(input_data["columns"][0], inplace=True)
            st.line_chart(df_data)
        elif chart_type == "scatter":
            if len(input_data["columns"]) >= 2:
                fig = px.scatter(df_data, x=input_data["columns"][0], y=input_data["columns"][1])
                st.plotly_chart(fig)
            else:
                st.warning("散点图需要至少两列数据")


    # 上传数据
    data = st.file_uploader("📥 上传你的数据文件（CSV格式）：", type="csv")
    if data:
        df = pd.read_csv(data)
        st.session_state["df"] = df
        with st.expander("🔍 原始数据预览"):
            st.dataframe(df)

    query = st.text_area("🧠 请输入你关于表格的问题、提取请求或可视化要求（比如提取、计算、分析或统计某些数据；生成条形图、折线图或是散点图）：")
    api_key = os.getenv("DEEPSEEK_API_KEY") or st.session_state.get("api_key")

    if st.button("🚀 生成回答"):
        if not api_key:
            st.warning("❗ 请输入你的 DeepSeek API 密钥")
        elif "df" not in st.session_state:
            st.warning("❗ 请先上传 CSV 文件")
        else:
            with st.spinner("正在思考中，请稍候..."):
                response_dict = dataframe_agent(api_key, st.session_state["df"], query)

                # 展示回答
                if "answer" in response_dict:
                    st.markdown("#### 💡 回答：")
                    st.write(response_dict["answer"])
                if "table" in response_dict:
                    st.markdown("#### 📋 表格数据：")
                    st.table(
                        pd.DataFrame(response_dict["table"]["data"], columns=response_dict["table"]["columns"]))
                if "bar" in response_dict:
                    st.markdown("#### 📊 条形图")
                    create_chart(response_dict["bar"], "bar")
                if "line" in response_dict:
                    st.markdown("#### 📈 折线图")
                    create_chart(response_dict["line"], "line")
                if "scatter" in response_dict:
                    st.markdown("#### ⚪ 散点图")
                    create_chart(response_dict["scatter"], "scatter")

                # 保存历史记录（包括图表）
                history_entry = {
                    "question": query,
                    "answer": response_dict.get("answer", ""),
                    "bar": response_dict.get("bar"),
                    "line": response_dict.get("line"),
                    "scatter": response_dict.get("scatter")
                }
                st.session_state["csv_history"].append(history_entry)

    # 展示历史记录（包括图表）
    if st.session_state["csv_history"]:
        with st.expander("🕰️ 点击查看历史记录"):
            for item in reversed(st.session_state["csv_history"]):
                st.markdown(f"**你：** {item['question']}")
                st.markdown(f"**AI：** {item['answer']}")
                if item.get("bar"):
                    st.markdown("📊 条形图：")
                    create_chart(item["bar"], "bar")
                if item.get("line"):
                    st.markdown("📈 折线图：")
                    create_chart(item["line"], "line")
                if item.get("scatter"):
                    st.markdown("⚪ 散点图：")
                    create_chart(item["scatter"], "scatter")
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
    now = datetime.datetime.now()
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