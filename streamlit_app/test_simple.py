import streamlit as st

st.title("テストアプリ")
st.write("Streamlitが正常に動作しています")

name = st.text_input("名前を入力してください")
if name:
    st.write(f"こんにちは、{name}さん！")