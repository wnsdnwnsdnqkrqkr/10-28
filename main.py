import streamlit as st
st.title('바이브코딩 웹사이트 제작')
name = st.text_input('이름을 입력해주세요 :')
menu = st.selectbox('좋아하는 음식을 선택해주세요 :', ['한식','양식','일식'])
if st.button('인사말') :
  st.write(name+'! 너는'+menu+'을 제일 좋아하는구나')
