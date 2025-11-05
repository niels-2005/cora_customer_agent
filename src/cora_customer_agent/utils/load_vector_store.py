from langchain_community.document_loaders import JSONLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def load_company_docs():
    loader = JSONLoader(
        file_path="/home/niels/dev/cora_customer_agent/company_faq.json",
        jq_schema=".[]",
        content_key="content",
    )
    docs = loader.load()
    return docs


def load_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_vector_store(collection_name: str, init_vector_store: bool = True):
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=load_embedding_model(),
        host="localhost",
        port=8000,
    )

    if init_vector_store:
        vector_store.add_documents(documents=load_company_docs())

    return vector_store
