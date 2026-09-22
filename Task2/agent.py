import json

from config import client, MODEL
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a college placement eligibility agent.

Use the provided tools to check private placement rules.
Do not guess eligibility.
Use tools whenever the question requires checking eligibility.
"""


def agent(question):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for step in range(5):

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

            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"Step {step + 1}: {name}({arguments})")

            result = TOOL_FUNCTIONS[name](**arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "Agent stopped after maximum steps."


if __name__ == "__main__":

    questions = [
        "I have 7.6 CGPA, no backlog and 80% attendance. Which companies can I apply for?",
        "I have 8.2 CGPA, no backlog and 80% attendance. Which companies can I apply for?",
        "I have 7.8 CGPA, no backlog and 70% attendance. Can I apply for Company A?"
    ]

    print("=== TASK 2: AI AGENT ===")

    for q in questions:
        print("\nQ:", q)
        print("A:", agent(q))
        print("-" * 60)