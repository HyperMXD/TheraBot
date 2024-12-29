import ollama
import streamlit as st
import speech_recognition as sr
from langchain.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from streamlit_float import *


# Initialize Chroma database
persist_directory = "rag/Pyscho_db"
vecdb = Chroma(
    persist_directory=persist_directory,
    embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"),
    collection_name="rag-chroma"
)



# RAG retrieval logic
def retrieve_from_db(question):
    # get the model
    model = OllamaLLM(model="llama3.2")
    # initialize the vector store

    retriever = vecdb.as_retriever()
    retrieved_docs = retriever.invoke(question)
    retrieved_docs_txt = retrieved_docs[1].page_content

    return retrieved_docs_txt


# Main chatbot logic
st.markdown("<h1 style='text-align : center;'>🤖 Therapy ChatBot</h1>", unsafe_allow_html=True)

def generate_response(user_message: str, chat_history: list=[], doc=""):
#give role to Chatbot    
    system_msg=("""You are a Chatbot for mental health support, don't overtalk. When the users are trying to harm themselves, remind them that they're loved by someone.
    When asked about someone say "sorry, I don't wanna talk about people". Stick to the context of mental health. If the situation is serious refer to moroccan health services.
    Don't insist on questions, try to be friendly and make the client feel comfortable talking with you.
    don't repeat the same questions in the same message.
    Don't say "Based on the provided context" or "According to the provided document" or any such phrases.
    if there is no answer, please answer with "I m sorry, the context is not enough to answer the question.
    Don't keep on questioning what's happening, your main job is to listen actively and make the client feel comfortable with you.
    Combine what you know and verify it using the Relevant Documents : {document}
    User input: {question}
    
                """)        
    my_message = [{"role": "system", "content": system_msg,  "document": doc}]
#Append history in message 
    for chat in chat_history:                      
        my_message.append({"role": chat["name"], "content": chat["msg"]})
#Append the latest question in message
    my_message.append({"role": "user", "content": user_message, "document": doc})

    response = ollama.chat(                      
    model="llama3.2",
    messages=my_message
    ) 
    return response["message"]["content"]

def main():
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    # Display chat history
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # Placeholder for the input section (audio + text)
    # Create footer container and add content
    input_placeholder = st.container()

    with input_placeholder.container():
        col1, col2 = st.columns([11, 1], gap="small")
        with col1:
            user_message = st.chat_input("What is up?", key="user_input")
        with col2:
            record_audio = st.button("🎙️")
    
        # Float the footer container and provide CSS to target it with
    input_placeholder.float("bottom: 0px;padding : 30px 20px 50px 20px; border-radius: 10px; background:#0E1117;")


    # Process user input
    if user_message:
        with st.chat_message("user"):
            st.markdown(user_message)

        doc = retrieve_from_db(user_message)
        # Generate response
        response = generate_response(user_message, chat_history=st.session_state.chat_log, doc= doc)

        if response:
            with st.chat_message("assistant"):
                assistant_response_area = st.empty()
                assistant_response_area.write(response)

            # Update chat history
            st.session_state.chat_log.append({"name": "user", "msg": user_message})
            st.session_state.chat_log.append({"name": "assistant", "msg": response})

    elif record_audio:
        # Handle audio recording
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.markdown("You can start talking...")
            r.adjust_for_ambient_noise(source, duration=0.2)  
            audio_text = r.listen(source)
            try:
                user_message = r.recognize_google(audio_text)
                with st.chat_message("user"):
                    st.markdown(user_message)
                doc = retrieve_from_db(user_message)
                # Generate response
                response = generate_response(user_message, chat_history=st.session_state.chat_log, doc=doc)

                if response:
                    with st.chat_message("assistant"):
                        assistant_response_area = st.empty()
                        assistant_response_area.write(response)

                    # Update chat history
                    st.session_state.chat_log.append({"name": "user", "msg": user_message})
                    st.session_state.chat_log.append({"name": "assistant", "msg": response})
            except:
                st.markdown("Sorry, I did not get that")

    

if __name__ == "__main__":
    main()
