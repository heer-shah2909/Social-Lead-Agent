from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from utils.embeddings import load_vectorstore
from config import MODEL_NAME


vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever()


llm = ChatGroq(
    model_name=MODEL_NAME,
    temperature=0
)


template = """
Use the knowledge below to answer.

Context:
{context}

Question:
{question}

Answer clearly using the context.
"""


prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)


def rag_answer(question):

    docs = retriever.invoke(question)

    context = "\n".join(
        [d.page_content for d in docs]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content