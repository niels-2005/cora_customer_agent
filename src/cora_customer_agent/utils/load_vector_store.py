from langchain_community.document_loaders import JSONLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def load_company_docs(file_path: str):
    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".[]",
        content_key="content",
    )
    docs = loader.load()
    return docs


def load_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_vector_store(
    collection_name: str,
    init_vector_store: bool = True,
    documents_json_path: str = None,
) -> Chroma:
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=load_embedding_model(),
        host="localhost",
        port=8000,
    )

    if init_vector_store:
        vector_store.add_documents(documents=load_company_docs(documents_json_path))

    return vector_store
