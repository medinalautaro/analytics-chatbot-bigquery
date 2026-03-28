from __future__ import annotations

import streamlit as st

from queries import QUERY_TEMPLATES
from utils import classify_question, run_query, explain_query_type

PROJECT_ID = "project-f3e4931e-2406-418c-917"

st.set_page_config(page_title="Analytics Chatbot", page_icon="📊")
st.title("Analytics Chatbot")
st.write("Ask questions about revenue, products, and channel performance.")

example_questions = [
    "What was total revenue last month?",
    "Show me the top products by revenue",
    "How is channel performance doing?",
]

st.markdown("**Example questions**")
for q in example_questions:
    st.write(f"- {q}")

question = st.text_input("Enter your question")

if question:
    query_type = classify_question(question)

    if query_type == "unknown":
        st.warning(
            "Question not supported yet. Try asking about revenue, top products, or channel performance."
        )
    else:
        sql = QUERY_TEMPLATES[query_type].format(project_id=PROJECT_ID)

        st.subheader("Interpretation")
        st.write(explain_query_type(query_type))

        st.subheader("Generated SQL")
        st.code(sql, language="sql")

        df = run_query(PROJECT_ID, sql)

        st.subheader("Result")
        st.dataframe(df, use_container_width=True)

        if query_type == "channel_performance" and not df.empty:
            st.subheader("Chart")
            chart_df = df.set_index("marketing_channel")["revenue"]
            st.bar_chart(chart_df)

        elif query_type == "top_products" and not df.empty:
            st.subheader("Chart")
            chart_df = df.set_index("product_name")["revenue"]
            st.bar_chart(chart_df)