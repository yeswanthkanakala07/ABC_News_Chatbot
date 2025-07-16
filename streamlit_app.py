import streamlit as st
from search_es import search_articles
from llm_client import get_openai_response
st.set_page_config(page_title="ABC News Chatbot", layout="wide")
st.title("📰 ABC News Conversational Chatbot")

query = st.text_input("Ask a question about recent ABC News coverage")

if query:
    with st.spinner("Thinking..."):
        docs = search_articles(query)  # From ElasticSearch
        context = "\n\n".join(doc["description"] for doc in docs)
        full_prompt = f"""Answer the user's question based on the following news context:\n\n{context}\n\nUser question: {query}"""
        answer = get_openai_response(full_prompt)
        st.write(answer)