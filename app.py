from openai import OpenAI
import streamlit as st
from st_pages import Page, show_pages
import time
import pandas as pd
from io import StringIO
import sys
from tabulate import tabulate
import os
import re
sys.path.append(f"./backend/")
from main import user_input, reblur_data, process_request
from pdfminer.high_level import extract_text
UPLOAD_FOLDER = 'uploaded_files/'

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="BlurredAI", page_icon="https://media.discordapp.net/attachments/713817450130571416/1208719786041810984/icon.png?ex=65e44f05&is=65d1da05&hm=080bc21bdb34c2fcc95dc6e6bfbc7332223822f3fc1b536762bfc2df879eb3a0&=&format=webp&quality=lossless&width=1376&height=1376")
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

    show_pages(
        [
        Page("app.py", "Chat", ":thought_balloon:"),
        Page("about.py", "About", ":information_source:")
        ]
    )

    # localModelMapping = {'LLaMA-2 Chat (70B)' : 'meta-llama/Llama-2-70b-chat-hf', 'LLaMA-2 Chat (13B)' : 'meta-llama/Llama-2-13b-chat-hf', 'LLaMA-2 Chat (7B)' : 'meta-llama/Llama-2-7b-chat-hf', 'Mistral (7B) Instruct v0.2' : 'mistralai/Mistral-7B-Instruct-v0.2', 'Mixtral-8x7B Instruct (46.7B)' : 'mistralai/Mixtral-8x7B-Instruct-v0.1'}
    localModelMapping = {'LLaMA-2 Chat (70B)' : 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'LLaMA-2 Chat (13B)' : 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'LLaMA-2 Chat (7B)' : 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'Mistral (7B) Instruct v0.2' : 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B Instruct (46.7B)' : 'mistralai/Mixtral-8x7B-Instruct-v0.1'}

    remoteModelMapping = {'GPT-4':'gpt-4-turbo-preview', 'GPT-3.5':'gpt-3.5-turbo', 'Gemini-1.0 Pro': 'gemini-1.0-pro'}
    redactedInstruction = ""
    redactedText = ""
    rawData = ""
    unblurredData = ""
    currentPrompt = ""
    file_path = ""
    redactedDataApproved = False
    private_data = ""

    if 'redactedDataApproved' not in st.session_state:
        st.session_state.redactedDataApproved = redactedDataApproved

    if 'currentPrompt' not in st.session_state:
        st.session_state.currentPrompt = currentPrompt

    if 'redacted' not in st.session_state:
        st.session_state.redacted = redactedText

    if 'redactedInstruction' not in st.session_state:
        st.session_state.redactedInstruction = redactedInstruction

    if 'rawData' not in st.session_state:
        st.session_state.rawData = rawData

    if 'unblurredData' not in st.session_state:
        st.session_state.unblurredData = unblurredData
    
    if 'running_state' not in st.session_state:
        st.session_state.running_state = ""
    
    if 'file_path' not in st.session_state:
        st.session_state.file_path = ""
    
    if 'private_data' not in st.session_state:
        st.session_state.private_data = ""

    with st.sidebar:
        
        # Set up sidebar for chat history
        st.title("Chat History")
        st.write("This is where your chat history goes.")
        "[Model Duplication Warning...](https://platform.openai.com/account/api-keys)"
        "[Higher level data insights...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[Git rebase branching...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

    userInputted = False

    # Create two columns for the panels
    col0, col1, col2 = st.columns([2, 3, 3])

    def stream_data(textToDisplay, stop_time = 0.03):
        for word in re.split(r'(\s+)', textToDisplay):
            yield word
            time.sleep(stop_time)

    # First panel covering half the page
    with col0:
        # st.title("BlurredAI")
        st.image("https://media.discordapp.net/attachments/713817450130571416/1208728527323668520/cover.png?ex=65e4572a&is=65d1e22a&hm=7f169f9aa186d86b8814c0dd124c3486e2db7280886fdf56d9dbf43ac4643e20&=&format=webp&quality=lossless&width=1410&height=452")
        st.caption("A privacy-first inference for any Large Language Model")
        private_data = st.text_area("Text your private data here", height=300)
        uploaded_file = st.file_uploader("Choose a file")

    with col1:
        localModelChosen = st.selectbox('Choose a local model to privatize your request',
                ('Mixtral-8x7B Instruct (46.7B)', 'Mistral (7B) Instruct v0.2', 'LLaMA-2 Chat (70B)', 'LLaMA-2 Chat (13B)', 'LLaMA-2 Chat (7B)',  ))
        with st.container(height=650, border=True):
            # Initialize chat history
            if "box1messages" not in st.session_state:
                st.session_state.box1messages = []
            # Display chat messages from history on app rerun
            for message in st.session_state.box1messages:
                if (message["role"] == "user"):
                    with st.chat_message(message["role"], avatar="https://github.com/rchtgpt.png"):
                        st.markdown(message["content"])
                if (message["role"] == "blurredAI"):
                    with st.chat_message("assistant", avatar="https://media.discordapp.net/attachments/713817450130571416/1208709666461323305/logo.jpeg?ex=65e44599&is=65d1d099&hm=ac498b5d773ee33297fa4932964e5f6dd146d14fe2250026967cde3e3f60e16c&=&format=webp&width=1006&height=1008"):
                        st.markdown(message["content"])
            
            if st.session_state.running_state == "prompting":
                prompt = st.session_state.currentPrompt
                private_data = st.session_state.private_data
                uploaded_file = st.uploaded_file
                file_path = st.session_state.file_path
                st.session_state.running_state = "blurring"
                if(st.session_state.currentPrompt != ""):
                    with st.chat_message("user", avatar="https://github.com/rchtgpt.png"):
                        show_text = f'**Instruction:** {prompt}\n\n'
                        st.write_stream(stream_data(f'**Instruction:** {prompt}\n\n', stop_time = 0))
                        if (private_data != ""):
                            show_text += f'**Private Data:** {private_data}'
                            st.write_stream(stream_data(f'**Private Data:** {private_data}', stop_time = 0))
                        if (file_path != ""):
                            #turn uploaded file into a string
                            if file_path.endswith(".csv"):
                                uploaded_file = pd.read_csv(file_path)
                                uploaded_file = tabulate(uploaded_file, headers=uploaded_file.columns, tablefmt="github")
                                #uploaded_file = uploaded_file.replace("\n", "\n\n")
                            else:
                                uploaded_file = extract_text(file_path)
                            show_text += f'**Private File Preview:** \n\n{uploaded_file[:1000]}'
                            st.write_stream(stream_data(f'**Private File Preview:** \n\n{uploaded_file[:1000]}', stop_time = 0))
                    st.session_state.box1messages.append({"role": "user", "content": show_text})
                if(st.session_state.currentPrompt != ""):
                    redactedInstruction, redactedText = user_input(prompt, private_data, localModelMapping[localModelChosen], file_path=file_path)
                    st.session_state.redacted = redactedText
                    st.session_state.redactedInstruction = redactedInstruction
                    userInputted = True
                    st.session_state.currentPrompt = prompt
            if (st.session_state.unblurredData != "" and st.session_state.running_state == "finalizing"):
                st.session_state.box1messages.append({"role": "blurredAI", "content": "**Final Response (Powered by BlurredAI)**\n" + st.session_state.unblurredData})
                with st.chat_message("assistant", avatar="https://media.discordapp.net/attachments/713817450130571416/1208709666461323305/logo.jpeg?ex=65e44599&is=65d1d099&hm=ac498b5d773ee33297fa4932964e5f6dd146d14fe2250026967cde3e3f60e16c&=&format=webp&width=1006&height=1008"):
                    st.write_stream(stream_data("**Final Response (Powered by BlurredAI)**"))
                    st.write_stream(stream_data(st.session_state.unblurredData))
                st.session_state.running_state = "done"
        if prompt := st.chat_input("Ask me a question about your data (privately)..."):
            st.session_state.running_state = "prompting"
            st.uploaded_file = uploaded_file
            if uploaded_file is not None:
                file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            else:
                file_path = ""
            st.session_state.redacted = ""
            st.session_state.rawData = ""
            st.session_state.unblurredData = ""
            st.session_state.currentPrompt = prompt
            st.session_state.redactedDataApproved = False
            st.session_state.file_path = file_path
            st.session_state.private_data = private_data
            st.experimental_rerun()
    def set_state(i):
        if i == 1:
            st.session_state.running_state = "reblurring"
        else:
            st.session_state.running_state = "blurred"
            st.session_state.box2messages.append({"role": "blurredAI", "content": f"**Here is what I'm going to send to the remote server, with sensitive information redacted:**\n\n**Instruction:** {st.session_state.redactedInstruction}\n\n**Redacted Data:** {st.session_state.redacted}"})

        st.session_state.stage = i

    # Second panel covering half the page
    with col2:
        remoteModelChosen = st.selectbox('Choose a remote model to process your private request',
                ('GPT-4', 'GPT-3.5', 'Gemini-1.0 Pro'))
        with st.container(height=650, border=True):
                # Display assistant response in chat message container
                if "box2messages" not in st.session_state:
                    st.session_state.box2messages = []
                # Display chat messages from history on app rerun
                for message in st.session_state.box2messages:
                    print("message", message)
                    if (message["role"] == "user"):
                        with st.chat_message(message["role"], avatar="https://github.com/rchtgpt.png"):
                            st.markdown(message["content"])
                    if (message["role"] == "blurredAI"):
                        with st.chat_message("assistant", avatar="https://media.discordapp.net/attachments/713817450130571416/1208709666461323305/logo.jpeg?ex=65e44599&is=65d1d099&hm=ac498b5d773ee33297fa4932964e5f6dd146d14fe2250026967cde3e3f60e16c&=&format=webp&width=1006&height=1008"):
                            st.markdown(message["content"])
                    if (message["role"] == "llm"):
                        with st.chat_message("assistant", avatar="https://freepnglogo.com/images/all_img/1690998192chatgpt-logo-png.png"):
                            st.markdown(message["content"])
                if st.session_state.redacted != "" and ( st.session_state.running_state == "blurring" or st.session_state.running_state == "reblurred"):
                    with st.chat_message("assistant", avatar="https://media.discordapp.net/attachments/713817450130571416/1208709666461323305/logo.jpeg?ex=65e44599&is=65d1d099&hm=ac498b5d773ee33297fa4932964e5f6dd146d14fe2250026967cde3e3f60e16c&=&format=webp&width=1006&height=1008"):
                        st.write_stream(stream_data("**Here is what I'm going to send to the remote server, with sensitive information redacted:**"))
                        st.write_stream(stream_data(f"**Instruction:** {st.session_state.redactedInstruction}"))
                        st.write_stream(stream_data(f"**Redacted Data:** {st.session_state.redacted}"))
                        if st.button("No, reblur", type="secondary", on_click=set_state, args=[1]):
                            st.experimental_rerun()
                            pass  # Placeholder to prevent content from being cleared
                        if st.button("Yes, continue", type="primary", on_click=set_state, args=[2]):
                            pass  # Placeholder to prevent content from being cleared
                
                if st.session_state.running_state == "reblurring":
                    st.session_state.running_state = "reblurred"
                    st.session_state.redactedInstruction, st.session_state.redacted = reblur_data(st.session_state.currentPrompt, private_data, redactedText, localModelMapping[localModelChosen], file_path = st.session_state.file_path)
                    st.experimental_rerun()

                if st.session_state.running_state == "blurred":          
                    raw_output, unblurred_response = process_request(st.session_state.redactedInstruction, st.session_state.redacted, localModelMapping[localModelChosen], remoteModelMapping[remoteModelChosen])
                    st.session_state.rawData = raw_output
                    st.session_state.unblurredData = unblurred_response
                    if (st.session_state.rawData != ""):
                        with st.chat_message("assistant", avatar="https://freepnglogo.com/images/all_img/1690998192chatgpt-logo-png.png"):
                            # Append the new message to the chat history
                            st.session_state.box2messages.append({"role": "llm", "content": f"**Output by LLM (on Filtered Input)**\n\n {st.session_state.rawData}"})
                            # Display only the new message
                            st.write_stream(stream_data("**Output by LLM (on Filtered Input)**"))
                            st.write_stream(stream_data(st.session_state.rawData))
                        st.session_state.running_state = "finalizing"
                        st.experimental_rerun()
                        #st.session_state.rawData = ""

if __name__ == "__main__":
    main()
