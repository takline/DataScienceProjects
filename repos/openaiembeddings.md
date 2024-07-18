---
layout: post-wide
hero-bg-color: "#00aeef"
uid: openaiembeddings
title:  "AI Projects"
worktype: "Coding"
date:   2023-04-19 15:35:01
categories: portfolio
progress: 100
---

[OpenAI Embeddings in Notion](https://github.com/takline/Home/tree/main/AI/OpenAI%20-%20Embeddings%20with%20Notion)


This repo will help guide you through the creation of a Notion chatbot utilizing a blend of LangChain, OpenAI, FAISS, and Streamlit!

## The Concept Behind a Notion Chatbot

Imagine a chatbot seamlessly integrated into Notion.

### The Challenge
In my previous engagement, a client had their entire organizational database on Notion. Given the extensive documentation, swiftly locating specific information was a challenge. To counter this, I devised a Notion chatbot, leveraging cutting-edge AI tools to simplify information retrieval.

### The Approach
Our strategy begins with LangChain to parse and segment Notion's content, transforming it into vector representations via OpenAI embeddings, and housing them in FAISS, a vector database. We craft a Conversational Retrieval Chain using LangChain to bridge our vector database and OpenAI GPT, aiming to respond to queries with the most pertinent information derived from our Notion database. Enhancements include customizing the system prompt and integrating memory capabilities. The final touch involves crafting a user-friendly chat interface via Streamlit, embedding it directly within Notion.

## Project Roadmap

1. Initial Setup and Framework
We explore the project's framework and set up necessary dependencies. This stage also involves securing an OpenAI API key and replicating a public Notion page to form the foundation of our project.

2. Processing Documents
This phase focuses on transforming Notion's content into numerical vectors. Given the limitations of LLMs like GPT in processing lengthy texts, we employ LangChain to fragment the content into manageable segments. These segments are then vectorized using OpenAI’s embedding model and stored in a vector database.

3. Formulating Queries
User queries are vectorized using the same embedding model and compared against our pre-established vector database. The corresponding content, alongside the user query, is fed into OpenAI GPT to generate responses.

To enhance the chatbot's functionality, we maintain a record of previous interactions, allowing the chatbot to access this conversational history during interactions.

4. Building the Chatbot Interface
We utilize Streamlit to design an intuitive chat interface, which is then hosted online and integrated within the Notion platform.

This guide takes inspiration from Harrison Chase (Founder of LangChain) on interacting with Notion content through LangChain. Our enhancements include:

- Specific markdown characters for optimal content segmentation
- Memory feature for the chatbot
- Using Streamlit for a sophisticated chat interface, incorporating its new chat functionalities
- Embedding the Streamlit chat application into a Notion page

## Tutorial Overview

1. Project Structure and Initiation

  1.1 Framework of the Project

### Project Framework
The notion-chatbot project is structured as follows:

- .streamlit/secrets.toml: For storing the OpenAI API key
- faiss_index: The FAISS index, our vector database
- notion_content: Directory for Notion content in markdown format
- .gitignore: To exclude tracking of the OpenAI API key and Notion content
- app.py: The Streamlit chat application script
- ingest.py: Script for vectorizing Notion content and indexing
- utils.py: Script for creating the Conversation Retrieval Chain
- requirements.txt: Necessary packages for Streamlit Community Cloud deployment

We'll construct these components step-by-step throughout this tutorial.

1.2 Initializing the Project

- Create a project directory named notion-chatbot
- Establish a new environment and install required dependencies
- Generate a .gitignore file to outline untracked files
- Retrieve your OpenAI API key from OpenAI’s portal
- Set up a .streamlit folder and within it, create secrets.toml for storing the OpenAI API key
- Utilize Blendle Employee Handbook as the knowledge base for this tutorial
- If you don’t have a Notion account, register for free on their site
- Duplicate the Blendle Employee Handbook to your Notion for project use

2. Ingesting Documents
2.1 Exporting Notion Content

- Navigate to the Blendle Employee Handbook main page on Notion
- Opt for Export in Markdown and CSV formats, including subpages
- Save the exported file as notion_content.zip, unzip it, and place it in the notion-chatbot folder

For simplicity, we're manually exporting Notion content for this tutorial.

2.2 Vectorizing Notion Content

To utilize the Notion page content as our chatbot's knowledge base, we convert it into vectors and store them using LangChain, OpenAI embedding model, and FAISS.

Open the project in your preferred IDE and create ingest.py:

```python
# ingest.py

[Code block detailing the process of loading the OpenAI API key, loading and splitting Notion content, initializing the OpenAI embedding model, and converting text chunks into vectors stored in a FAISS index]
```

3. Managing Queries
3.1 Query Process

- Establish a chat history to serve as the chatbot's memory, storing user queries and chatbot responses
- User poses a question, which is logged in the chat history
- Blend the question with the chat history to form a standalone query
- Vectorize the standalone query and search for similar vectors in the database
- GPT generates an answer using the most relevant content from Notion
- The chatbot conveys GPT's answer to the user, adding it to the chat history
- Repeat the process for ongoing interactions

3.2 Handling Queries

We develop a LangChain Conversational Retrieval Chain as the core of our application, creating utils.py to house the load_chain() function.

```python
# utils.py

[Code segment outlining the creation of the Conversational Retrieval Chain, including the initialization of the OpenAI embedding model, the chat model, the local FAISS index, and the memory feature, along with the setup of the system prompt]
```

4. Chatbot Interface Development
4.1 Streamlit Application

With our chatbot's "brain" ready, we proceed to build the Streamlit application:

```python
# app.py

[Code snippet explaining the importation of the chain from utils.py, configuration of the Streamlit page, initialization of the LLM chain and chat history, chat message display mechanism, and the chat logic processing user queries and generating responses]
```

4.2 Deploying on Streamlit Cloud

Ready to go live? Here's how to deploy on Streamlit Cloud:

- Prepare a requirements.txt file listing all dependencies
- Follow the deployment process, specifying Python version and OpenAI API key

4.3 Integrating Streamlit App in Notion

- After successful deployment, copy your app's URL
- In Notion, choose Embed in the block options and paste the app URL

And there you have it, your interactive Notion chatbot is ready for action!

