#!/usr/bin/env python3
"""
AI Humanizer Chatbot
Uses Gemini API with specialized system prompt and parameters to generate
humanized text that bypasses AI detection by manipulating perplexity and burstiness.

Usage:
    export GEMINI_API_KEY="your-key"
    python humanizer.py
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)

# Try to import rich for beautiful output
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
# MODEL & GENERATION CONFIGURATION
# =============================================================================
MODEL_NAME = "gemini-2.5-pro-preview-06-05"

EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye", "q"}


def print_welcome():
    """Display welcome message."""
    welcome_text = f"""
🎭 AI Humanizer Chatbot

This chatbot generates human-like text by manipulating:
• Perplexity (surprising word choices)
• Burstiness (varied sentence structures)
• AI pattern eradication (bans robotic phrases)
• Human voice injection (opinions, fragments, colloquialisms)

Model: {MODEL_NAME}
Parameters: temperature=0.95, top_p=0.92, top_k=50

Type 'exit' or 'quit' to end.
"""
    if RICH_AVAILABLE:
        console.print(Panel(welcome_text, title="🤖 Humanizer", border_style="cyan", box=box.ROUNDED))
    else:
        print(welcome_text)


def get_input(prompt_text: str = "You") -> str:
    """Get user input."""
    if RICH_AVAILABLE:
        return Prompt.ask(f"[bold green]{prompt_text}[/bold green]")
    return input(f"{prompt_text}: ").strip()


def print_response(text: str):
    """Display response."""
    if RICH_AVAILABLE:
        console.print(Markdown(text))
        console.print()
    else:
        print(f"\n{text}\n")


def get_api_key() -> str:
    """Get API key from env or prompt."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        if RICH_AVAILABLE:
            console.print("[yellow]⚠️  GEMINI_API_KEY not found[/yellow]")
        else:
            print("⚠️  GEMINI_API_KEY not found")
        api_key = get_input("Enter your Gemini API key")
        if not api_key:
            print("Error: API key required")
            sys.exit(1)
    return api_key


def create_client(api_key: str):
    """Create Gemini client."""
    return genai.Client(api_key=api_key)


def generate_response(client, user_input: str, history: list) -> str:
    """Generate humanized response."""
    # Build conversation context
    contents = []
    
    # Add system instruction as first user message with system marker
    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=f"System: {HUMANIZATION_SYSTEM_PROMPT}")]
    ))
    contents.append(types.Content(
        role="model", 
        parts=[types.Part(text="Understood. I'll write like a human.")]
    ))
    
    # Add conversation history
    for msg in history:
        contents.append(types.Content(
            role=msg["role"],
            parts=[types.Part(text=msg["content"])]
        ))
    
    # Add current user input
    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=user_input)]
    ))
    
    # Configure generation parameters
    config = types.GenerateContentConfig(
        temperature=0.95,
        top_p=0.92,
        top_k=50,
        max_output_tokens=2048,
    )
    
    # Generate response
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    )
    
    return response.text


def main():
    """Main chat loop."""
    print_welcome()
    
    api_key = get_api_key()
    client = create_client(api_key)
    
    # Conversation history (alternating user/model messages)
    history = []
    
    if RICH_AVAILABLE:
        console.print(f"[dim]Connected to {MODEL_NAME}. Ready![/dim]\n")
    else:
        print(f"Connected to {MODEL_NAME}. Ready!\n")
    
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
            
            # Generate
            if RICH_AVAILABLE:
                with console.status("[yellow]Humanizing...[/yellow]", spinner="dots"):
                    response = generate_response(client, user_input, history)
            else:
                print("Humanizing...", end=" ", flush=True)
                response = generate_response(client, user_input, history)
                print("✓")
            
            # Update history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "model", "content": response})
            
            # Trim history (keep last 10 exchanges)
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
