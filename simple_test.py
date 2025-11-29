"""Simple test to verify agent works."""
import os
os.environ["GROQ_API_KEY"] = "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"

from agent.graph import chat

print("Testing agent...")
print("\n1. Factual question:")
response = chat("What is the capital of France?", "test")
print(f"Response: {response}")

print("\n2. Conversational:")
response2 = chat("Hello!", "test2")
print(f"Response: {response2}")

print("\nAgent test complete!")
