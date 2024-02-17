from openai import OpenAI
import streamlit as st
from st_pages import Page, show_pages
import time

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
        </style>
        """
    st.markdown(styl, unsafe_allow_html=True)

    show_pages(
        [
        Page("app.py", "Chat", ":thought_balloon:"),
        Page("about.py", "About", ":information_source:")
        ]
    )

    localModelMapping = {'LLaMA-2 Chat (70B)' : 'meta-llama/Llama-2-70b-chat-hf', 'LLaMA-2 Chat (13B)' : 'meta-llama/Llama-2-13b-chat-hf', 'LLaMA-2 Chat (7B)' : 'meta-llama/Llama-2-7b-chat-hf', 'Mistral (7B)' : 'mistralai/Mistral-7B-v0.1', 'Mixtral-8x7B (46.7B)' : 'mistralai/Mixtral-8x7B-v0.1'}
    remoteModelMapping = {'GPT-4':'gpt-4-turbo-preview', 'GPT-3.5':'gpt-3.5-turbo', 'Gemini-1.0 Pro': 'gemini-1.0-pro'}

    with st.sidebar:
        
        # Set up sidebar for chat history
        st.title("Chat History")
        st.write("This is where your chat history goes.")
        "[Model Duplication Warning...](https://platform.openai.com/account/api-keys)"
        "[Higher level data insights...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[Git rebase branching...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

    st.title("😵 BlurredAI")
    st.caption("🚀 A privacy-first inference for any Large Language Model")
    currentPrompt = ""
    userInputted = False

    # Create two columns for the panels
    col1, col2 = st.columns(spec=2, gap="medium")

    def stream_data(textToDisplay):
        for word in textToDisplay.split():
            yield (word + " ")
            time.sleep(0.08)

    # First panel covering half the page
    with col1:
        localModelChosen = st.selectbox('Choose a local language model for filtering',
                ('LLaMA-2 Chat (70B)', 'LLaMA-2 Chat (13B)', 'LLaMA-2 Chat (7B)', 'Mistral (7B)', 'Mixtral-8x7B (46.7B)'))
        print("the user is using", localModelMapping[localModelChosen])
        with st.container(height=500, border=True):
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                if (message["role"] == "user"):
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            # React to user input
            if prompt := st.chat_input("Type something here..."):
                
                userInputted = True
                currentPrompt = prompt
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.write_stream(stream_data(prompt))
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

    # Second panel covering half the page
    with col2:
        remoteModelChosen = st.selectbox('Choose a remote language model for computation',
                ('GPT-4', 'GPT-3.5', 'Gemini-1.0 Pro'))
        print("the user is using", remoteModelMapping[remoteModelChosen])
        with st.container(height=500, border=True):
            if userInputted:
                response = f"You wrote: {currentPrompt}"
                userInputted = False
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.write_stream(stream_data(response))
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
