"""
main.py — AI Email Generator with Conversational Memory

Features:
- Generate emails using LangChain and OpenAI.
- Support formal, informal, and neutral tones.
- Store previous interactions in memory.json.
- Load previous history across application runs.
- Use relevant history when generating new emails.

Usage:
    python main.py --context "Schedule a project meeting" --tone formal
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


# ==============================================================
# CONFIGURATION
# ==============================================================

# Load environment variables from .env
load_dotenv()

MODEL_NAME = "gpt-4o-mini"

VALID_TONES = ["formal", "informal", "neutral"]

# Store memory.json in the same directory as main.py
BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "memory.json"


# ==============================================================
# INITIALIZE THE LANGUAGE MODEL
# ==============================================================

def get_llm():
    """Initialize the OpenAI chat model."""

    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=0.7,
        timeout=60,
        max_retries=2
    )


# ==============================================================
# MEMORY FUNCTIONS
# ==============================================================

def load_memory():
    """Load previous email interactions from memory.json."""

    if not MEMORY_FILE.exists():
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

        if not isinstance(memory, list):
            raise ValueError("Memory file must contain a JSON list.")

        return memory

    except (json.JSONDecodeError, OSError, ValueError) as exc:
        raise RuntimeError(
            f"Could not load conversation memory: {exc}"
        ) from exc


def save_memory(memory):
    """Save email interactions to memory.json."""

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            memory,
            f,
            indent=2,
            ensure_ascii=False
        )


def format_memory(memory: list) -> str:
    """Convert previous email interactions into readable text."""

    if not memory:
        return "No previous email conversations."

    lines = []

    for item in memory:
        lines.append(f"Previous context: {item['context']}")
        lines.append(f"Previous tone: {item['tone']}")
        lines.append(f"Previous email:\n{item['email']}")
        lines.append("-" * 40)

    return "\n".join(lines)


# ==============================================================
# CORE FUNCTION
# ==============================================================

def generate_email(
    context: str,
    tone: str = "neutral",
    memory: list | None = None
) -> str:
    """Generate an email using the current request and previous history."""

    # Validate context.
    if not isinstance(context, str) or not context.strip():
        raise ValueError("Email context cannot be empty.")

    # Validate tone.
    if tone not in VALID_TONES:
        raise ValueError(
            f"Invalid tone. Choose one of {VALID_TONES}."
        )

    # Validate API key.
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY is missing. Check your .env file."
        )

    if memory is None:
        memory = []

    # Format previous interactions.
    history = format_memory(memory)

    # Create the prompt.
    prompt = PromptTemplate.from_template(
        """
You are a professional AI email-writing assistant.

Use the previous email history only when it is relevant
to the current request.

PREVIOUS EMAIL HISTORY:
{history}

CURRENT EMAIL CONTEXT:
{context}

REQUESTED TONE:
{tone}

INSTRUCTIONS:
1. Generate a relevant subject line.
2. Include an appropriate greeting.
3. Write a clear email body in 2-3 paragraphs.
4. Match the requested tone.
5. Include an appropriate sign-off.
6. Reuse relevant details from previous emails when appropriate.
7. If the current request conflicts with older information,
   follow the current request.
8. Never invent names, dates, facts, or commitments.
9. Use placeholders such as [Recipient Name] or [Your Name]
   when information is missing.
10. Return only the completed email.

Generate the email now.
"""
    )

    # Initialize the LLM.
    llm = get_llm()

    # Build the LangChain LCEL pipeline.
    chain = prompt | llm

    # Invoke the model with history and current inputs.
    result = chain.invoke({
        "history": history,
        "context": context.strip(),
        "tone": tone
    })

    return result.content


# ==============================================================
# CLI ENTRY POINT
# ==============================================================

def main():
    """Parse arguments, generate an email, and save memory."""

    parser = argparse.ArgumentParser(
        description="AI Email Generator with Conversational Memory"
    )

    parser.add_argument(
        "--context",
        required=True,
        help="Describe what the email should be about."
    )

    parser.add_argument(
        "--tone",
        default="neutral",
        choices=VALID_TONES,
        help="Writing tone: formal, informal, or neutral."
    )

    args = parser.parse_args()

    try:
        # 1. Load previous interactions.
        memory = load_memory()

        print(f"\nPrevious interactions loaded: {len(memory)}")
        print(f"Memory file: {MEMORY_FILE}")
        print(f"\nGenerating a {args.tone} email...\n")
        print("=" * 60)

        # 2. Generate an email using previous history.
        email = generate_email(
            context=args.context,
            tone=args.tone,
            memory=memory
        )

        # 3. Display the email.
        print(email)

        # 4. Append the successful interaction.
        memory.append({
            "context": args.context,
            "tone": args.tone,
            "email": email
        })

        # 5. Persist the updated history.
        save_memory(memory)

        print("\n" + "=" * 60)
        print("Email generated successfully!")
        print(f"Conversation saved to: {MEMORY_FILE}")

    except Exception as exc:
        print(f"\nError: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()