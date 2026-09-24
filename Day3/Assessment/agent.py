import json
from config import client, MODEL
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = """You are a helpful and precise assistant equipped with tools.
Use the provided tools when you need to calculate expressions or fetch web/file content.
Always provide a concise final answer once you have gathered sufficient information."""

# --- Guard Thresholds ---
MAX_STEPS = 6              # Hard step exit
MAX_TOOL_CHARS = 1500      # Guard 2: Single tool output truncation
CHAR_BUDGET = 30000        # Guard 3: Total character budget for context/cost control
MAX_REPEAT_LIMIT = 3       # Guard 1: Max times exact same call can repeat

def run_guarded_agent(user_query: str):
    print(f"\n--- Starting Agent Run: '{user_query}' ---")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    seen_calls = {}          # Tracks tool + arg repetitions (Guard 1)
    total_chars_used = 0     # Tracks total character budget (Guard 3)

    for step in range(1, MAX_STEPS + 1):
        print(f"\n[Step {step}/{MAX_STEPS}]")

        # Call LLM
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message)

        # Check if the LLM reached a final text answer without tool calls
        if not response_message.tool_calls:
            print("\nFinal Answer:")
            print(response_message.content)
            return response_message.content

        # Handle tool calls
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            raw_args = tool_call.function.arguments

            # ------------------------------------------------------------------
            # GUARD 1: Repeat Tool Call Detection
            # ------------------------------------------------------------------
            call_signature = f"{function_name}:{raw_args}"
            seen_calls[call_signature] = seen_calls.get(call_signature, 0) + 1

            if seen_calls[call_signature] >= MAX_REPEAT_LIMIT:
                print(f"[GUARD 1 TRIGGERED] Loop detected: {call_signature} called {seen_calls[call_signature]} times.")
                tool_output = f"Error: Tool call repeated {MAX_REPEAT_LIMIT} times. Action aborted to break infinite loop."
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": tool_output
                })
                continue

            # Execute tool
            if function_name in TOOL_FUNCTIONS:
                try:
                    args = json.loads(raw_args)
                    tool_func = TOOL_FUNCTIONS[function_name]
                    tool_output = str(tool_func(**args))
                except Exception as e:
                    tool_output = f"Error executing tool {function_name}: {str(e)}"
            else:
                tool_output = f"Error: Unknown tool '{function_name}'."

            # ------------------------------------------------------------------
            # GUARD 2: Tool Output Limit (Truncation)
            # ------------------------------------------------------------------
            if len(tool_output) > MAX_TOOL_CHARS:
                print(f"[GUARD 2 TRIGGERED] Output truncated from {len(tool_output)} to {MAX_TOOL_CHARS} chars.")
                tool_output = tool_output[:MAX_TOOL_CHARS] + "\n...[TRUNCATED: Output exceeded character limit]"

            # ------------------------------------------------------------------
            # GUARD 3: Total Character Budget Check
            # ------------------------------------------------------------------
            total_chars_used += len(tool_output)
            print(f"Tool: {function_name} | Observation len: {len(tool_output)} | Total budget used: {total_chars_used}/{CHAR_BUDGET}")

            if total_chars_used > CHAR_BUDGET:
                print(f"[GUARD 3 TRIGGERED] Total character budget exceeded ({total_chars_used} > {CHAR_BUDGET}). Stopping run.")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": "Context budget exceeded. Please provide your best final response based on available data."
                })
                # Prompt final wrap-up call
                final_res = client.chat.completions.create(
                    model=MODEL,
                    messages=messages
                )
                print("\nFinal Answer (forced stop):")
                print(final_res.choices[0].message.content)
                return final_res.choices[0].message.content

            # Append valid observation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": tool_output
            })

    print(f"\n[SAFETY EXIT] Reached maximum allowed steps ({MAX_STEPS}).")
    return "Agent terminated: maximum step limit reached without final conclusion."

if __name__ == "__main__":
    # Test query requiring calculator tool
    run_guarded_agent("What is (250 * 4) + 1350 * 0.15?")