import streamlit as st
from llama_index.llms.llamafile import Llamafile


@st.cache_resource
def load_model():
    llm = Llamafile(request_timeout=60)
    return llm


def retrieve_answer_and_output(model, prompt):
    resp = model.complete(prompt)
    st.markdown(resp)


def run():
    st.title("Movie Chatbot")

    model = load_model()

    prompt = st.chat_input("What would you like to know?")
    if prompt:
        retrieve_answer_and_output(model, prompt)


if __name__ == "__main__":
    run()
