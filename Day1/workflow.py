
COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


def workflow(question):
    q = question.lower()

    if "fee for ai202" in q:
        return "The fee for AI202 is Rs. 18,000."

    if "total fee" in q and "cs101" in q and "ai202" in q:
        total = (COURSE_FEES["CS101"] + COURSE_FEES["AI202"]) * 0.9
        return f"The total fee after a 10% scholarship is Rs. {total:.0f}."

    if "ds303" in q and "cs101" in q and "more expensive" in q:
        difference = COURSE_FEES["DS303"] - COURSE_FEES["CS101"]
        return f"Yes. DS303 costs Rs. {difference:,} more than CS101."

    if "welcome" in q and "ai students" in q:
        return (
            "Welcome to the AI programme!\n"
            "Ask questions, build often, and enjoy every experiment."
        )

    return "Sorry, I don't have a rule for that question."


if __name__ == "__main__":

    questions = [
        "What is the fee for AI202?",
        "What is the total fee for CS101 and AI202 after a 10% scholarship?",
        "Is DS303 more expensive than CS101, and by how much?",
        "Write a two-line welcome message for new AI students."
    ]

    print("=== SYSTEM 2: RULE-BASED WORKFLOW ===")

    for question in questions:
        print("\nQ:", question)
        print("A:", workflow(question))
        print("-" * 70)