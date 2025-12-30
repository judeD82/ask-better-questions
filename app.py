import streamlit as st
import random
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Ask Better Questions",
    page_icon="❓",
    layout="centered"
)

# --------------------------------------------------
# Password gate
# --------------------------------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["app_password"]:
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        return False

    if not st.session_state["authenticated"]:
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("Incorrect password")
        return False

    return True


if not check_password():
    st.stop()

# --------------------------------------------------
# Load ML model (cached)
# --------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# --------------------------------------------------
# App UI
# --------------------------------------------------
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

# --------------------------------------------------
# Question bank
# --------------------------------------------------
QUESTIONS = [
    # Gentle
    {"text": "What do I actually want here?", "tone": "Gentle"},
    {"text": "What would make this feel 10% lighter?", "tone": "Gentle"},
    {"text": "What am I assuming without checking?", "tone": "Gentle"},
    {"text": "What’s the smallest honest step?", "tone": "Gentle"},
    {"text": "What feels unclear, specifically?", "tone": "Gentle"},

    # Direct
    {"text": "What decision am I avoiding?", "tone": "Direct"},
    {"text": "What’s the real constraint?", "tone": "Direct"},
    {"text": "What would action look like if I stopped overthinking?", "tone": "Direct"},
    {"text": "What happens if I do nothing for another month?", "tone": "Direct"},
    {"text": "What outcome am I secretly hoping for?", "tone": "Direct"},

    # Uncomfortable
    {"text": "What am I protecting myself from seeing?", "tone": "Uncomfortable"},
    {"text": "What do I gain by staying stuck?", "tone": "Uncomfortable"},
    {"text": "What truth would disrupt my current story?", "tone": "Uncomfortable"},
    {"text": "If I respected myself, what would I do next?", "tone": "Uncomfortable"},
    {"text": "What responsibility am I quietly refusing to take?", "tone": "Uncomfortable"},
]

# --------------------------------------------------
# Generate questions (semantic matching)
# --------------------------------------------------
if st.button("Generate questions"):
    if not issue.strip():
        st.warning("Write a sentence or two first.")
    else:
        # Filter questions by tone
        filtered = [q for q in QUESTIONS if q["tone"] == tone]
        texts = [q["text"] for q in filtered]

        # Encode text
        question_embeddings = model.encode(texts)
        input_embedding = model.encode([issue])

        # Compute similarity
        similarities = cosine_similarity(input_embedding, question_embeddings)[0]

        # Select top 3 most relevant questions
        top_indices = np.argsort(similarities)[-3:][::-1]

        st.subheader("Your questions")
        for idx in top_indices:
            st.write("•", texts[idx])

        st.divider()
        st.caption(
            "Suggestion: choose one question and write for 3 minutes without stopping."
        )
