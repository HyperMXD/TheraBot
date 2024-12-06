.. TheraBot documentation master file, created by
   sphinx-quickstart on Fri Dec  6 19:47:13 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TheraBot
========

TheraBot is a therapeutic chatbot designed to provide mental health support through empathetic and evidence-based interactions. The chatbot employs Retrieval-Augmented Generation (RAG) to incorporate external resources and uses an LLM-based framework for natural conversation. 

We used two diffrent methods to embed and retrieve documents.

This project is made by Mouad BOULAID & Zineb DKIER
Supervised by: Dr. Tawfik MASROUR

.. toctree::
    :maxdepth: 2
    :caption: Table of contents

    method_1
    method_2


Features
--------
- **Dynamic Knowledge Base**: Leverages web scraping and PDF parsing for database creation.
- **Customizable Prompting**: Fine-tuned LLM for empathetic and guided responses.
- **Real-Time Voice Input**: Supports text and speech-based user queries.
- **Streamlined UI**: Easy-to-use chat interface.

Pipeline
--------

1. **Database Preparation**: Collection of relevant mental health resources through web scraping and PDF parsing.
2. **Model Selection**: Use of Ollama's LLM to generate responses.
3. **RAG Implementation**: Integration of Chroma-based and FAISS-based retrievers for context-driven document querying.
4. **Voice-to-Text Service**: Speech recognition for voice input handling.
5. **UI Development**: Streamlit-based interface for interactive user sessions.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UI Development (`TheraBot Interface`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The chatbot UI is built using Streamlit, providing:
- Text-based input via chat box.
- Voice input using `speech_recognition`.
- Dynamic response display.

Dependencies
------------
- `os`
- `ollama`
- `streamlit`
- `speech_recognition`
- `chromadb`
- `llama_parse`
- **LangChain**:
  - `langchain`
  - `langchain-ollama`
  - `langchain_community`

