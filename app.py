import streamlit as st
import time
import json
from datetime import datetime
from llm import generate_response
from prompts import technical_question_prompt

st.set_page_config(
    page_title="TalentScout — Initial Candidate Screening",
    layout = "centered"
)
# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "stage" not in st.session_state:
    st.session_state.stage = "greeting"

if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "name": "",
        "email": "",
        "experience": "",
        "role": "",
        "location": "",
        "tech_stack": "",
    }

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

#helpers
def bot_message(text, delay = 0.5):
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("TalentScout is typing...")
        time.sleep(delay)
        placeholder.markdown(text)
    st.session_state.chat_history.append(("assistant", text))

def user_message(text):
    with st.chat_message("user"):
        st.markdown(text)
    st.session_state.chat_history.append(("user", text))

def save_conversation(candidate, chat_history):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"

    data = {
        "candidate": candidate,
        "conversation": [
            {"role": role, "message": msg}
            for role, msg in chat_history
        ]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return filename

#rendering chat history
st.title("TalentScout — Initial Candidate Screening")

for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

#extract valid questions
def extract_valid_questions(llm_output, max_questions):
    raw_lines = [l.strip() for l in llm_output.split("\n") if l.strip()]
    questions = []

    for line in raw_lines:
        # Remove bullets or numbering
        line = line.lstrip("*- ").strip()
        if line[0].isdigit() and "." in line:
            line = line.split(".", 1)[1].strip()

        # Keep only real questions
        if "?" in line and len(line) > 15:
            questions.append(line)

        if len(questions) >= max_questions:
            break

    return questions


#conversation flow
if st.session_state.stage == "greeting":
    bot_message(
        "Hi, I'm TalentScount's hiring assistant. "
        "I'll ask a few questions to understand your background and then move to a short technical screening."
    )
    bot_message("to get started, What's your full name?")
    st.session_state.stage = "name"

user_input = None
if st.session_state.stage != "done":
    user_input = st.chat_input("Type your response here…")

if user_input:
    user_message(user_input)
    # Name 
    if st.session_state.stage == "name":
        st.session_state.candidate["name"] = user_input.strip()
        bot_message(f"Thanks, {st.session_state.candidate['name']}. What role are you applying for?")
        st.session_state.stage = "role"

    # Role 
    elif st.session_state.stage == "role":
        st.session_state.candidate["role"] = user_input.strip()
        bot_message("How many years of professional experience do you have?")
        st.session_state.stage = "experience"

    # Experience 
    elif st.session_state.stage == "experience":
        st.session_state.candidate["experience"] = user_input.strip()
        bot_message("Where are you currently located?")
        st.session_state.stage = "location"

    # Location 
    elif st.session_state.stage == "location":
        st.session_state.candidate["location"] = user_input.strip()
        bot_message(
            "Please list your primary technical skills or tech stack "
            "(for example: Python, SQL, Django)."
        )
        st.session_state.stage = "tech_stack"

    # Tech Stack 
    elif st.session_state.stage == "tech_stack":
        tech_stack = [t.strip() for t in user_input.split(",") if t.strip()]
        st.session_state.candidate["tech_stack"] = tech_stack

        bot_message(
            "Great, thank you. I’ll now prepare a few technical questions based on your skills.",
            delay=1.2
        )

        with st.spinner("Preparing relevant technical questions…"):
            prompt = technical_question_prompt(tech_stack)
            llm_output = generate_response(prompt)

        max_q = max(2, len(tech_stack) * 2)

        questions = extract_valid_questions(llm_output, max_q)

        if not questions:
            bot_message(
                "I wasn’t able to generate valid questions. "
                "Thank you for your time — our team will follow up separately."
            )
            st.session_state.stage = "done"
        else:
            st.session_state.questions = questions
            st.session_state.current_question = 0

            bot_message("Let’s begin the technical screening.")
            bot_message(st.session_state.questions[0])
            st.session_state.stage = "tech_questions"

    # Technical Questions 
    elif st.session_state.stage == "tech_questions":
        bot_message("Thanks, noted.", delay=0.6)

        st.session_state.current_question += 1

        if st.session_state.current_question < len(st.session_state.questions):
            bot_message(
                st.session_state.questions[st.session_state.current_question]
            )
        else:
            filename = save_conversation(
                st.session_state.candidate,
                st.session_state.chat_history
            )

            bot_message(
                "That concludes the initial screening.\n\n"
                "Thank you for your responses. Our recruitment team will review them "
                "and reach out regarding the next steps.\n\n"
                "You may now close this window."
            )

            st.session_state.stage = "done"