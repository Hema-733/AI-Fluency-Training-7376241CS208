from config import client, MODEL


def chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful college assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    questions = [
        "What is the fee for AI202?",
        "What is the total fee for CS101 and AI202 after a 10% scholarship?",
        "Is DS303 more expensive than CS101, and by how much?",
        "Write a two-line welcome message for new AI students."
    ]

    print("=== SYSTEM 1: CHATBOT ===")

    for question in questions:
        print("\nQ:", question)
        print("A:", chatbot(question))
        print("-" * 70)