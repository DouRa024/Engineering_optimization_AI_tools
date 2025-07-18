import datetime
from theme_manager import apply_theme
apply_theme()
import streamlit as st
import base64


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
img1 = image_to_base64("图片2.png")
img2 = image_to_base64("图片3.png")
img3 = image_to_base64("图片4.png")

with open("bg.jpg", "rb") as f:
    bg_image = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{bg_image}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="工程过程增效AI工具",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


with open("static/ling_xin.ttf", "rb") as g:
    font_data = g.read()

font_base641 = base64.b64encode(font_data).decode()
st.markdown(f"""
<style>
@font-face {{
    font-family: 'ling_xin';
    src: url(data:font/truetype;charset=utf-8;base64,{font_base641}) format('truetype');
}}
.custom-title1 {{
    font-family: 'ling_xin';
    font-size: 44px;
    font-weight:regular;
    color: #273332;
    text-align: center;
    letter-spacing: 3px;
    margin-top: -65px;
    margin-bottom: 10px;
    margin-left: 2px;
}}
</style>

<div class="custom-title1">
    ✨欢迎使用工程过程增效工具✨
</div>
""", unsafe_allow_html=True)

column4,column5,column6=st.columns([1,4,1])
with column4:
    with open("video4.mp4", "rb") as f:
        video_bytes = f.read()

    b64_video = base64.b64encode(video_bytes).decode()

    video_html = f"""
       <div style="width: 80px; margin-left:30px; text-align: center;">
         <video width="250" autoplay muted loop style="display: block; margin-left:-800px auto;">
           <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
           Your browser does not support the video tag.
         </video>


       </div>
       """

    st.markdown(video_html, unsafe_allow_html=True)

with column5:
    with open("video.mp4", "rb") as f:
        video_bytes = f.read()

    b64_video = base64.b64encode(video_bytes).decode()

    video_html = f"""
    <div style="width: 800px; margin: 0 auto; text-align: center;">
      <video width="800" autoplay muted loop  style="display: block; margin: 0 auto;">
        <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
        Your browser does not support the video tag.
      </video>

      <div style="width: 660px; margin: 20px auto 0 auto;">
        <h9 style="text-align: left; margin-bottom: 6px;"></h9>
        <div style="
            background-color: #e6f4ff;
            color: black;
            border-left: 6px solid #1e90ff;
            padding: 12px 16px;
            border-radius: 6px;
            text-align: left;margin-bottom: 20px;">
          <span>
            这是一个基于 DeepSeek 的 API 独立开发的 AI 工具系统，您可通过左侧导航栏进行探索
          </span>
        </div>
      </div>
    </div>
    """

    st.markdown(video_html, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style='
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        '>
            <img src='data:image/png;base64,{img1}' width='80'>
            <h5 style='margin: 10px -15px 0px 5px;'> 文件分析</h5>
            <p style='text-align: center;'>使用图表和工具分析您的文件</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        '>
            <img src='data:image/png;base64,{img2}' width='80'>
            <h5 style='margin: 10px -15px 0px 5px;'> 报告优化</h5>
            <p style='text-align: center;'>优化您的各种报告</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        '>
            <img src='data:image/png;base64,{img3}' width='80'>
            <h5 style='margin: 10px -20px 0px  5px;'> 智能问答</h5>
            <p style='text-align: center;'>自定义您的AI助手</p>
        </div>
        """, unsafe_allow_html=True)
with column6:
    with open("video2.mp4", "rb") as f:
        video_bytes = f.read()

    b64_video = base64.b64encode(video_bytes).decode()

    video_html = f"""
       <div style="width: 80px; margin-left:-60px; text-align: center;">
         <video width="247  " autoplay muted loop  style="display: block; margin:0 auto;">
           <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
           Your browser does not support the video tag.
         </video>


       </div>
       """

    st.markdown(video_html, unsafe_allow_html=True)



# 功能卡片




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