
import os
import asyncio

# from PIL import Images
import streamlit as st

from hn_bot import get_hb_bot

# set streamlit pageconfig

st.set_page_config(page_title="Scratch Agent implementation")
st.title("Scratch Agent implementation")

with st.sidebar:
    st.markdown(
        """
        # **Greetings, Digital Explorer!**

        Are you fatigued from navigating the expansive digital realm in search of daily tech tales.
        Look No-Where else.
        """)

    api_key = st.text_input("Enter the key:", type ="password")
    print(api_key)
    st.session_state["agent"] = get_hb_bot(api_key=api_key)


if "messages" not in st.session_state:
    st.session_state["messages"] = []

def generate_response(question):
    context = "\n".join([msg['bot'] for msg in st.session_state['messsages']])
    response = st.session_state["agent"].run(f'context:{context} Question:{question}')

    return response

# display chat history
for msg in st.session_state["messages"]:
    st.chat_message("human").write(msg['user'])
    st.chat_message("ai").write(msg['bot'])


# chat input handling
if prompt:=st.chat_input():
    st.chat_message('human').write(prompt)

    with st.spinner('thinking....'):
        response = generate_response(prompt)

        st.chat_message('ai').write(response)

    # store history
    st.session_state["mesage"].append({'user':prompt,'bot':response})





