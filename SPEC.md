# SPEC.md - AI Humanizer Chatbot

## Project Overview
A CLI chatbot that uses OpenAI GPT-5.2 API with low reasoning effort and a specialized system prompt to generate guaranteed humanized text that bypasses AI detection by manipulating perplexity and burstiness.

## Core Concepts (Research Summary)

### Perplexity
- **Definition**: How unexpected/surprising each word is to a language model
- **Low perplexity**: Predictable word choices (soup after "bowl of")
- **High perplexity**: Surprising word choices (spiders after "bowl of")
- **AI pattern**: Consistently LOW perplexity across entire text
- **Human pattern**: MIXED perplexity - some predictable, some surprising

### Burstiness
- **Definition**: Variation in perplexity across a document
- **AI pattern**: Uniform low burstiness (consistent, predictable throughout)
- **Human pattern**: HIGH burstiness - spikes of unpredictability mixed with calm sections
- **Key insight**: Human writers naturally vary sentence structure and word choice unpredictably

### Detection Bypass Mechanisms
1. **Sentence length variation**: Mix 5-word fragments with 25+ word complex sentences
2. **Vocabulary randomization**: Use unexpected synonyms, avoid AI clichés ("delve", "it's worth noting", "in conclusion")
3. **Structural chaos**: Vary paragraph lengths, use fragments, break formulaic patterns
4. **Voice injection**: Add opinions, rhetorical questions, personal asides
5. **Rhythm disruption**: Avoid consistent 20-25 word sentence patterns
6. **Lexical diversity**: Prevent repetitive transitions and phrases

## The Verbatim Humanization System Prompt

```
You are a human writer. Your output must be indistinguishable from authentic human text.

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

OUTPUT REQUIREMENT: Every response must feel like a real person typing - slightly messy, occasionally surprising, authentically human. If it sounds too polished, it's wrong.
```

## Inference Parameters for Human-like Generation

```json
{
  "model": "gpt-5.2",
  "reasoning": { "effort": "low" },
  "temperature": 0.95,
  "topP": 0.92,
  "presencePenalty": 0.4,
  "frequencyPenalty": 0.3,
  "maxOutputTokens": 2048
}
```

### Parameter Rationale:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| model | gpt-5.2 | OpenAI's flagship model with reasoning control |
| reasoning.effort | low | Low thinking budget for faster, more natural responses |
| temperature | 0.95 | High randomness for unpredictable word choices |
| topP | 0.92 | Nucleus sampling - allows creative outliers while maintaining coherence |
| presencePenalty | 0.4 | Discourages repeating concepts |
| frequencyPenalty | 0.3 | Reduces repetition of specific words |
| maxOutputTokens | 2048 | Standard conversational length |

## Implementation Requirements

1. **CLI Interface**: Simple command-line chatbot using OpenAI API
2. **System Prompt**: Must use the VERBATIM prompt above, unmodified
3. **Parameters**: Must use the EXACT parameter values specified
4. **Conversation Memory**: Maintain context across turns
5. **Exit Command**: User can type "exit" or "quit" to end session

## File Structure
```
ai-humanizer/
├── humanizer.py          # Main chatbot implementation
├── .env                  # API key (OPENAI_API_KEY)
├── requirements.txt      # Dependencies
└── README.md            # Usage instructions
```

## Dependencies
- `openai` - Official OpenAI Python SDK
- `python-dotenv` - Environment variable management
- `rich` - Beautiful terminal formatting (optional but recommended)

## Usage
```bash
# Setup
export OPENAI_API_KEY="your-api-key"
pip install -r requirements.txt

# Run
python humanizer.py

# Chat with the humanized AI
> Write about climate change
[Humanized response appears]

> exit
Goodbye!
```

## Verification
After implementation, test outputs should:
1. Show dramatic sentence length variation
2. Avoid ALL banned phrases
3. Include contractions and colloquialisms
4. Have unpredictable word choices
5. Pass AI detection tools (GPTZero, etc.) with <10% AI probability
