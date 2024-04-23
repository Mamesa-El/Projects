import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from streamlit_chat import message
from dotenv import load_dotenv, find_dotenv
#Security
import streamlit_authenticator as stauth
from document_loader import load_document

load_dotenv(find_dotenv(), override = True)
st.set_page_config(
    page_title='''Mamesa's Assitant A.I''',
    page_icon = '🤖'
)
st.subheader('Job Finder: `The Job is Out There...` 🤖')
chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

# creating the messages (chat history) in the Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# creating the sidebar
with st.sidebar:
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='System role')
    # streamlit text input widget for the user message
    user_prompt = st.text_input(label='Send a message')

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
                )

    # st.write(st.session_state.messages)

    # if the user entered a question
    if user_prompt:
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )

        with st.spinner('Working on your request ...'):
            # creating the ChatGPT response
            response = chat(st.session_state.messages)

        # adding the response's content to the session state
        st.session_state.messages.append(AIMessage(content=response.content))


# adding a default SystemMessage if the user didn't entered one
if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant.'))

# displaying the messages (chat history)
for i, msg in enumerate(st.session_state.messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=f'{i} + 🤓') # user's question
    else:
        message(msg.content, is_user=False, key=f'{i} +  🤖') # ChatGPT response

#-----------------------------Security Feature-------------------------------
# import yaml
# from yaml.loader import SafeLoader
# with open('./config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)
    
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
# name, authenticator_status, user_name = authenticator.login()

# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'sidebar')
#     st.sidebar.success('Logged in as {}'.format(name))
#     st.subheader('Job Finder: `The Job is Out There...` 🤖')
#     st.write(f'Welcome *{st.session_state["name"]}*')
# elif st.session_state["authentication_status"] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] is None:
#     st.warning('Please enter your username and password')

#-----------------------------Security Feature-------------------------------
