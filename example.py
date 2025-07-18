import streamlit as st
import pandas as pd


st.write('这是一串测试')
st.write('## 这是一串测试')
st.title('这是标题 💡')

st.image('./图片.png',width=300)

st.divider()

df=pd.DataFrame({'学号':['01','02','03'],'班级':['04','05','06']})
st.dataframe(df)

name=st.text_input('请输入一串数字')
if name:
    st.write(f'你好,{name}')

age=st.number_input('输入数字',value=0,min_value=0,max_value=100,step=1)

checked=st.checkbox('没问题')
if checked:
    st.write(f'你看到了秘密！')

with st.sidebar:
    st.divider()

    st.radio('你的姓别',['男','女','未知','1'],index=None)

    st.divider()
    st.selectbox('联系方式',['电话','短信','邮件'])

column1,column2=st.columns(2)
with column1:
    st.write('第一列')
with column2:
    st.write('第二列')

column3,column4=st.columns([1,5])
with column3:
    st.write('第三列')
with column4:
    st.write('第四列')


tab1,tab2,tab3=st.tabs(['1','2','3'])
with tab1:
    st.write('第一个选项卡')
with tab2:
    st.write('第一个选项卡')
with tab3:
    st.write('第一个选项卡')


st.multiselect('你喜欢什么水果',['1','2','3'])