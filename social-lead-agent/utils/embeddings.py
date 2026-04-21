import json

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBED_MODEL


def load_vectorstore():

    with open(
        "knowledge/knowledge_base.json",
        "r"
    ) as f:

        data = json.load(f)

    texts = []

    for section in data.values():

        if isinstance(section, dict):

            for item in section.values():

                texts.append(str(item))

        else:

            texts.append(str(section))

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL
    )

    vectorstore = FAISS.from_texts(
        texts,
        embeddings
    )

    return vectorstore