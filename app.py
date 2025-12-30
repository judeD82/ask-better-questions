import streamlit as st
import random

st.set_page_config(page_title="Ask Better Questions")

st.title("Ask Better Questions")
st.caption("This tool gives you better questions, not answers.")

issue = st.text_area(
    "What are you dealing with right now?",
    placeholder="e.g. I feel stuck about money and keep going in circles."
)

tone = st.selectbox(
    "Tone",
    ["Gentle", "Direct", "Uncomfortable"]
)

QUESTIONS = {
    "Gentle": [
        "What do I actually want here?",
        "What would make this feel 10% lighter?",
        "What am I assuming without checking?",
        "What’s the smallest honest step?"
    ],
    "Direct": [
        "What decision am I avoiding?",
        "What’s the real constraint?",
        "What would action look like if I stopped overthinking?",
        "What happens if I do nothing for another month?"
    ],
    "Uncomfortable": [
        "What am I protecting myself from seeing?",
        "What do I gain by staying stuck?",
        "What truth would disrupt my current story?",
        "If I respected myself, what would I do next?"
    ]
}

if st.button("Generate questions"):
    if issue.strip() == "":
        st.warning("Write a sentence or two first.")
    else:
        st.subheader("Your questions")
        for q in random.sample(QUESTIONS[tone], k=3):
            st.write("•", q)
