# content_processor.py
import streamlit as app
import openai
from langchain.loaders import NotionContentLoader
from langchain.splitter import MarkdownSplitter
from langchain.models import OpenAIModelEmbeddings
from langchain.stores import FAISSVectorStore

# API key setup
openai.api_key = app.secrets["OPENAI_API_KEY"]

# Notion content loading
content_loader = NotionContentLoader("notion_content")
notion_docs = content_loader.load()

# Splitting Notion content
content_splitter = MarkdownSplitter(
    delimiters=["#", "##", "###", "\n\n", "\n", "."],
    segment_size=1500,
    overlap_size=100,
)
processed_docs = content_splitter.split(notion_docs)

# Embedding model initialization
model_embeddings = OpenAIModelEmbeddings()

# Vector conversion and storage
vector_db = FAISSVectorStore.from_documents(processed_docs, model_embeddings)
vector_db.save_to_local("vectors")

print("Stored local vectors.")
