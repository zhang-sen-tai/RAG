"""
    基于Streamlit完成Web网页上传服务
"""
import streamlit as st
import time
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title('知识库更新服务')

# 文件上传
uploaded_file = st.file_uploader(
    "请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False, # False表示仅接受一个文件的上传
)

# streamlit 每次刷新页面会是当前程序文件重新执行
# 这样会导致状态值丢失
# st.session_state: 就是用来解决这个问题的，当程序重新执行时，这个字典中的状态值不会被初始化
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 提取文件信息
if uploaded_file is not None:
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024 # kb

    st.subheader(f"文件名: {file_name}")
    st.write(f"格式: {file_type} | 大小: {file_size:.2f} KB ")

    text = uploaded_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中..."):
        time.sleep(2)
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)
