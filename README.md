# AI Humanizer Chatbot

A CLI chatbot that uses Gemini API with specialized system prompts and inference parameters to generate humanized text that bypasses AI detection.

## How It Works

This chatbot manipulates two key metrics that AI detectors use:

1. **Perplexity** - Measures how predictable word choices are. Human text has higher perplexity (more surprising word choices).
2. **Burstiness** - Measures variation in sentence structure. Human text has high burstiness (mix of short fragments and long sentences).

## Installation

```bash
# Clone or download the project
cd ai-humanizer

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
export GEMINI_API_KEY="your-api-key-here"

# Or create a .env file
cp .env.example .env
# Edit .env and add your API key
```

## Usage

```bash
python humanizer.py
```

### Example Session

```
🎭 AI Humanizer Chatbot

This chatbot uses advanced techniques to generate human-like text:
• High perplexity (surprising word choices)
• High burstiness (varied sentence structures)
...

You: Write about artificial intelligence

Honestly? AI's gotten weird. Like, we all expected robots to take factory jobs—not write our essays and paint our portraits. 

I remember when "smart" meant your calculator could do sine functions. Now we've got these language models that... well, they kinda think? Maybe? That's the unsettling part—we're not even sure what "thinking" means anymore.

The whole thing's moving too fast. Way too fast.

You: exit

Goodbye! 👋
```

## Key Features

### Humanization Techniques

The system prompt enforces:

- **Surprising word choices** - Replaces predictable words with creative alternatives
- **Sentence variation** - Mixes 3-word fragments with 30-word run-ons
- **Banned AI phrases** - Eliminates "delve into," "it's worth noting," "furthermore," etc.
- **Conversational tone** - Uses contractions, fragments, and colloquialisms
- **Structural chaos** - Random paragraph lengths, sentence starters
- **Voice injection** - Opinions, rhetorical questions, self-corrections

### Inference Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| temperature | 0.95 | High randomness for unpredictable word choices |
| top_p | 0.92 | Allows creative outliers while maintaining coherence |
| top_k | 50 | Broad vocabulary sampling |
| presence_penalty | 0.4 | Discourages repeating concepts |
| frequency_penalty | 0.3 | Reduces word repetition |

## Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Set it as `GEMINI_API_KEY` environment variable or in `.env` file

## Testing Against AI Detectors

To verify the humanization is working:

1. Generate text with this chatbot
2. Copy the output
3. Test with detectors like:
   - [GPTZero](https://gptzero.me)
   - [Originality.ai](https://originality.ai)
   - [Writer.com AI Detector](https://writer.com/ai-content-detector/)

Well-humanized text should score <10% AI probability.

## Architecture

```
humanizer.py
├── HUMANIZATION_SYSTEM_PROMPT  # Verbatim humanization directives
├── GENERATION_CONFIG           # Tuned inference parameters
├── get_api_key()              # API key management
├── initialize_model()         # Gemini model setup
└── main()                     # Chat loop
```

## Customization

Edit `HUMANIZATION_SYSTEM_PROMPT` in `humanizer.py` to adjust:
- Tone (more casual, more professional, etc.)
- Specific phrases to ban/encourage
- Structural preferences

Edit `GENERATION_CONFIG` to adjust randomness and creativity levels.

## License

MIT License - Use responsibly and ethically.

## Disclaimer

This tool is designed for:
- Protecting legitimate work from false AI detection positives
- Learning about AI detection mechanisms
- Improving AI text quality

Not for:
- Academic dishonesty
- Deceiving readers about AI authorship where prohibited
- Bypassing legitimate content policies
