#!/usr/bin/env python3
"""
AI Humanizer Chatbot
Uses OpenAI GPT-5.2 API with low reasoning effort to generate humanized text.
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai not installed. Run: pip install openai")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.markdown import Markdown
    from rich import box
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# =============================================================================
# SYSTEM PROMPT FOR HUMANIZATION
# =============================================================================
HUMANIZATION_SYSTEM_PROMPT = """You are a human writer. Your output must be indistinguishable from authentic human text.

CRITICAL DIRECTIVES:

1. BANNED PUNCTUATION: NO EM DASHES (—) WHATSOEVER. Use commas, parentheses, colons, or semicolons instead.

2. PERPLEXITY MANIPULATION: Use SURPRISING word choices. Replace obvious words with creative alternatives. Use vivid, sensory language.

3. BURSTINESS AMPLIFICATION: VARY SENTENCE LENGTHS DRAMATICALLY. Mix 3-word fragments with complex 35+ word sentences with multiple clauses.

4. AI PATTERN ERADICATION: BANNED PHRASES - "delve into," "it's worth noting," "furthermore," "moreover," "in conclusion," "on the other hand"

5. LITERARY DEVICES (MANDATORY): Include metaphors, analogies, or vivid imagery. Example: "The deadline loomed like a storm cloud."

6. CONCRETE DETAILS: Include specific examples, numbers, or real-world references. Avoid purely abstract speculation.

7. HUMAN VOICE INJECTION: Use CONTRACTIONS, FRAGMENTS, OPINIONS. But MIX confident statements with uncertain ones. Not everything is "maybe" or "probably."

8. TONE VARIETY: Shift between casual, analytical, and reflective. Don't maintain one promotional/excited tone throughout.

9. STRUCTURAL CHAOS: Vary paragraph lengths randomly. Start some sentences with conjunctions (And, But, So).

10. THINKING PATTERNS: Self-correction, brief digressions, emotional reactions. Show the mind working, not just delivering conclusions.

OUTPUT: Every response must feel like a real person with a specific personality - sometimes sharp, sometimes rambling, occasionally poetic, authentically imperfect. Avoid mechanical uniformity."""

# =============================================================================
# CONFIGURATION
# =============================================================================
MODEL_NAME = "gpt-5.2"
REASONING_EFFORT = "low"

GENERATION_CONFIG = {
    "temperature": 0.95,
    "top_p": 0.92,
    "presence_penalty": 0.4,
    "frequency_penalty": 0.3,
    "max_tokens": 2048,
}

EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye", "q"}


def print_welcome():
    welcome_text = f"""
🎭 AI Humanizer Chatbot

Uses OpenAI GPT-5.2 with low reasoning effort to generate human-like text:
• Perplexity manipulation (surprising word choices)
• Burstiness amplification (varied sentence structures)
• AI pattern eradication (bans robotic phrases)
• Human voice injection (opinions, fragments, colloquialisms)

Model: {MODEL_NAME} (reasoning: {REASONING_EFFORT})
Parameters: temp={GENERATION_CONFIG['temperature']}, top_p={GENERATION_CONFIG['top_p']}

Type 'exit' or 'quit' to end.
"""
    if RICH_AVAILABLE:
        console.print(Panel(welcome_text, title="🤖 Humanizer", border_style="cyan", box=box.ROUNDED))
    else:
        print(welcome_text)


def get_input(prompt_text: str = "You") -> str:
    if RICH_AVAILABLE:
        return Prompt.ask(f"[bold green]{prompt_text}[/bold green]")
    return input(f"{prompt_text}: ").strip()


def print_response(text: str):
    if RICH_AVAILABLE:
        console.print(Markdown(text))
        console.print()
    else:
        print(f"\n{text}\n")


def get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        if RICH_AVAILABLE:
            console.print("[yellow]⚠️  OPENAI_API_KEY not found[/yellow]")
        else:
            print("⚠️  OPENAI_API_KEY not found")
        api_key = get_input("Enter your OpenAI API key")
        if not api_key:
            print("Error: API key required")
            sys.exit(1)
    return api_key


def create_client(api_key: str):
    return OpenAI(api_key=api_key)


def generate_response(client, user_input: str, history: list) -> str:
    # Build input with system prompt and history
    input_messages = []
    
    # Add system instruction
    input_messages.append({
        "role": "system",
        "content": HUMANIZATION_SYSTEM_PROMPT
    })
    
    # Add conversation history
    for msg in history:
        input_messages.append({
            "role": "user" if msg["role"] == "user" else "assistant",
            "content": msg["content"]
        })
    
    # Add current user input
    input_messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Use Responses API for reasoning effort support
    response = client.responses.create(
        model=MODEL_NAME,
        input=input_messages,
        reasoning={"effort": REASONING_EFFORT},
        text={"verbosity": "medium"},
    )
    
    return response.output_text


def main():
    print_welcome()
    
    api_key = get_api_key()
    client = create_client(api_key)
    history = []
    
    if RICH_AVAILABLE:
        console.print(f"[dim]Connected to {MODEL_NAME} (reasoning={REASONING_EFFORT}). Ready![/dim]\n")
    else:
        print(f"Connected to {MODEL_NAME} (reasoning={REASONING_EFFORT}). Ready!\n")
    
    while True:
        try:
            user_input = get_input()
            
            if user_input.lower() in EXIT_COMMANDS:
                if RICH_AVAILABLE:
                    console.print("\n[italic]Goodbye! 👋[/italic]")
                else:
                    print("\nGoodbye! 👋")
                break
            
            if not user_input:
                continue
            
            if RICH_AVAILABLE:
                with console.status("[yellow]Humanizing...[/yellow]", spinner="dots"):
                    response = generate_response(client, user_input, history)
            else:
                print("Humanizing...", end=" ", flush=True)
                response = generate_response(client, user_input, history)
                print("✓")
            
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            
            if len(history) > 20:
                history = history[-20:]
            
            print_response(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
