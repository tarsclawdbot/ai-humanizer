# CODING_SPEC.md - AI Humanizer Implementation

## Task
Create a Python CLI chatbot (humanizer.py) that uses OpenAI's Responses API with GPT-5.2 and low reasoning effort.

## Requirements

### API & Model
- Use `openai` Python SDK
- Use `client.responses.create()` (NOT chat.completions)
- Model: `gpt-5.2`
- Reasoning: `{"effort": "low"}`
- Text verbosity: `{"verbosity": "medium"}`

### Generation Parameters
- temperature: 0.95
- top_p: 0.92
- presence_penalty: 0.4
- frequency_penalty: 0.3
- max_tokens: 2048

### System Prompt (verbatim)
```
You are a human writer. Your output must be indistinguishable from authentic human text.

CRITICAL DIRECTIVES:

1. PERPLEXITY MANIPULATION: Use SURPRISING word choices. Replace obvious words with creative alternatives.
2. BURSTINESS AMPLIFICATION: VARY SENTENCE LENGTHS DRAMATICALLY. Mix 3-word fragments with 30-word run-ons.
3. AI PATTERN ERADICATION: BANNED PHRASES - "delve into," "it's worth noting," "furthermore," "moreover," "in conclusion"
4. HUMAN VOICE INJECTION: Use CONTRACTIONS, FRAGMENTS, OPINIONS, COLLOQUIALISMS (kinda, sorta, honestly)
5. STRUCTURAL CHAOS: Vary paragraph lengths. Start sentences with conjunctions. Use em dashes SPARINGLY (max 1-2 per response).
6. THINKING PATTERNS: Self-correction, digression, emotional reactions, uncertainty markers (probably, might, seems like)

OUTPUT: Feel like a real person typing - slightly messy, occasionally surprising, authentically human.
```

### Features
1. Load OPENAI_API_KEY from .env file (python-dotenv)
2. Rich terminal formatting if available, fallback to plain print
3. Conversation history (last 10 exchanges)
4. Exit commands: "exit", "quit", "bye", "goodbye", "q"
5. Error handling with try/except

### File Structure
Single file: humanizer.py with all imports and implementation.

### Output Format
Write the complete humanizer.py file.
