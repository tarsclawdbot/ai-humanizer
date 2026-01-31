#!/usr/bin/env python3
"""
AI Humanizer Chatbot
Uses Gemini API with specialized system prompt and parameters to generate
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
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai not installed. Run: pip install google-generativeai")
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

5. STRUCTURAL CHAOS:
   - Vary paragraph lengths randomly (2 sentences, then 7, then 3)
   - Start sentences with conjunctions: "And," "But," "So," "Because"
   - Use DASHES and ELLIPSES... for effect.
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
# INFERENCE PARAMETERS FOR HUMAN-LIKE GENERATION
# These parameters are tuned to increase randomness and reduce AI predictability
# =============================================================================
GENERATION_CONFIG = {
    "temperature": 0.95,        # High randomness for unpredictable word choices
    "top_p": 0.92,              # Nucleus sampling - allows creative outliers
    "top_k": 50,                # Broad vocabulary sampling
    "presence_penalty": 0.4,    # Discourages repeating concepts
    "frequency_penalty": 0.3,   # Reduces repetition of specific words
    "max_output_tokens": 2048,  # Standard conversational length
}

EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye", "q"}


def print_welcome():
    """Display welcome message and instructions."""
    welcome_text = """
🎭 AI Humanizer Chatbot

This chatbot uses advanced techniques to generate human-like text:
• High perplexity (surprising word choices)
• High burstiness (varied sentence structures)  
• AI pattern eradication (bans robotic phrases)
• Human voice injection (opinions, fragments, colloquialisms)

Parameters: temperature=0.95, top_p=0.92, top_k=50
            presence_penalty=0.4, frequency_penalty=0.3

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
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        if RICH_AVAILABLE:
            console.print("[yellow]⚠️  GEMINI_API_KEY not found in environment[/yellow]")
        else:
            print("⚠️  GEMINI_API_KEY not found in environment")
        
        api_key = get_input("Enter your Gemini API key" if not RICH_AVAILABLE else "Enter your Gemini API key")
        
        if not api_key:
            print("Error: API key is required")
            sys.exit(1)
    
    return api_key


def initialize_model(api_key: str):
    """Initialize the Gemini model with humanization settings."""
    genai.configure(api_key=api_key)
    
    # Configure the model with system instruction
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction=HUMANIZATION_SYSTEM_PROMPT,
        generation_config=GENERATION_CONFIG
    )
    
    return model


def main():
    """Main chatbot loop."""
    print_welcome()
    
    # Get API key and initialize model
    api_key = get_api_key()
    
    try:
        model = initialize_model(api_key)
    except Exception as e:
        print(f"Error initializing model: {e}")
        sys.exit(1)
    
    # Start chat session with history
    chat = model.start_chat(history=[])
    
    if RICH_AVAILABLE:
        console.print("[dim]Connected to Gemini API. Ready to chat![/dim]\n")
    else:
        print("Connected to Gemini API. Ready to chat!\n")
    
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
            
            # Generate response
            if RICH_AVAILABLE:
                with console.status("[bold yellow]Humanizing...[/bold yellow]", spinner="dots"):
                    response = chat.send_message(user_input)
            else:
                print("Humanizing...", end=" ", flush=True)
                response = chat.send_message(user_input)
                print("✓")
            
            # Display response
            print_response(response.text)
            
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
