import os
import requests
import streamlit as st

CHAT_API_URL = os.getenv(
    "CHAT_API_URL",
    "http://localhost:8000/chat",
)

VISION_API_URL = os.getenv(
    "VISION_API_URL",
    CHAT_API_URL.replace("/chat", "/vision/classify"),
)

st.set_page_config(page_title="Analytics Chatbot", layout="wide")
st.title("Analytics Chatbot")
st.caption("BigQuery • dbt • FastAPI • RAG • Vision")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = None

with st.sidebar:
    st.header("Image context")
    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
    )

    use_image_context = st.checkbox(
        "Use image as context",
        value=True,
        disabled=uploaded_image is None,
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a question about the business...")

if prompt:
    final_prompt = prompt
    vision_result = None

    if uploaded_image is not None and use_image_context:
        try:
            files = {
                "file": (
                    uploaded_image.name,
                    uploaded_image.getvalue(),
                    uploaded_image.type,
                )
            }

            vision_response = requests.post(
                VISION_API_URL,
                files=files,
                params={"top_k": 5},
                timeout=60,
            )
            vision_response.raise_for_status()
            vision_result = vision_response.json()

            labels = [
                f'{p["label"]} ({p["score"]})'
                for p in vision_result.get("predictions", [])
            ]

            image_context = ", ".join(labels)

            final_prompt = f"""
User question:
{prompt}

Image classification context:
The uploaded image was classified by the vision model as: {image_context}.

Use the image classification context only if it is relevant to answer the user.
""".strip()

        except Exception as e:
            st.warning(f"Image classification failed: {e}")

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "message": final_prompt,
        "history": st.session_state.messages[:-1],
    }

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(CHAT_API_URL, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()

                answer = data.get("answer", "No answer returned.")
                st.markdown(answer)

                if vision_result:
                    with st.expander("Vision context used"):
                        st.json(vision_result)

        st.session_state.last_response = data
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

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

with st.sidebar:
    st.divider()
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