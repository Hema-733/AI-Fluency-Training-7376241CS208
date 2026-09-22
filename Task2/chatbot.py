from config import client, MODEL

PRIVATE_DATA = """
College Placement Eligibility Rules:
General eligibility:
- CGPA must be at least 7.0
- No active backlogs
- Attendance must be at least 75%

Company requirements:
- Company A: CGPA >= 7.5, no active backlog
- Company B: CGPA >= 7.0, no active backlog
- Company C: CGPA >= 8.0, no active backlog
"""


def chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Answer using the following private college placement data:\n"
                           + PRIVATE_DATA
            },
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    questions = [
        "What are the general placement eligibility requirements?",
        "Can a student with 7.6 CGPA and no backlog apply for Company A?",
        "Can a student with 7.6 CGPA apply for Company C?",
        "A student has 7.8 CGPA, no backlog and 80% attendance. Which companies can they apply for?"
    ]

    print("=== TASK 2: CHATBOT ===")

    for q in questions:
        print("\nQ:", q)
        print("A:", chatbot(q))
        