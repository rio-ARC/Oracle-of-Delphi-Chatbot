"""
Test script for the AI Question-Answer Helper agent.
This script tests the agent directly without going through the API layer.
"""

import os
from dotenv import load_dotenv
from agent.graph import chat

# Load environment variables
load_dotenv()


def test_agent():
    """
    Test the agent with various types of questions.
    """
    print("=" * 60)
    print("AI Question-Answer Helper - Test Suite")
    print("=" * 60)
    
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("\n❌ ERROR: GROQ_API_KEY not found in environment variables.")
        print("Please set it in your .env file before running tests.")
        return
    
    print("\n✅ API key found. Starting tests...\n")
    
    # Test session ID
    test_session = "test-session-001"
    
    # Test 1: Factual question about capitals
    print("\n" + "-" * 60)
    print("TEST 1: Factual Question (Should use search tool)")
    print("-" * 60)
    question1 = "What is the capital of France?"
    print(f"User: {question1}")
    response1 = chat(question1, test_session)
    print(f"Agent: {response1}")
    
    # Test 2: Another factual question
    print("\n" + "-" * 60)
    print("TEST 2: Another Factual Question")
    print("-" * 60)
    question2 = "What is the capital of Japan?"
    print(f"User: {question2}")
    response2 = chat(question2, test_session)
    print(f"Agent: {response2}")
    
    # Test 3: Science fact
    print("\n" + "-" * 60)
    print("TEST 3: Science Fact")
    print("-" * 60)
    question3 = "What is the speed of light?"
    print(f"User: {question3}")
    response3 = chat(question3, test_session)
    print(f"Agent: {response3}")
    
    # Test 4: Conversational question
    print("\n" + "-" * 60)
    print("TEST 4: Conversational Question (Should NOT use search tool)")
    print("-" * 60)
    question4 = "Hello! How are you today?"
    print(f"User: {question4}")
    response4 = chat(question4, test_session)
    print(f"Agent: {response4}")
    
    # Test 5: General conversation
    print("\n" + "-" * 60)
    print("TEST 5: General Conversation")
    print("-" * 60)
    question5 = "Can you help me with something?"
    print(f"User: {question5}")
    response5 = chat(question5, test_session)
    print(f"Agent: {response5}")
    
    # Test 6: Memory test - follow-up question
    print("\n" + "-" * 60)
    print("TEST 6: Memory/Context Test")
    print("-" * 60)
    # First establish context
    question6a = "What is the capital of Germany?"
    print(f"User: {question6a}")
    response6a = chat(question6a, test_session)
    print(f"Agent: {response6a}")
    
    # Now ask follow-up that requires context
    question6b = "Tell me more about that city."
    print(f"\nUser: {question6b}")
    response6b = chat(question6b, test_session)
    print(f"Agent: {response6b}")
    
    # Test 7: Question not in knowledge base
    print("\n" + "-" * 60)
    print("TEST 7: Question Outside Knowledge Base")
    print("-" * 60)
    question7 = "What is the capital of Antarctica?"
    print(f"User: {question7}")
    response7 = chat(question7, test_session)
    print(f"Agent: {response7}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Suite Complete!")
    print("=" * 60)
    print("\nExpected Behavior:")
    print("✓ Tests 1-3: Should use search tool for factual answers")
    print("✓ Tests 4-5: Should provide conversational responses")
    print("✓ Test 6: Should remember context from previous message")
    print("✓ Test 7: Should handle unknown facts gracefully")
    print("\nCheck the responses above to verify the agent is working correctly.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_agent()
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        print("\nMake sure:")
        print("1. You have set GROQ_API_KEY in your .env file")
        print("2. All dependencies are installed (pip install -r requirements.txt)")
        print("3. You have an active internet connection")
