from matplotlib.dviread import Page
import streamlit as st
import pandas as pd
import numpy as np



st.set_page_config(page_title="GenAI")

st.title("GenAI Chat Bot")

if 'messages' not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


prompt = st.chat_input("Ask Something...")
if prompt:
    # st.write("User has send following prompt: " + prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({'role':'user', 'content': prompt})

    response = f'Echo: {prompt}'
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role":"assistant", "content":response})