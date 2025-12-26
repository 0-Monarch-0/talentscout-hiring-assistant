# TalentScout – Hiring Assistant (Initial Screening)

## Overview

This project implements a hiring assistant chatbot designed for **initial candidate screening**.  
The chatbot interacts with candidates in a conversational manner, collects basic background details, and conducts a short technical screening based on the candidate’s declared skill set.

The focus of this assignment is to demonstrate:
- controlled use of a large language model,
- clear prompt design,
- structured conversation flow,
- and a realistic user experience aligned with a hiring scenario.

---

## What the Chatbot Does

The chatbot follows a guided, step-by-step interaction:

1. Greets the candidate and explains the purpose of the screening.
2. Collects candidate details one at a time:
   - Full name  
   - Role applied for  
   - Years of experience  
   - Current location  
   - Technical skills / tech stack
3. Generates technical questions based on the provided skills.
4. Asks the technical questions **one by one**, maintaining context.
5. Acknowledges each response without evaluating or scoring it.
6. Ends the session with a professional closing message.

This reflects how an initial screening assistant would typically operate before a full interview round.

---

## Design Decisions

### Conversational Flow

Instead of using static forms, the application uses a chat-style interface where:
- the assistant asks one question at a time,
- the user responds naturally,
- and the conversation progresses in a controlled sequence.

This makes the interaction feel closer to a real recruiter-led screening.

---

### Technical Question Generation

- Technical questions are generated **once per session**.
- Each listed skill receives at least one relevant question.
- Only valid interview questions are presented (headings and formatting artifacts are filtered out).

The chatbot does not attempt to judge or analyze candidate answers, as evaluation is outside the scope of initial screening.

---

### Language Model Usage

- The application uses an open-source language model (**TinyLlama**) via **Ollama**, running locally.
- No paid APIs or cloud services are required.
- The model is used strictly for question generation, not for conversation control.

This keeps the system lightweight, cost-free, and predictable.

---

## Data Handling

- Candidate details and chat messages are stored temporarily in memory during the session.
- At the end of the screening, the full conversation is saved locally as a JSON file for demonstration purposes.
- No data is persisted beyond the session or transmitted externally.

This approach aligns with basic data-privacy principles while keeping the implementation simple.

---

## Project Structure

```
talentscout-hiring-assistant/
│
├── app.py          # Main Streamlit application
├── llm.py          # Local LLM interface (Ollama)
├── prompts.py      # Prompt templates for question generation
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.9 or above
- Ollama installed locally

### Installation Steps

```bash
# Clone the repository
git clone <your-repository-link>
cd talentscout-hiring-assistant

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull the language model
ollama pull tinyllama

# Run the application
streamlit run app.py
```

The application will be available at:
```
http://localhost:8501
```

---

## Demo

A short demo video demonstrates:
- conversational onboarding,
- technical question flow,
- and session completion.

**Demo link:** *(add your Loom link here)*

---

## Challenges Faced

- **LLM output formatting**  
  Language model responses can include headings or non-question text.  
  This was handled by filtering and validating generated questions before presenting them.

- **Performance on limited hardware**  
  To keep response times reasonable on a CPU-only system, model calls were minimized and the interaction flow was carefully structured.

---

## Possible Improvements

- Resume upload with automatic detail extraction  
- Cloud deployment for improved latency  
- Multilingual support  
- Structured storage for candidate responses  

These enhancements were intentionally kept out of scope for this assignment.

---

## Conclusion

This project demonstrates a practical and controlled use of a language model within a hiring assistant chatbot.  
The emphasis is on clarity, reliability, and realistic interaction rather than feature overload.
