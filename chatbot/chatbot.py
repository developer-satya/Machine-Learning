import streamlit as st
from openai import OpenAI

st.title("GenAI Chatbot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("what is up?")
if prompt:
    st.session_state.messages.append({"role":"user", "avatar":"😊", "content":prompt})
    with st.chat_message(name="user", avatar="😊"):
        st.markdown(prompt)

    with st.chat_message(name="assistant", avatar="🤖"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "avatar":"🤖", "content": response})