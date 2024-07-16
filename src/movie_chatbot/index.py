"""Create index from Document objects from movie data
for the Streamlit app."""

import json
import random
from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

VECTOR_STORE_DIR = "vector_store"


def retrieve_documents_from_file(filename):
    """Create Document objects for movies from file.
    Resource: https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_documents/
    Note:
    - We can't use SimpleDirectoryReader because it doesn't support JSON.
    - This will only need to be run if you want to create your own index.

    Args:
        filename (str): Name of file that contains movie data
            to create Documents for

    Returns:
        documents (List[Documents]): Subset of total documents
            for movies from the file that will be used to create the index
    """
    documents = []
    with open(file=filename, encoding="utf-8", mode="r") as f:
        movies_list = json.load(f)
        print(f"There are {len(movies_list)} movies from {filename}")
        for movie_dict in movies_list:
            # extract provides the summary, cast/crew, and/or history
            if "extract" in movie_dict:
                details = movie_dict["extract"]
                title = movie_dict["title"]
                # Index on the title of the movie
                document = Document(text=details, metadata={"title": title})
                documents.append(document)
    return documents


def retrieve_documents():
    """Aggregate Document objects across all data files and write
    the represented titles from each decade to disk.
    Note: This will only need to be run if you want to create your own index.
    """
    # From dataset titles
    decade_str_list = [
        "1900s",
        "1910s",
        "1920s",
        "1930s",
        "1940s",
        "1950s",
        "1960s",
        "1970s",
        "1980s",
        "1990s",
        "2000s",
        "2010s",
        "2020s",
    ]
    # Track represented titles with Document objects per decade
    titles_with_docs = {}
    # Aggregate all Document objects across all decades
    documents = []
    max_num_docs_decade = 500  # Manage vector store size
    for decade_str in decade_str_list:
        # Track Document objects for movies in the current decade
        # This is tracked in case sampling is needed to manage vector store size
        filename_decade = f"data/movies-{decade_str}.json"
        decade_documents = retrieve_documents_from_file(filename_decade)
        # Determine if sampling is needed
        num_decade_docs = len(decade_documents)
        print(f"There are {num_decade_docs} documents created for the {decade_str}")
        if num_decade_docs < max_num_docs_decade:
            sampled_decade_docs = decade_documents
            print(f"Keeping all {num_decade_docs} documents for {decade_str}")
        else:
            # To keep the amount of memory used to
            #   a more manageable amount
            sampled_decade_docs = random.sample(decade_documents, max_num_docs_decade)
            print(f"Sampling {max_num_docs_decade} documents from {decade_str}")
        # Aggregate sampled Document objects
        documents.extend(sampled_decade_docs)
        # Track represented titles with Document objects
        # This is used to write by decade to file for testing
        decade_titles_with_docs = [doc.metadata["title"] for doc in sampled_decade_docs]
        titles_with_docs[decade_str] = decade_titles_with_docs

    # Serializing JSON
    json_object = json.dumps(titles_with_docs, indent=4)
    # Write all represented titles across all decades
    with open(
        file="titles_in_vector_store.json", encoding="utf-8", mode="w"
    ) as outfile:
        outfile.write(json_object)
        print("Wrote all titles with documents to titles_in_vector_store.json")
    return documents


def create_index(embed_model):
    """Create and store index for later use.
    This should only need to be done once.
    Resource: https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/

    Args:
        embed_model (HuggingFaceEmbedding): Embedding model to use
            during index creation and retrieval step for user prompt

    Returns:
        index (VectorStoreIndex): Vector store to save to disk
            to load upon app startup

    """
    # Create documents from data folder
    documents = retrieve_documents()
    # Create index from documents
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model,
    )
    # Save to disk so that it can be retrieved later
    index.storage_context.persist(persist_dir=VECTOR_STORE_DIR)
    return index


def load_index(embed_model):
    """Load index from saved file.
    Resources:
    - Storage Context: https://docs.llamaindex.ai/en/latest/api_reference/storage/storage_context/
    - Storing and retrieving index: https://docs.llamaindex.ai/en/stable/understanding/storing/storing/

    Args:
        embed_model (HuggingFaceEmbedding): Embedding model to use
            during index creation and retrieval step for user prompt

    Returns:
        index (VectorStoreIndex): Vector store from disk
            to load upon app startup
    """
    # Rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=VECTOR_STORE_DIR)
    # Load the saved index from disk
    index = load_index_from_storage(storage_context, embed_model=embed_model)
    return index
