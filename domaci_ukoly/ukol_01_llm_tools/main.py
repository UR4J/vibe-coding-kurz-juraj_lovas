"""
Domácí úkol č. 1: Python skript pro LLM API s nástrojem.

  1. the script sends a question to the LLM (Anthropic Messages API) with the tool definitions
  2. the LLM answers with tool_use: which tool, with which arguments
  3. the script runs the tool (a calculation function in tools.py)
  4. the result goes back to the LLM as tool_result
  5. repeat 2-4 until the LLM answers with text only

Use case: how much a headhunter invoices for a placement (fee and VAT).

Run:
  uv run main.py                         # two demo questions
  uv run main.py "your own question"     # any question
"""

import json
import os
import sys

import anthropic
from dotenv import load_dotenv

from tools import FUNCTIONS, TOOLS

load_dotenv()

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
MAX_STEPS = 5  # safety limit for the tool loop

SYSTEM = (
    "Si asistent headhuntera v Neohunter. Na každý výpočet použi nástroje, "
    "nikdy nepočítaj sám. Odpovedaj po slovensky, stručne, sumy v EUR na dve desatinné miesta."
)

DEMO_QUESTIONS = [
    "Kandidát nastupuje ako regionálny manažér predaja s platom 3 800 € brutto mesačne, "
    "firma vypláca aj 13. plat. Náš fee je 18 % z ročného platu. "
    "Koľko budeme fakturovať bez DPH a s DPH?",
    "Klient váha medzi dvoma kandidátmi. A chce 4 200 € mesačne (12 platov), "
    "B chce 3 900 € mesačne (14 platov). Pri fee 20 %: na ktorom zarobíme viac a o koľko?",
]

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("Chýba ANTHROPIC_API_KEY: skopíruj .env.example na .env a vlož kľúč.")

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment / .env


def run_tool(name: str, arguments: dict) -> tuple[str, bool]:
    """Run one tool. Errors go back to the LLM as text, so it can fix its call."""
    function = FUNCTIONS.get(name)
    if function is None:
        return f"Unknown tool: {name}", True
    try:
        return json.dumps(function(**arguments)), False
    except (TypeError, ValueError) as error:
        return f"Invalid arguments for {name}: {error}", True


def ask(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    for step in range(1, MAX_STEPS + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )

        tool_calls = [block for block in response.content if block.type == "tool_use"]
        if not tool_calls:
            # No tool needed any more: this is the final answer
            return "".join(block.text for block in response.content if block.type == "text")

        # Keep the assistant turn exactly as returned (incl. thinking blocks)
        messages.append({"role": "assistant", "content": response.content})

        # Run every requested tool and send ALL results back in one user message
        results = []
        for call in tool_calls:
            output, is_error = run_tool(call.name, call.input)
            print(f"  [krok {step}] {call.name}({call.input}) -> {output}")
            results.append({
                "type": "tool_result",
                "tool_use_id": call.id,
                "content": output,
                "is_error": is_error,
            })
        messages.append({"role": "user", "content": results})

    return f"Chyba: model nedal odpoveď ani po {MAX_STEPS} krokoch."


if __name__ == "__main__":
    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else DEMO_QUESTIONS
    for question in questions:
        print(f"\nOTÁZKA: {question}")
        print(f"\nODPOVEĎ:\n{ask(question)}\n")
        print("-" * 80)
