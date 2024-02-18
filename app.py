from openai import OpenAI
import streamlit as st
from st_pages import Page, show_pages
import time
import pandas as pd
from io import StringIO
import sys
sys.path.append(f"./backend/")
from main import user_input, reblur_data

def main():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 400px;
            margin-left: -400px;
        }
        
        """,
        unsafe_allow_html=True,
    )

    styl = f"""<style>
            .stChatInput {{
            position: fixed;
            bottom: 3rem;
            }}

            .stFileUploader {{
            position: fixed;
            bottom: 3rem;
            }}
            
        </style>
        """
    st.markdown(styl, unsafe_allow_html=True)

    show_pages(
        [
        Page("app.py", "Chat", ":thought_balloon:"),
        Page("about.py", "About", ":information_source:")
        ]
    )

    localModelMapping = {'LLaMA-2 Chat (70B)' : 'meta-llama/Llama-2-70b-chat-hf', 'LLaMA-2 Chat (13B)' : 'meta-llama/Llama-2-13b-chat-hf', 'LLaMA-2 Chat (7B)' : 'meta-llama/Llama-2-7b-chat-hf', 'Mistral (7B) Instruct v0.2' : 'mistralai/Mistral-7B-Instruct-v0.2', 'Mixtral-8x7B Instruct (46.7B)' : 'mistralai/Mixtral-8x7B-Instruct-v0.1'}
    remoteModelMapping = {'GPT-4':'gpt-4-turbo-preview', 'GPT-3.5':'gpt-3.5-turbo', 'Gemini-1.0 Pro': 'gemini-1.0-pro'}
    redactedText = ""

    if 'redacted' not in st.session_state:
        st.session_state.redacted = redactedText

    with st.sidebar:
        
        # Set up sidebar for chat history
        st.title("Chat History")
        st.write("This is where your chat history goes.")
        "[Model Duplication Warning...](https://platform.openai.com/account/api-keys)"
        "[Higher level data insights...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[Git rebase branching...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

    st.title("BlurredAI")
    st.caption("A privacy-first inference for any Large Language Model")
    currentPrompt = ""
    userInputted = False

    # Create two columns for the panels
    col1, col2 = st.columns(spec=2, gap="medium")

    def stream_data(textToDisplay):
        for word in textToDisplay.split():
            yield (word + " ")
            time.sleep(0.04)

    # First panel covering half the page
    with col1:
        localModelChosen = st.selectbox('Choose a local language model for filtering',
                ('Mixtral-8x7B Instruct (46.7B)', 'Mistral (7B) Instruct v0.2', 'LLaMA-2 Chat (70B)', 'LLaMA-2 Chat (13B)', 'LLaMA-2 Chat (7B)',  ))
        with st.container(height=500, border=True):
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                if (message["role"] == "user"):
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # uploaded_file = st.file_uploader("Choose a file")
            # if uploaded_file is not None:
            #     # To read file as bytes:
            #     bytes_data = uploaded_file.getvalue()
            #     st.write(bytes_data)

            #     # To convert to a string based IO:
            #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            #     st.write(stringio)

            #     # To read file as string:
            #     string_data = stringio.read()
            #     st.write(string_data)

            #     # Can be used wherever a "file-like" object is accepted:
            #     dataframe = pd.read_csv(uploaded_file)
            #     st.write(dataframe)
            print("Local model being used", localModelMapping[localModelChosen])
            # React to user input
            if prompt := st.chat_input("Type something here..."):
                redactedText = user_input(prompt, """
                           Dear Sam Altman,

I am excited to submit my application for the CEO position at OpenAI. As a mid-level professional with 30 years of experience in Artificial Intelligence, I am confident that my skills and experience make me a strong candidate for the role.

In my current position at Deepmind, I have honed my skills in Artificial Int, which I believe would be a valuable asset to your team. I am particularly drawn to OpenAI's reputation for , and I am eager to contribute my expertise to help achieve the company's goals.
                           """, localModelMapping[localModelChosen])
                st.session_state.redacted = redactedText
                userInputted = True
                currentPrompt = prompt
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.write_stream(stream_data(currentPrompt))
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

    def set_state(i):
        st.session_state.stage = i

    # Second panel covering half the page
    with col2:
        remoteModelChosen = st.selectbox('Choose a remote language model for computation',
                ('GPT-3.5', 'GPT-4', 'Gemini-1.0 Pro'))
        with st.container(height=500, border=True):
                # Display assistant response in chat message container
                print(redactedText + "hii")
                if st.session_state.redacted != "":
                    with st.chat_message("assistant"):
                        st.write_stream(stream_data(redactedText))
                        # Add assistant response to chat history
                        
                        st.session_state.messages.append({"role": "assistant", "content": redactedText})
                        print("st.session_state.messages",  st.session_state.messages)

                        if 'stage' not in st.session_state:
                            st.session_state.stage = 0

                        if st.session_state.stage == 0:
                            if st.button("No, reblur", type="secondary", on_click=set_state, args=[1]):
                                pass  # Placeholder to prevent content from being cleared
                            if st.button("Yes, continue", type="primary", on_click=set_state, args=[2]):
                                pass  # Placeholder to prevent content from being cleared
                        
                        print("st.session_state.stage",  st.session_state.stage)

                        if st.session_state.stage == 1:
                            print("i am here atleast, i clicked no")
                            st.write_stream(stream_data(reblur_data(currentPrompt, """
                            Dear Sam Altman,

    I am excited to submit my application for the CEO position at OpenAI. As a mid-level professional with 30 years of experience in Artificial Intelligence, I am confident that my skills and experience make me a strong candidate for the role.

    In my current position at Deepmind, I have honed my skills in Artificial Int, which I believe would be a valuable asset to your team. I am particularly drawn to OpenAI's reputation for , and I am eager to contribute my expertise to help achieve the company's goals.
                            """, redactedText, localModelMapping[localModelChosen])))
                            
                        if st.session_state.stage >= 2:
                            # process request
                            name = st.text_input('Name', on_change=set_state, args=[2])

if __name__ == "__main__":
    main()
