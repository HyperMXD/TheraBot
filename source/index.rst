.. TheraBot documentation master file, created by
   sphinx-quickstart on Fri Dec  6 19:47:13 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TheraBot
========

AI in mental health is not a new topic for discussion. In the 1960s,the first chatbot, ELIZA,
was created by Joseph Weizenbaum at MIT.It operated using a script called DOCTOR,
which allowed it to respond like a psychotherapist. But despite of it’s simplicity it was
one of the first attempts to use and define chatbots as a resource for mental health.
Since then, the evolution had led to the development of chatbots that are much smarter
and empathetic making them able to hold meaningful conversations.One such chatbot is
Therabot, designed to provide meantal health support to users to help them in their daily
life.
Such mental health issues like anxiety, depression, stress and many others have recently
became more common in our society. However, many people still struggle as they search
for assistance, for instance they may be busy, therapies can be expensive, or they just feel
ashamed. Some of these may be solved by a therapeutic chatbot by providing confidential
and cheap service when compared to other therapeutic solutions.
One of the key benefits of a therapeutic chatbot is that it can be available anytime and
anywhere at the press of a button. This makes it a good choice for individuals who have
no time or cannot afford to attend therapy sessions or those who prefer to do a self-help
program in the comfort of their rooms away from people’s interference... And since the
chatbot is anonymous, users might feel more comfortable opening up about their thoughts
and emotions, and they are more likely to disclose more about their feelings.
Although, therapeutic chatbot is not a replacement for professional therapy, it can
be a helpful tool for those who need immediate support or as an addition to clinical
therapy. And as the technology continues to improve, these chatbots will definitely be
more efficient in identifying and responding to human emotions, a plus to mental health
care.

This project is made by **Mouad BOULAID** & **Zineb DKIER**.

Supervised by: **Dr. Tawfik MASROUR**

.. toctree::
    :maxdepth: 2
    :caption: Table of contents
    method_1
    method_2
Features
========
- **Dynamic Knowledge Base**: Leverages web scraping and PDF parsing for database creation.
- **Customizable Prompting**: Fine-tuned LLM for empathetic and guided responses.
- **Real-Time Voice Input**: Supports text and speech-based user queries.
- **Streamlined UI**: Easy-to-use chat interface.

Requirements
============
The implementation of this project requires the following:

**• Programming Language**
- `Python`

**• Libraries and Frameworks**

- `LangChain:`
   - `langchain`
   - `langchain-ollama`
   - `langchain_community`
   - `langchain_core`

- `ollama`
- `speechRecognition`
- `streamlit`
- `chromadb`
- `llama_parse`
- `os`

Pipeline
========

The pipeline for our therapeutic chatbot involves the following stages :

1. **Database Preparation**: Collection of relevant mental health resources through web scraping and PDF parsing.
2. **Model Selection**: We chose the LLaMa3.1 model from Ollama's LLMs for response generation.
3. **RAG Implementation**: Integration of Chroma-based and FAISS-based retrievers for fetching revelant documents from the prepared data.
4. **Voice-to-Text**: The voice input will be processed and converted to text using Google's SpeechRecognition python module.
5. **UI Development**: We deployed the chatbot using Streamlit

User Input
==========
The chatbot has two inputs : a text input and an audio input.

Text Input
----------

The user directly types their query or message into a text box.

Voice Input
-----------
We integrated the audio input feature using the Streamlit framework and the SpeechRecognition library. Users can speak to the chatbot instead of typing, and their speech is
transcribed into text using Google’s SpeechRecognition Python module.


   .. code-block:: python
       elif recorder:
           recognizer = sr.Recognizer()
           with sr.Microphone() as source:
               st.toast("You can start talking...", icon='🎤')
               recognizer.adjust_for_ambient_noise(source, duration=0.2)  
               audio = recognizer.listen(source)
               try:
                   user_query = recognizer.recognize_google(audio)
                   # Display user message
                   with st.chat_message("user"):
                       st.markdown(user_query)
                   # Generate response, and add it to the chat history
                   response = generator.generate_answer(user_query,chat_history=st.session_state.chat_history)
   
                   # Display the generated response
                   with st.chat_message("assistant"):
                       st.markdown(response)
                   # Update chat history
                   st.session_state.chat_history.append({"role": "user", "content": user_query})
                   st.session_state.chat_history.append({"role": "assistant", "content": response})
               except:
                   st.markdown("Sorry, I did not get that")


First, the user presses the microphone button in the chatbot interface to activate the audio recording feature. 
If the recorder condition is active (microphone button clicked), indicating that the user has triggered the voice recording feature, a Recognizer object from the SpeechRecognition library is created. 
This object will handle audio processing and transcription:

   .. code-block:: python

      recognizer = sr.Recognizer()

Then, the audio is captured using the sr.Microphone() to access the user’s microphone. The with statement ensures that the microphone is properly closed after use:

   .. code-block:: python

      with sr.Microphone() as source:
         st.toast("You can start talking...", icon='🎤')
         recognizer.adjust_for_ambient_noise(source, duration=0.2)  
         audio = recognizer.listen(source)

The user starts speaking when a message **"You can start talking..."** is displayed using the toast method to notify the user that the system is ready to record.
We used **recognizer.adjust_for_ambient noise(source, duration=0.2)** to filter out background noise for better accuracy. This process lasts 0.2 seconds.
Then, **recognizer.listen(source)** records audio from the microphone and stores it in the **audio** variable.

If the transcription fails (for example due to poor audio quality or accents), an error message is displayed to the user :

   .. code-block:: python

      except :
            st.markdown ("Sorry ,I did not get that ")

If the transcription is successful, the **user_query** variable will store the the user's audio input converted into text, using the **recognizer.recognize google(audio)** method:

   .. code-block:: python

      user_query = recognizer.recognize_google(audio)

Finally, the audio input converted into a text format can be handled as a text input and passed to RAG (Retrieval-Augmented Generation) and the llama model for response generation.

LLaMa for Text Generation
=========================

UI Development (`TheraBot Interface`)
=====================================

The chatbot UI is built using Streamlit, it contains:

- Text-based input via chat box.

   .. code-block:: python

      user_query = st.chat_input("What is up?", key="user_input")

- Voice input using a microphone button.

   .. code-block:: python

      recorder = st.button("🎙️")

- Dynamic response display.


