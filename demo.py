#!/usr/bin/env python3
"""
Demo script showing the difference between standard AI output and humanized output.
This demonstrates the perplexity and burstiness manipulation in action.
"""

import os

# Import the constants directly to avoid SDK dependency for demo
HUMANIZATION_SYSTEM_PROMPT = "..."
GENERATION_CONFIG = {
    "temperature": 0.95,
    "top_p": 0.92,
    "top_k": 50,
    "presence_penalty": 0.4,
    "frequency_penalty": 0.3,
}

DEMO_PROMPT = "Explain what photosynthesis is"

STANDARD_SYSTEM_PROMPT = "You are a helpful AI assistant. Be clear, accurate, and informative."

print("=" * 70)
print("🎭 AI HUMANIZER - COMPARISON DEMO")
print("=" * 70)
print()

print(f"📋 PROMPT: '{DEMO_PROMPT}'")
print()

print("-" * 70)
print("🤖 STANDARD AI OUTPUT (Low perplexity, low burstiness)")
print("-" * 70)
print("""
Photosynthesis is the process by which plants, algae, and some bacteria convert 
light energy into chemical energy. During this process, organisms use sunlight, 
water, and carbon dioxide to create glucose and oxygen. The chemical equation 
is 6CO2 + 6H2O → C6H12O6 + 6O2. This process is essential for life on Earth 
because it produces oxygen and forms the base of most food chains.

It's worth noting that photosynthesis occurs in two stages: the light-dependent 
reactions and the Calvin cycle. Furthermore, chlorophyll is the primary pigment 
responsible for capturing light energy.
""")

print()
print("-" * 70)
print("📝 HUMANIZED OUTPUT (High perplexity, high burstiness)")
print("-" * 70)
print("""
Okay so photosynthesis? Basically plants are solar panels, but way cooler and 
they've been doing it for like... billions of years. Way before Elon Musk 
thought Tesla was a good idea.

Here's the wild part. These green dudes just... sit there. All day. Soaking up 
sunlight like it's a beach vacation, and somehow—SOMEHOW—they're turning that 
light into actual food. Sugar, specifically. While the rest of us have to 
order DoorDash.

The chemistry's actually pretty elegant, if you're into that. CO2 plus water 
plus sunshine equals glucose and oxygen. That's it. That's the magic formula. 
Plants literally exhale the air we breathe. Kinda makes you want to hug a tree, 
right?

Oh, and there's this whole thing with chlorophyll—that's the green stuff—
catching photons like a baseball glove. Two-stage process. Light reactions, 
then the Calvin cycle. Don't ask me why it's named after Calvin. Probably some 
scientist with too much time on his hands.

Anyway. Plants are metal. That's the takeaway.
""")

print()
print("=" * 70)
print("📊 ANALYSIS")
print("=" * 70)
print("""
STANDARD AI TEXT DETECTION PATTERNS:
• Uniform sentence length (~20-25 words each)
• Formal, academic tone throughout
• Predictable transitions: "Furthermore," "It's worth noting"
• Consistent structure: Definition → Explanation → Importance
• Low perplexity: "Photosynthesis is the process by which..." (expected phrasing)
• Low burstiness: Same complexity level throughout

HUMANIZED TEXT CHARACTERISTICS:
• Variable sentence length: 3 words to 35+ words
• Mixed tone: casual, humorous, then technical, then casual again
• Human markers: "Okay so," "Here's the wild part," "Don't ask me why"
• Opinions and reactions: "Way cooler," "Kinda makes you want to hug a tree"
• High perplexity: "green dudes," "solar panels," "metal" (unexpected word choices)
• High burstiness: Short punchy fragments mixed with complex explanations
• Self-correction: "Sugar, specifically"

AI DETECTOR SCORES (Estimated):
• Standard text: 85-95% AI probability
• Humanized text: 5-15% AI probability
""")

print()
print("=" * 70)
print("🔧 SYSTEM PROMPT CONFIGURATION")
print("=" * 70)
print(f"""
The humanization is achieved through a specialized system prompt and tuned parameters:

PARAMETERS:
• temperature: {GENERATION_CONFIG['temperature']} (high randomness)
• top_p: {GENERATION_CONFIG['top_p']} (creative outliers allowed)
• top_k: {GENERATION_CONFIG['top_k']} (broad vocabulary)
• presence_penalty: {GENERATION_CONFIG['presence_penalty']} (discourage repetition)
• frequency_penalty: {GENERATION_CONFIG['frequency_penalty']} (lexical diversity)

SYSTEM PROMPT INCLUDES:
• Perplexity manipulation directives
• Burstiness amplification rules
• Banned phrase list ("delve into", "furthermore", etc.)
• Human voice injection (opinions, fragments, colloquialisms)
• Structural chaos requirements

See humanizer.py for the full implementation.
""")
