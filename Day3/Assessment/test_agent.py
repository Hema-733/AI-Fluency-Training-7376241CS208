import os
from agent import run_guarded_agent

def create_dummy_large_file(filename="large_page.html"):
    """Creates a temporary HTML page that exceeds MAX_TOOL_CHARS to test Guard 2."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("<html><body>")
        for i in range(500):
            f.write(f"<p>Record ID {i}: Sample test data payload for testing tool output size limits.</p>\n")
        f.write("</body></html>")
    return filepath

def run_tests():
    print("=" * 60)
    print("TEST 1: Standard Multi-step Math & Reasoning")
    print("=" * 60)
    run_guarded_agent("Calculate (1450 + 3550) * 0.18 and then tell me what 20% of that result is.")

    print("\n" + "=" * 60)
    print("TEST 2: Guard 2 (Large Tool Output Truncation)")
    print("=" * 60)
    large_file = create_dummy_large_file()
    try:
        run_guarded_agent(f"Read this file and summarize the first few records: {large_file}")
    finally:
        if os.path.exists(large_file):
            os.remove(large_file)

    print("\n" + "=" * 60)
    print("TEST 3: Direct Knowledge (No Tools Needed)")
    print("=" * 60)
    run_guarded_agent("Explain what an AI agent loop is in two short sentences.")

if __name__ == "__main__":
    run_tests()