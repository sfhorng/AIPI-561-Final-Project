import streamlit as st
from llama_index.llms.llamafile import Llamafile
from llama_index.core.llms import ChatMessage
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
    subprocess.Popen(["sh", "./TinyLlama-1.1B-Chat-v1.0.F16.llamafile"])
    llm = Llamafile(additional_kwargs={"n_predict": 100})
    return llm


def chat(model):
    # React to user input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response_stream = retrieve_from_model(model)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            full_string_response = st.write_stream(response_stream)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_string_response}
        )


def retrieve_from_model(model):
    # ChatMessage: https://github.com/run-llama/llama_index/blob/4d2e8dbdc202eb58b3dc2e34b8da1bf7343f4a01/llama-index-core/llama_index/core/base/llms/types.py#L29
    messages = [
        ChatMessage(
            role=m["role"],
            content=m["content"],
        )
        for m in st.session_state.messages
    ]
    # stream_chat: https://docs.llamaindex.ai/en/stable/examples/llm/llamafile/
    model_response_stream = model.stream_chat(messages)
    for response in model_response_stream:
        # Get next chunk
        yield response.delta


def run():
    model = load_model()

    initialize()

    chat(model)


if __name__ == "__main__":
    run()
