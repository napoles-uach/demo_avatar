import streamlit as st
from streamlit_avatar import avatar

lang = "en-EN"

text = st.chat_input("Say something",key=0)
avatar(text)
