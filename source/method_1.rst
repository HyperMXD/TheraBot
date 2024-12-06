First Method
============

API Environment Configuration
=============================
- `LANGCHAIN_TRACING_V2`: Enables tracing for debugging.
- `LANGCHAIN_ENDPOINT`: Endpoint URL for the LangChain API.
- `LANGCHAIN_API_KEY`: API key for secure access.
- `LANGCHAIN_PROJECT`: Identifier for the current LangChain project.

Functional Details
==================

Web Scraping Component And Database Creation
============================================

The web scraping component is responsible for collecting mental health resources from specified URLs. Using `FireCrawlLoader`, content is extracted from trusted websites and processed into document chunks suitable for retrieval-augmented generation (RAG).

^^^^^^^^^^^^^^^^^^^^^^^
1. Define Target URLs :
^^^^^^^^^^^^^^^^^^^^^^^

   The list of target URLs contains links to reliable mental health resources.

   .. code-block:: python

      urls = [
          "https://www.betterhealth.vic.gov.au/health/conditionsandtreatments/cognitive-behaviour-therapy",
          "https://www.mentalhealth.org.uk/explore-mental-health/publications/how-manage-and-reduce-stress",
          "https://www.who.int/news-room/fact-sheets/detail/anxiety-disorders",
          "https://www.who.int/news-room/fact-sheets/detail/mental-disorders",
          "https://www.who.int/news-room/fact-sheets"
      ]

^^^^^^^^^^^^^^^^^^^
2. Load Web Pages :
^^^^^^^^^^^^^^^^^^^

   The `FireCrawlLoader` is used to scrape each URL for content.

   .. code-block:: python

      docs = [FireCrawlLoader(api_key=FireCrawl_API, url=url, mode="scrape").load() for url in urls]

   - **Parameters**:
     - `api_key`: API key for authenticating requests.
     - `url`: The webpage to scrape.
     - `mode="scrape"`: Specifies scraping as the method.

   - **Result**: A list of document objects containing the scraped content.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
3. Flatten the Document List :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   The nested list of documents is flattened into a single list for easier processing.

   .. code-block:: python

      docs_list = [item for sublist in docs for item in sublist]
^^^^^^^^^^^^^^^^^^^^^^^^^^^
4. Split Text into Chunks :
^^^^^^^^^^^^^^^^^^^^^^^^^^^

   To manage large text efficiently, the content is split into smaller chunks using `RecursiveCharacterTextSplitter`.

   .. code-block:: python

      text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=512, chunk_overlap=50)
      doc_splits = text_splitter.split_documents(docs_list)

   - **Chunk Size**: 512 tokens.
   - **Overlap**: 50 tokens to ensure continuity between chunks.
^^^^^^^^^^^^^^^^^^^^
5. Filter Metadata :
^^^^^^^^^^^^^^^^^^^^

   Metadata fields are cleaned to ensure compatibility with the vector store.

   .. code-block:: python

      cleaned_docs = []

      for doc in doc_splits:
          if isinstance(doc, Document) and hasattr(doc, 'metadata'):
              clean_metadat = {k: v for k, v in doc.metadata.items() if isinstance(v, (str, int, float, bool))}
              cleaned_docs.append(Document(page_content=doc.page_content, metadata=clean_metadat))

   - Retains metadata fields of types `str`, `int`, `float`, and `bool`.
   - Creates a new list of cleaned documents.
^^^^^^^^^^^^^^^^^^^^^^^^
6. Generate Embeddings :
^^^^^^^^^^^^^^^^^^^^^^^^
   Embeddings are generated for the text chunks using the Hugging Face `sentence-transformers/all-MiniLM-L6-v2` model.

   .. code-block:: python

      embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                  
7. Store in FAISS Vector Database :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
   The cleaned documents and their embeddings are stored in a FAISS vector store.

   .. code-block:: python

      db = FAISS.from_documents(documents=cleaned_docs, embedding=embeddings)
      db.save_local(DB_FAISS_PATH)
      retriever = db.as_retriever()

   - **FAISS**: Enables efficient similarity-based retrieval of relevant chunks during chatbot interactions.

^^^^^^^^^^^^^^^
Function Output
^^^^^^^^^^^^^^^
The `create_db()` function returns a retriever object:

.. code-block:: python

   return retriever

This retriever is used during chatbot interactions to query the vector store for relevant content.

^^^^^^^
Purpose
^^^^^^^
This web scraping component forms the foundation for integrating external knowledge into the chatbot, allowing it to provide accurate and contextually relevant responses.




Generating Chatbot Output
============================================

