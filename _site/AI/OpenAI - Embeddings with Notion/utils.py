# chat_utils.py
import streamlit as app
import openai
from langchain.chains import ChatRetrievalChain
from langchain.buffers import ConversationHistory
from langchain.models import OpenAIChatModel
from langchain.stores import FAISSVectorRetriever
from langchain.models import OpenAIModelEmbeddings
from langchain.templates import ChatPromptTemplate
from langchain.templates.chat import ChatSystemMessageTemplate

openai.api_key = app.secrets["OPENAI_API_KEY"]


@app.cache_resource
def initialize_chatbot_chain():
    """
    Initializes the chatbot chain for responding to user queries.
    Returns a ChatRetrievalChain object.
    """

    # Embedding and chat model setup
    embeddings = OpenAIModelEmbeddings()
    chat_model = OpenAIChatModel(temperature=0)

    # FAISS index as a retriever
    vector_store = FAISSVectorRetriever.load_from_local("faiss_index", embeddings)
    retriever = vector_store.as_query_retriever(search_args={"k": 3})

    # Chatbot memory setup
    chat_memory = ConversationHistory(window_size=3, memory_key="chat_history")

    # Chat retrieval chain creation
    retrieval_chain = ChatRetrievalChain.from_model(
        chat_model,
        retriever=retriever,
        memory=chat_memory,
        retrieve_chat_history=lambda h: h,
        verbose_output=True,
    )

    # System prompt configuration
    system_prompt = """
    As an AI assistant, you're responsible for answering questions about the COMPANYXXX Employee Handbook.
    Given parts of a document and a question, provide a conversational response.
    If uncertain, respond with 'Sorry, I'm unsure... 😔'.
    For questions outside the handbook's scope, inform the user accordingly.

    {document_context}
    Question: {user_question}
    Suggested Answer:"""

    # Integrating system prompt into the chain
    CHAT_PROMPT = ChatPromptTemplate(
        variables=["document_context", "user_question"], template=system_prompt
    )
    retrieval_chain.document_chain.chat_chain.prompt.messages[
        0
    ] = ChatSystemMessageTemplate(prompt=CHAT_PROMPT)

    return retrieval_chain
