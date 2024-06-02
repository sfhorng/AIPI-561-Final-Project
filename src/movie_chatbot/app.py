import streamlit as st
from llama_index.llms.llamafile import Llamafile

st.title("Movie Chatbot")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

llm = Llamafile(temperature=0, seed=0)
resp = llm.complete("Who is Octavia Butler?")
st.write(resp)
