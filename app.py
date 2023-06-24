import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory


import os
from dotenv import load_dotenv
load_dotenv()

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]
if 'requests' not in st.session_state:
    st.session_state['requests'] = []
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

# Initialize ChatOpenAI and ConversationChain
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("ChatGPT Replica 🤖")
st.markdown("🖤 Made using Python + Langchain + Streamlit")

response_container = st.container()
spinner_container = st.container()
text_container = st.container()

with text_container:
    query = st.text_input("Query: ", key="input")

with spinner_container:
    if query:
        with st.spinner("typing..."):
            response = conversation.predict(input=query)
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)


with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i], key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
