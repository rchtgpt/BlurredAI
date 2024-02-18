from openai import OpenAI
import streamlit as st
from st_pages import Page, show_pages
import time
import pandas as pd
from io import StringIO
import sys
sys.path.append(f"./backend/")
from main import user_input, reblur_data, process_request

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
    rawData = ""
    unblurredData = ""
    currentPrompt = ""
    redactedDataApproved = False

    if 'redactedDataApproved' not in st.session_state:
        st.session_state.redactedDataApproved = redactedDataApproved

    if 'currentPrompt' not in st.session_state:
        st.session_state.currentPrompt = currentPrompt

    if 'redacted' not in st.session_state:
        st.session_state.redacted = redactedText

    if 'rawData' not in st.session_state:
        st.session_state.rawData = rawData

    if 'unblurredData' not in st.session_state:
        st.session_state.unblurredData = unblurredData

    with st.sidebar:
        
        # Set up sidebar for chat history
        st.title("Chat History")
        st.write("This is where your chat history goes.")
        "[Model Duplication Warning...](https://platform.openai.com/account/api-keys)"
        "[Higher level data insights...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[Git rebase branching...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

    st.title("BlurredAI")
    st.caption("A privacy-first inference for any Large Language Model")
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
                    with st.chat_message(message["role"], avatar="https://github.com/rchtgpt.png"):
                        st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("Type something here..."):
                redactedText = user_input(prompt, """
                           Dear Sam Altman,

I am excited to submit my application for the CEO position at OpenAI. As a mid-level professional with 30 years of experience in Artificial Intelligence, I am confident that my skills and experience make me a strong candidate for the role.

In my current position at Deepmind, I have honed my skills in Artificial Int, which I believe would be a valuable asset to your team. I am particularly drawn to OpenAI's reputation for , and I am eager to contribute my expertise to help achieve the company's goals.
                           """, localModelMapping[localModelChosen])
                st.session_state.redacted = redactedText
                userInputted = True
                st.session_state.currentPrompt = prompt
                # Display user message in chat message container
                with st.chat_message("user", avatar="https://github.com/rchtgpt.png"):
                    st.write_stream(stream_data(st.session_state.currentPrompt))
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                if (st.session_state.unblurredData != ""):
                    st.session_state.messages.append({"role": "assistant", "content": st.session_state.unblurredData})

                    with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuiig-uR57Q6mVe4iMO82umLGrS8tcUjAjSJXToLxhJg&s"):
                        st.write_stream(stream_data("**Final Response (Powered by BlurredAI)**"))
                        st.write_stream(stream_data(st.session_state.unblurredData))

    def set_state(i):
        st.session_state.stage = i

    # Second panel covering half the page
    with col2:
        remoteModelChosen = st.selectbox('Choose a remote language model for computation',
                ('GPT-3.5', 'GPT-4', 'Gemini-1.0 Pro'))
        with st.container(height=500, border=True):
                # Display assistant response in chat message container
                if st.session_state.redacted != "":
                    with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuiig-uR57Q6mVe4iMO82umLGrS8tcUjAjSJXToLxhJg&s"):
                        print(st.session_state.redactedDataApproved)
                        if (st.session_state.redactedDataApproved == False):
                            st.write_stream(stream_data("**Here is what I'm going to send to the remote server, with sensitive information redacted:**"))
                            st.write_stream(stream_data(st.session_state.redacted))
                        else:
                            st.write("**Redacted Version for LLM**")
                            st.write(st.session_state.redacted)


                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": redactedText})

                        if 'stage' not in st.session_state:
                            st.session_state.stage = 0

                        if st.session_state.stage == 0:
                            if st.button("No, reblur", type="secondary", on_click=set_state, args=[1]):
                                pass  # Placeholder to prevent content from being cleared
                            if st.button("Yes, continue", type="primary", on_click=set_state, args=[2]):
                                pass  # Placeholder to prevent content from being cleared

                        if st.session_state.stage == 1:
                            st.session_state.redacted = reblur_data(st.session_state.currentPrompt, """
                            Dear Sam Altman,

    I am excited to submit my application for the CEO position at OpenAI. As a mid-level professional with 30 years of experience in Artificial Intelligence, I am confident that my skills and experience make me a strong candidate for the role.

    In my current position at Deepmind, I have honed my skills in Artificial Int, which I believe would be a valuable asset to your team. I am particularly drawn to OpenAI's reputation for , and I am eager to contribute my expertise to help achieve the company's goals.
                            """, redactedText, localModelMapping[localModelChosen])
                            st.write_stream(stream_data("**Redacted Version for LLM**"))

                            st.write_stream(stream_data(st.session_state.redacted))
                            if st.button("No, reblur", type="secondary", on_click=set_state, args=[1]):
                                pass  # Placeholder to prevent content from being cleared
                            if st.button("Yes, continue", type="primary", on_click=set_state, args=[2]):
                                pass  # Placeholder to prevent content from being cleared
                            
                        if st.session_state.stage == 2:                            
                            # process request
                            raw_output, unblurred_response = process_request(st.session_state.currentPrompt, st.session_state.redacted, localModelMapping[localModelChosen], remoteModelMapping[remoteModelChosen])

                            st.session_state.rawData = raw_output
                            st.session_state.unblurredData = unblurred_response

                    if (st.session_state.rawData != ""):
                        with st.chat_message("assistant", avatar="https://freepnglogo.com/images/all_img/1690998192chatgpt-logo-png.png"):
                            # Append the new message to the chat history
                            st.session_state.messages.append({"role": "assistant", "content": st.session_state.rawData})
                            # Display only the new message
                            st.write_stream(stream_data("**Output by LLM (on Filtered Input)**"))
                            st.write_stream(stream_data(st.session_state.rawData))

                    if (st.session_state.unblurredData != ""):
                        st.session_state.messages.append({"role": "assistant", "content": st.session_state.unblurredData})

                        with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuiig-uR57Q6mVe4iMO82umLGrS8tcUjAjSJXToLxhJg&s"):
                            st.write_stream(stream_data("**Final Response (Powered by BlurredAI)**"))
                            st.write_stream(stream_data(st.session_state.unblurredData))

if __name__ == "__main__":
    main()
