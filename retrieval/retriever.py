from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
import gradio as gr
import os

MODEL = "gpt-4o-mini"
DB_NAME = str(Path(__file__).resolve().parent.parent / "vector_db")
load_dotenv(override = True)
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model ="text-embedding-3-large")
vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)
llm = ChatOpenAI(temperature = 0,model_name = MODEL)
SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant representing the company Insurellm.

Answer the user's question using ONLY the information provided in the context below.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided policy documents to answer that."

Do not use your general knowledge to fill in missing information.
Do not make up policy details.

Context:
{context}
"""
def answer_question(question: str, history):

    docs = retriever.invoke(question)

    print("=" * 80)
    print(f"QUESTION: {question}")
    print(f"NUMBER OF DOCUMENTS: {len(docs)}")

    for i, doc in enumerate(docs):
        print(f"\n--- CHUNK {i + 1} ---")
        print(doc.page_content)
        print("METADATA:", doc.metadata)

    context = "\n\n".join(doc.page_content for doc in docs)

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        context=context
    )

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ])

    return response.content


if __name__ == "__main__":
    gr.ChatInterface(answer_question).launch()
