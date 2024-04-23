import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override= True)

import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings

from langchain.schema import(
    SystemMessage,
    HumanMessage,
    AIMessage
)
from streamlit_chat import message


pc = pinecone.Pinecone()
embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)  # 512 works as well
vector_store = Pinecone.from_existing_index('personaldata', embeddings)
chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

def get_conversational_chain():
    prompt_template = """
    Provide details based on the available information.\n\n
    context: \n{context}\n
    Question: {question}\n

    Answer:
    """
    model = ChatOpenAI(model_name = 'gpt-4-turbo-preview', temperature = 0)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context","question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# def user_input(user_question):
#     embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)
#     new_db = Pinecone.from_existing_index('resume', embeddings)
#     docs = new_db.similarity_search(user_question)
#     chain = get_conversational_chain()
#     response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
#     st.write("Reply: ", response["output_text"])

def user_input(user_question):
    # Assuming your Pinecone setup and embedding model are correctly initialized
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)
    new_db = Pinecone.from_existing_index('personaldata', embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents":docs ,"question": user_question}, return_only_outputs=True)
    # Generate the response and update the session state (chat history)
    if response["output_text"]:
        reply = response["output_text"]
    else:
        reply = "I'm sorry, I couldn't find a relevant answer."
    # Return the reply for further processing
    return reply

def main():
    st.set_page_config(page_title='Job Search Assistant')
    st.header("Cortana 🤖")

    if 'messages' not in st.session_state:
        st.session_state.messages = [SystemMessage(content='You are a useful assistant that speaks in English manners.')]

    user_prompt = st.text_input(label='Send a message', key='user_prompt')
    if user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))

        with st.spinner('Working on your request...'):
            # Use the RAG method to process the user's input and get a response
            reply = user_input(user_prompt)
            
        st.session_state.messages.append(AIMessage(content=reply))
        # # Clear the input box after processing
        # st.session_state['user_prompt'] = ''

    # Displaying the messages (chat history) with the most recent at the top
    for i, msg in enumerate(reversed(st.session_state.messages)):
        if isinstance(msg, HumanMessage) or isinstance(msg, AIMessage):
            is_user = isinstance(msg, HumanMessage)
            message(msg.content, is_user=is_user, key=f'reversed_msg_{i}')

if __name__ == "__main__":
    main()
