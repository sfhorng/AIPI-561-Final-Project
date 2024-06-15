"""This module tests the whether the retrieved context from the
created index based on a sample dataset of movies is accurate.
The sample dataset is pulled directly from the datasets for each
decade."""

import os
import json
import pytest
from src.movie_chatbot.index import retrieve_documents_from_file
from llama_index.embeddings.huggingface import (
    HuggingFaceEmbedding,
)  # pylint: disable=import-error, no-name-in-module
from llama_index.core import (
    VectorStoreIndex,
)

os.environ["IS_TESTING"] = "True"  # For mocking LLM
TEST_DATASET_FILENAME = "tests/dataset.json"
MISPELLED_KEYWORD_TO_TITLE = {
    "xman": "X-Men",
    "matrex resurrections": "The Matrix Resurrections",
    "the terminater dark fate": "Terminator: Dark Fate",
}


@pytest.fixture(scope="session", name="movie_info_dict")
def fixture_movie_info_dict():
    """Create a dictionary with the movie and corresponding information
    in from the test file. This will be used to retrieve the 'extract'
    field for comparing the context.
    """
    with open(file=TEST_DATASET_FILENAME, encoding="utf-8", mode="r") as f:
        movies_list = json.load(f)
    movies_dict = {movie["title"]: movie for movie in movies_list}
    return movies_dict


@pytest.fixture(scope="session", name="chat_engine")
def fixture_chat_engine():
    """Create chat engine from test Document objects."""
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    documents = retrieve_documents_from_file(filename=TEST_DATASET_FILENAME)
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model,
    )
    context_chat_engine = index.as_chat_engine(chat_mode="context", llm="default")
    return context_chat_engine


@pytest.mark.parametrize(
    "movie",
    [
        "The Kleptomaniac",
        "Antony and Cleopatra",
        "The Lost Battalion",
        "The Cloud Dodger",
        "The Terminator",
        "Terminator: Dark Fate",
        "The Matrix",
        "The Matrix Resurrections",
        "X-Men",
        "X2: X-Men United",
    ],
)
def test_retrieval(chat_engine, movie_info_dict, movie):
    """Verify whether the output of the model given an input with
    the title represented in the index provides the correct context.
    """
    user_input = f"Give me a summary of the details of the movie titled {movie}."
    # LlamaIndex returns a response object that contains
    # both the output string and retrieved nodes
    response_object = chat_engine.chat(user_input)
    # Check top source node is for movie
    top_retrieved_source_node = response_object.source_nodes[0]
    top_retrieved_title = top_retrieved_source_node.metadata["title"]
    assert top_retrieved_title == movie
    # Check context retrieved for movie is the same as the one from file
    context_for_top_title = top_retrieved_source_node.text
    actual_context_for_title = movie_info_dict[movie]["extract"]
    assert context_for_top_title == actual_context_for_title


@pytest.mark.parametrize(
    "misspelled_movie",
    [
        "xman",
        "matrex resurrections",
        "the terminater dark fate",
    ],
)
def test_retrieval_misspelled(chat_engine, movie_info_dict, misspelled_movie):
    """Verify whether the output of the model given an slightly
    misspelled input for a title represented in the index
    provides the correct context.
    """
    user_input = (
        f"Give me a summary of the details of the movie titled {misspelled_movie}."
    )
    # LlamaIndex returns a response object that contains
    # both the output string and retrieved nodes
    response_object = chat_engine.chat(user_input)
    # Check top source node is for the one closest to misspelled_movie
    top_retrieved_source_node = response_object.source_nodes[0]
    top_retrieved_title = top_retrieved_source_node.metadata["title"]
    correct_spelling_movie = MISPELLED_KEYWORD_TO_TITLE[misspelled_movie]
    assert top_retrieved_title == correct_spelling_movie
    # Check context retrieved for movie is the same as the one from file
    context_for_top_title = top_retrieved_source_node.text
    actual_context_for_title = movie_info_dict[correct_spelling_movie]["extract"]
    assert context_for_top_title == actual_context_for_title
