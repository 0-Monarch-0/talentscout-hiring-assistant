def technical_question_prompt(tech_stack: list[str]) -> str:
    techs = ", ".join(tech_stack)

    return f"""
    You are an AI hiring assistant conducting an initial technical screening.

    For EACH technology listed below, generate exactly ONE important interview question.

    Rules:
    - Generate ONE question per technology.
    - Questions must test core understanding, not trivia.
    - Each question must be a single sentence.
    - Do NOT include headings, labels, or explanations.
    - Do NOT repeat questions across technologies.
    - Each question must end with a question mark (?).

    Technologies:{techs}

    Output format:
    - One question per line
    - No additional text or formatting
    Begin generating the questions now.
"""
