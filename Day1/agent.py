import json

from config import client, MODEL
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a helpful college fee assistant.

Use the available tools whenever you need accurate course fee information
or calculations.

Do not guess course fees.

Continue using tools until you have enough information to answer the user.
"""


def agent(question):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for step in range(6):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content.strip()

        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(
                f"Step {step + 1}: "
                f"{tool_name}({arguments})"
            )

            result = TOOL_FUNCTIONS[tool_name](**arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "Agent stopped: maximum steps reached."


if __name__ == "__main__":

    questions = [
        "What is the fee for AI202?",
        "What is the total fee for CS101 and AI202 after a 10% scholarship?",
        "Is DS303 more expensive than CS101, and by how much?",
        "Write a two-line welcome message for new AI students."
    ]

    print("=== SYSTEM 3: AI AGENT ===")

    for question in questions:
        print("\nQ:", question)
        print("A:", agent(question))
        print("-" * 70)