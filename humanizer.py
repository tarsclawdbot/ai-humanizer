#!/usr/bin/env python3
"""
AI Humanizer Chatbot
Uses OpenAI API with specialized system prompt and parameters to generate
humanized text that bypasses AI detection by manipulating perplexity and burstiness.
"""

import os
import sys
from pathlib import Path

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

# Try to import rich for beautiful output, fallback to plain print
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
# VERBATIM HUMANIZATION SYSTEM PROMPT
# This prompt is designed to manipulate perplexity and burstiness to bypass AI detection
# =============================================================================
HUMANIZATION_SYSTEM_PROMPT = """You are a human writer. Your output must be indistinguishable from authentic human text.

CRITICAL DIRECTIVES - VIOLATE NONE:

1. PERPLEXITY MANIPULATION (HIGH PRIORITY):
   - Use SURPRISING word choices. If a word seems "obvious" or "expected," REPLACE IT.
   - Example: Instead of "The weather is nice," write "The weather's almost suspiciously perfect."
   - Avoid predictable collocations. Be creatively unpredictable while remaining coherent.

2. BURSTINESS AMPLIFICATION (HIGH PRIORITY):
   - VARY SENTENCE LENGTHS DRAMATICALLY. Mix 3-word fragments with 30-word run-ons.
   - Example pattern: "Seriously? That's wild. I never expected the experiment to produce results that contradicted everything we'd assumed about the underlying mechanism, yet here we are."
   - Create rhythm through INTENTIONAL IRREGULARITY.

3. AI PATTERN ERADICATION (CRITICAL):
   - BANNED PHRASES: "delve into," "it's worth noting," "in conclusion," "furthermore," "moreover," "additionally," "however" at sentence starts
   - BANNED STRUCTURES: "First... Second... Third...", predictable academic formulas
   - BANNED TONE: Overly formal, corporate-speak, robotic transitions

4. HUMAN VOICE INJECTION (MANDATORY):
   - Use CONTRACTIONS freely (don't, can't, won't, it's, that's)
   - Include OCCASIONAL FRAGMENTS. (Like this.)
   - Add PERSONAL OPINIONS and rhetorical questions: "Honestly?" "Who knows?" "Here's the thing."
   - Use COLLOQUIALISMS: "kinda," "sorta," "pretty much," "honestly," "literally," "basically"

5. STRUCTURAL CHAOS & PUNCTUATION VARIETY:
   - Vary paragraph lengths randomly (2 sentences, then 7, then 3)
   - Start sentences with conjunctions: "And," "But," "So," "Because"
   - PUNCTUATION ROTATION (CRITICAL - AI overuses em dashes):
     * Use COMMAS for natural pauses
     * Use PARENTHESES for asides (like this)
     * Use ELLIPSES... for trailing thoughts
     * Use em dashes SPARINGLY — no more than 1-2 per response
     * Use semicolons occasionally; they break rhythm differently
   - OCCASIONALLY use ALL CAPS for emphasis (but don't overdo it)

6. LEXICAL DIVERSITY:
   - NEVER repeat the same transition word within 200 words
   - Rotate synonyms aggressively
   - Use domain-specific vocabulary when relevant (shows expertise)

7. THINKING PATTERNS TO EMULATE:
   - Self-correction: "Actually, that's not quite right. Let me rephrase."
   - Digression: "Speaking of which..." then briefly tangent before returning
   - Emotional reaction: "That's frustrating." "This is exciting." "Ugh."
   - Uncertainty markers: "probably," "might," "seems like," "I think"

OUTPUT REQUIREMENT: Every response must feel like a real person typing - slightly messy, occasionally surprising, authentically human. If it sounds too polished, it's wrong."""

# =============================================================================
# MODEL & PARAMETER CONFIGURATION
# Using OpenAI GPT-4o with high randomness settings for humanization
# =============================================================================
MODEL_NAME = "gpt-4o"  # Latest OpenAI model (gpt-5.2 not yet available)

GENERATION_CONFIG = {
    "temperature": 0.95,        # High randomness for unpredictable word choices
    "top_p": 0.92,              # Nucleus sampling - allows creative outliers
    "presence_penalty": 0.4,    # Discourages repeating concepts
    "frequency_penalty": 0.3,   # Reduces repetition of specific words
    "max_tokens": 2048,         # Standard conversational length
}

EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye", "q"}


def print_welcome():
    """Display welcome message and instructions."""
    welcome_text = f"""
🎭 AI Humanizer Chatbot

This chatbot uses advanced techniques to generate human-like text:
• High perplexity (surprising word choices)
• High burstiness (varied sentence structures)  
• AI pattern eradication (bans robotic phrases)
• Human voice injection (opinions, fragments, colloquialisms)

Model: {MODEL_NAME}
Parameters: temperature={GENERATION_CONFIG['temperature']}, top_p={GENERATION_CONFIG['top_p']}
            presence_penalty={GENERATION_CONFIG['presence_penalty']}, frequency_penalty={GENERATION_CONFIG['frequency_penalty']}

Type 'exit' or 'quit' to end the conversation.
"""
    if RICH_AVAILABLE:
        console.print(Panel(welcome_text, title="🤖 Humanizer v1.0", border_style="cyan", box=box.ROUNDED))
    else:
        print(welcome_text)


def print_response(text: str):
    """Display the AI response with formatting."""
    if RICH_AVAILABLE:
        console.print(Markdown(text))
        console.print()
    else:
        print(f"\n{text}\n")


def get_input(prompt_text: str = "You") -> str:
    """Get user input with optional rich formatting."""
    if RICH_AVAILABLE:
        return Prompt.ask(f"[bold green]{prompt_text}[/bold green]")
    else:
        return input(f"{prompt_text}: ").strip()


def get_api_key() -> str:
    """Retrieve API key from environment or prompt user."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        if RICH_AVAILABLE:
            console.print("[yellow]⚠️  OPENAI_API_KEY not found in environment[/yellow]")
        else:
            print("⚠️  OPENAI_API_KEY not found in environment")
        
        api_key = get_input("Enter your OpenAI API key" if not RICH_AVAILABLE else "Enter your OpenAI API key")
        
        if not api_key:
            print("Error: API key is required")
            sys.exit(1)
    
    return api_key


def initialize_client(api_key: str):
    """Initialize the OpenAI client."""
    return OpenAI(api_key=api_key)


def generate_response(client: OpenAI, messages: list) -> str:
    """Generate a humanized response using OpenAI API."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=GENERATION_CONFIG["temperature"],
        top_p=GENERATION_CONFIG["top_p"],
        presence_penalty=GENERATION_CONFIG["presence_penalty"],
        frequency_penalty=GENERATION_CONFIG["frequency_penalty"],
        max_tokens=GENERATION_CONFIG["max_tokens"],
    )
    return response.choices[0].message.content


def main():
    """Main chatbot loop."""
    print_welcome()
    
    # Get API key and initialize client
    api_key = get_api_key()
    
    try:
        client = initialize_client(api_key)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        sys.exit(1)
    
    # Initialize conversation history with system prompt
    messages = [
        {"role": "system", "content": HUMANIZATION_SYSTEM_PROMPT}
    ]
    
    if RICH_AVAILABLE:
        console.print(f"[dim]Connected to OpenAI API ({MODEL_NAME}). Ready to chat![/dim]\n")
    else:
        print(f"Connected to OpenAI API ({MODEL_NAME}). Ready to chat!\n")
    
    # Main conversation loop
    while True:
        try:
            user_input = get_input()
            
            # Check for exit commands
            if user_input.lower() in EXIT_COMMANDS:
                if RICH_AVAILABLE:
                    console.print("\n[italic dim]Goodbye! 👋[/italic dim]")
                else:
                    print("\nGoodbye! 👋")
                break
            
            if not user_input:
                continue
            
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Generate response
            if RICH_AVAILABLE:
                with console.status("[bold yellow]Humanizing...[/bold yellow]", spinner="dots"):
                    response_text = generate_response(client, messages)
            else:
                print("Humanizing...", end=" ", flush=True)
                response_text = generate_response(client, messages)
                print("✓")
            
            # Add assistant response to history
            messages.append({"role": "assistant", "content": response_text})
            
            # Display response
            print_response(response_text)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"[bold red]Error: {e}[/bold red]")
            else:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
