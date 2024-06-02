import streamlit as st
from llama_index.llms.llamafile import Llamafile
import subprocess

# The implementation is largely based off of
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps


def initialize():
    st.title("Movie Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


@st.cache_resource
def load_model():
    subprocess.Popen(["sh", "./rocket-3b.Q5_K_M.llamafile"])
    llm = Llamafile(request_timeout=60)
    return llm


def chat(model):
    # React to user input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = retrieve_from_model(model, prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def retrieve_from_model(model, prompt):
    try:
        resp = model.complete(prompt)
    except Exception:  # pylint: disable=broad-exception-caught
        resp = "I'm sorry. The query took too long to run. Please try another query instead."
    return resp


def run():
    model = load_model()

    initialize()

    chat(model)


if __name__ == "__main__":
    run()
