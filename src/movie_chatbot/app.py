"""Main file for starting Streamlit app for the movie chatbot.
The implementation is largely based off of
https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps"""

import subprocess
import streamlit as st
from llama_index.llms.llamafile import Llamafile
from llama_index.embeddings.huggingface import (
    HuggingFaceEmbedding,
)  # pylint: disable=import-error, no-name-in-module
from llama_index.core import Settings

# from index import create_index # uncomment to create your own index
from index import load_index  # pylint: disable=import-error


def initialize():
    """Initialize UI, including any recent messages,
    during startup or reload.
    """
    st.title("Movie Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


@st.cache_resource
def load():
    """Load and cache chat engine during startup.
    Resources:
    - Caching global resource: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource
    - Llamafile class: https://github.com/run-llama/llama_index/blob/1d6c8bfc1517ea096527f7977a5d1f47d75da71d/llama-index-integrations/llms/llama-index-llms-llamafile/llama_index/llms/llamafile/base.py#L29
    - Embeddings from HuggingFace: https://docs.llamaindex.ai/en/stable/examples/embeddings/huggingface/
    - Using Settings: https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/service_context_migration/
    - Chat engine with context mode: https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_context/
    """
    # Start llamafile
    subprocess.Popen(["sh", "./TinyLlama-1.1B-Chat-v1.0.F16.llamafile"])
    # Specify LLM and embedding model in Settings
    llm = Llamafile(additional_kwargs={"n_predict": 100})
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = llm
    Settings.embed_model = embed_model

    ### Please uncomment this and comment out line 54
    # if you would like to create your own index
    # index = create_index(embed_model)

    index = load_index(embed_model)
    # Create chat engine from index using the 'context' mode
    chat_engine = index.as_chat_engine(chat_mode="context", llm=llm)
    return chat_engine


def retrieve_from_model(engine, prompt):
    """Stream response from model.
    Resource: https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_context/
    """
    response = engine.stream_chat(prompt)
    for token in response.response_gen:
        # Get next chunk
        yield token


def chat(engine):
    """Display prompts and responses from chat engine."""
    # React to user input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Retrieve response stream
            response_stream = retrieve_from_model(engine, prompt)
            full_string_response = st.write_stream(response_stream)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_string_response}
        )


def run():
    """Main steps for running the app."""
    # Initialize UI
    initialize()
    # Load and cache chat engine
    engine = load()
    # Interact with chat engine
    chat(engine)


if __name__ == "__main__":
    run()
