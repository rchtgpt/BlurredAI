from openai import OpenAI
import streamlit as st

def main():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 400px;
            margin-left: -400px;
        }
        
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        
        # Set up sidebar for chat history
        st.title("Chat History")
        st.write("This is where your chat history goes.")
        "[Model Duplication Warning...](https://platform.openai.com/account/api-keys)"
        "[Higher level data insights...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[Git rebase branching...](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

    st.title("😵 BlurredAI")
    st.caption("🚀 A privacy-first inference for any Large Language Model")

    # Create two columns for the panels
    col1, col2 = st.columns(spec=2, gap="medium")

    # First panel covering half the page
    with col1:
        with st.container(height=500, border=True):
            if "messages" not in st.session_state:
                st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input():
                client = OpenAI(api_key="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")
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
                msg = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.chat_message("assistant").write(msg)

    # Second panel covering half the page
    with col2:
        with st.container(height=500, border=True):
            st.header("Panel 2")
            st.write("This is the second panel.")

if __name__ == "__main__":
    main()
