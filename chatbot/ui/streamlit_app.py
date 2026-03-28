import os
import requests
import streamlit as st

#API_URL = "http://localhost:8000/chat"
API_URL = os.getenv("https://chatbot-api-116752934914.us-central1.run.app", "http://localhost:8000/chat")

st.set_page_config(page_title="Analytics Chatbot", layout="wide")

st.title("Analytics Chatbot")
st.caption("BigQuery • dbt • FastAPI • OpenAI")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = None

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a question about the business...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "message": prompt,
        "history": st.session_state.messages[:-1]
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        answer = data.get("answer", "No answer returned.")
        st.session_state.last_response = data

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(API_URL, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()
                answer = data.get("answer", "No answer returned.")
                st.markdown(answer)

    except Exception as e:
        error_text = f"API connection failed: {e}"

        st.session_state.last_response = {
            "route": "unknown",
            "sql": None,
            "sources": [],
            "error": error_text,
            "resolved_question": None,
        }

        st.session_state.messages.append(
            {"role": "assistant", "content": error_text}
        )

        with st.chat_message("assistant"):
            st.error(error_text)

# Sidebar goes AFTER request handling
with st.sidebar:
    st.header("Debug")

    resp = st.session_state.last_response

    if resp:
        st.subheader("Route")
        st.code(resp.get("route") or "-- none --")

        st.subheader("Resolved Question")
        st.code(resp.get("resolved_question") or "-- none --")

        st.subheader("Generated SQL")
        st.code(resp.get("sql") or "-- no SQL generated --", language="sql")

        st.subheader("Sources")
        sources = resp.get("sources", [])
        if sources:
            for i, src in enumerate(sources, 1):
                if isinstance(src, dict):
                    title = src.get("title") or src.get("source_name") or f"Source {i}"
                    snippet = src.get("snippet") or src.get("content") or ""
                    st.markdown(f"**{i}. {title}**")
                    if snippet:
                        st.caption(snippet)
                else:
                    st.write(src)
        else:
            st.info("No sources")

        st.subheader("Error")
        st.code(resp.get("error") or "None")
    else:
        st.info("Ask a question to see route, SQL, and sources.")