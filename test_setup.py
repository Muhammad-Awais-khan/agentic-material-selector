"""
Test script to verify environment and API connectivity
"""
from dotenv import load_dotenv
import os
import sys

print("=" * 60)
print("ENVIRONMENT CHECK")
print("=" * 60)

# Check .env file
load_dotenv()
api_key = os.getenv("BYTEZ_API_KEY")

if not api_key:
    print("❌ BYTEZ_API_KEY not found in .env file!")
    print("\nCreate a .env file with:")
    print("BYTEZ_API_KEY=your_api_key_here")
    sys.exit(1)

print(f"✓ API Key found: {api_key[:10]}...")

# Check imports
print("\nChecking imports...")
try:
    import openai
    print("✓ openai imported")
except ImportError as e:
    print(f"❌ Failed to import openai: {e}")
    sys.exit(1)

try:
    from orchestrator import MaterialSelectorOrchestrator
    print("✓ Orchestrator imported")
except ImportError as e:
    print(f"❌ Failed to import orchestrator: {e}")
    sys.exit(1)

# Test API connection
print("\nTesting API connection...")
print("(This may take a moment...)")

try:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.bytez.com/models/v2/openai/v1/"
    )
    print("✓ OpenAI Client created")
    
    # Simple test call
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say 'Hello' only"}
        ],
        temperature=0.1,
        max_completion_tokens=10
    )
    
    result = response.choices[0].message.content
    print(f"✓ API Connection successful!")
    print(f"  Response: {result}")
    
except Exception as e:
    print(f"❌ API Error: {type(e).__name__}: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL CHECKS PASSED - System is ready!")
print("=" * 60)
print("\nRun: python main.py")
