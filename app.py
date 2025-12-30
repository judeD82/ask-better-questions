import streamlit as st
import random

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
    """
    Simple password gate using Streamlit secrets.
    The app will not run unless the correct password is entered.
    """

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
QUESTIONS = {
    "Gentle": [
        "What do I actually want here?",
        "What would make this feel 10% lighter?",
        "What am I assuming without checking?",
        "What’s the smallest honest step?",
        "What feels unclear, specifically?"
    ],
    "Direct": [
        "What decision am I avoiding?",
        "What’s the real constraint?",
        "What would action look like if I stopped overthinking?",
        "What happens if I do nothing for another month?",
        "What outcome am I secretly hoping for?"
    ],
    "Uncomfortable": [
        "What am I protecting myself from seeing?",
        "What do I gain by staying stuck?",
        "What truth would disrupt my current story?",
        "If I respected myself, what would I do next?",
        "What responsibility am I quietly refusing to take?"
    ]
}

# --------------------------------------------------
# Generate questions
# --------------------------------------------------
if st.button("Generate questions"):
    if not issue.strip():
        st.warning("Write a sentence or two first.")
    else:
        st.subheader("Your questions")
        for q in random.sample(QUESTIONS[tone], k=3):
            st.write("•", q)

        st.divider()
        st.caption(
            "Suggestion: choose one question and write for 3 minutes without stopping."
        )
