import ast
import operator
import re
from urllib.request import urlopen, Request
from urllib.error import URLError
import os

# --- Tool 1: Safe Calculator ---
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers allowed")
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            left = safe_eval(node.left)
            right = safe_eval(node.right)
            return SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](safe_eval(node.operand))
        raise ValueError(f"Unsupported operator: {op_type.__name__}")
    raise ValueError(f"Unsupported expression: {type(node).__name__}")

def calculator(expression: str) -> str:
    """Safely evaluates a basic mathematical expression using AST."""
    try:
        expr = expression.strip()
        tree = ast.parse(expr, mode='eval')
        result = safe_eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# --- Tool 2: Read Webpage ---
def read_webpage(url: str) -> str:
    """Reads content from a URL or a local file path and strips HTML tags."""
    try:
        if url.startswith(("http://", "https://")):
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=10) as response:
                html = response.read().decode("utf-8", errors="ignore")
        elif os.path.exists(url):
            with open(url, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
        else:
            return f"Error: File or URL not found: {url}"

        # Simple HTML tag stripping
        text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
        text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        clean_text = " ".join(text.split())
        return clean_text
    except Exception as e:
        return f"Error reading page: {str(e)}"

# --- Tool Registry & Schema for Groq/OpenAI function calling ---
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "read_webpage": read_webpage,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate basic arithmetic operations safely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to calculate, e.g., '(12000 + 18000) * 0.9'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": "Fetch and extract text content from a web URL or local file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL or local path to read"
                    }
                },
                "required": ["url"]
            }
        }
    }
]