The chatbot generates responses using a structured workflow that combines retrieval-augmented generation (RAG), user query processing, and natural language generation. The implementation is encapsulated within the `GenerateResponse` class.

^^^^^^^^^^^^^^^^^^^^
1. Prompt Template :
^^^^^^^^^^^^^^^^^^^^
  
   The chatbot uses a predefined prompt template to guide its responses, ensuring empathy, professionalism, and relevance.

   .. code-block:: python

      self.prompt_template = """
      You are a therapist, and your primary goal is to offer support, understanding, and guidance...
      Relevant Documents : {document}
      Question: {question}
      Answer:
      """

   - **Purpose**: Establishes the tone, style, and constraints for generating responses.
   - **Variables**:
     - `{document}`: Inserts retrieved external context.
     - `{question}`: Inserts the user's query.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2. Check for RAG Requirement :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   Before generating a response, the chatbot evaluates whether the query requires external information.

   .. code-block:: python

      self.rag_check_prompt = """
      You are a highly intelligent assistant...
      Query: "{query}"
      Needs External Information (True/False):
      """

   .. code-block:: python

      def check_need_for_rag(self, user_query):
          try:
              rag_check_input = self.rag_check_prompt.format(query=user_query)
              response = self.model.invoke({"question": rag_check_input})
              return response.strip().lower() == "true"
          except Exception as e:
              print(f"Error checking for RAG need: {str(e)}")
              return False
      """
   - **RAG Decision**:
     - Uses a secondary model prompt to decide if external documents are necessary.
   - **Result**: Returns `True` if RAG is needed, `False` otherwise.

^^^^^^^^^^^^^^^^^^^^^^^
3. Retrieve Documents :
^^^^^^^^^^^^^^^^^^^^^^^

   If RAG is required, the `retreive()` method fetches relevant content from the FAISS vector store.

   .. code-block:: python

      def retreive(self, user_query):
          retriever = create_db()
          retreived_docs = retriever.invoke(user_query)
          retreived_docs_txt = retreived_docs[1].page_content
          return retreived_docs_txt

   - **Steps**:
     - Calls the `create_db()` function to initialize the FAISS retriever.
     - Queries the retriever with the user's input.
     - Extracts and returns the retrieved document's text.

^^^^^^^^^^^^^^^^^^^^^^
4. Generate Response :
^^^^^^^^^^^^^^^^^^^^^^

   The main logic for response generation is implemented in the `generate_answer()` method.

   .. code-block:: python

      def generate_answer(self, user_query, chat_history: list=[]):
          try:
              # Check if external information is needed
              needs_rag = self.check_need_for_rag(user_query)
              if needs_rag:
                  retrieved_docs_txt = self.retreive(user_query)
              else:
                  retrieved_docs_txt = ""

              # Create input for the model
              my_message = [
                  {"role": "system", "content": self.prompt_template, "document": retrieved_docs_txt}
              ]

              # Add previous chat history
              for chat in chat_history:
                  my_message.append({"role": chat["role"], "content": chat["content"]})

              # Append the current user query
              my_message.append({"role": "user", "content": user_query, "document": retrieved_docs_txt})

              # Call the model to generate the response
              generated_answer = ollama.chat(
                  model="llama3.1",
                  messages=my_message
              )

              # Save the conversation to the chat history
              self.log_chat(user_query, generated_answer)
              return generated_answer["message"]["content"]
          except Exception as e:
              error_message = f"An error occurred: {str(e)}"
              return error_message

   - **Key Features**:
     - **Inputs**:
       - System prompt (`self.prompt_template`) ensures responses adhere to predefined guidelines.
       - Retrieved documents are included as context if needed.
       - Chat history and the latest query are appended to maintain conversational continuity.
     - **Response Generation**:
       - Uses the `ollama.chat` function with the `llama3.1` model to generate the response.
     - **Error Handling**:
       - Returns an error message if issues arise during response generation.

^^^^^^^^^^^^^^^^^^^^^
5. Log Chat History :
^^^^^^^^^^^^^^^^^^^^^
                
   Each interaction is logged for continuity in the conversation.

   .. code-block:: python

      def log_chat(self, user_query, response):
          chat = {"user": user_query, "assistant": response}
          self.chat_history.append(chat)

   - **Purpose**: Maintains a record of user queries and assistant responses.
   - **Usage**: Ensures the chatbot builds context across multiple exchanges.

Voice-to-Text
=============
- Uses `speech_recognition` for handling microphone input.
- Converts audio into text and integrates seamlessly into the chat workflow.


User Interface
==============
- Built with Streamlit:
  - Chat-based interaction with support for floating UI elements.
  - Voice input option for user convenience.

License
=======
This project is for educational and non-commercial use only.



