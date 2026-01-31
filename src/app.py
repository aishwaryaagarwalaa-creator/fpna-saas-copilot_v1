import streamlit as st
from narrative import (
    build_prompt,
    load_rag_docs,
    generate_narrative,
    review_narrative
)
from compute import get_fpna_outputs

st.set_page_config(page_title="FP&A Narrative Copilot", layout="wide")

st.title("📊 FP&A Narrative Copilot (SaaS)")
st.caption("Generate executive-ready FP&A commentary with review mode")

st.divider()

# Button
if st.button("🚀 Generate Narrative"):
    try:
        with st.spinner("Generating FP&A narrative..."):
            fpna_data = get_fpna_outputs()
            glossary, rules = load_rag_docs()
            prompt = build_prompt(fpna_data, glossary, rules)

            narrative = generate_narrative(prompt)
            review = review_narrative(narrative)

        st.success("Narrative generated!")
        st.subheader("📈 FP&A Narrative")
        st.markdown(narrative, unsafe_allow_html=True)

        st.divider()

        st.subheader("🧐 Review Mode")
        st.markdown(review)

    except Exception as e:
        st.error("Temporary connection issue. Please click Generate again.")
        st.exception(e)   # optional but VERY useful for demo/debug
