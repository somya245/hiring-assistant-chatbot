"""
Example test script to validate chatbot functionality
Run this to verify the chatbot works correctly before deployment
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_chatbot_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    try:
        from chatbot import HiringAssistantChatbot
        from config import SYSTEM_PROMPT, EXIT_KEYWORDS
        from utils import validate_email, validate_phone
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_email_validation():
    """Test email validation"""
    print("\nTesting email validation...")
    from utils import validate_email
    
    test_emails = [
        ("john@example.com", True),
        ("invalid.email", False),
        ("test+tag@domain.co.uk", True),
        ("wrong@@domain.com", False),
    ]
    
    for email, expected in test_emails:
        result = validate_email(email)
        status = "✓" if result == expected else "✗"
        print(f"{status} {email}: {result}")

def test_phone_validation():
    """Test phone validation"""
    print("\nTesting phone validation...")
    from utils import validate_phone
    
    test_phones = [
        ("+1-555-123-4567", True),
        ("555-123-4567", True),
        ("123", False),
        ("5551234567", True),
    ]
    
    for phone, expected in test_phones:
        result = validate_phone(phone)
        status = "✓" if result == expected else "✗"
        print(f"{status} {phone}: {result}")

def test_tech_extraction():
    """Test tech stack extraction"""
    print("\nTesting tech stack extraction...")
    from utils import extract_tech_stack_from_text
    
    test_texts = [
        "I work with Python and Django",
        "My stack: JavaScript, React, Node.js",
        "I know Python, Java, and C#"
    ]
    
    for text in test_texts:
        techs = extract_tech_stack_from_text(text)
        print(f"✓ '{text}' -> {techs}")

def test_exit_keywords():
    """Test exit keyword detection"""
    print("\nTesting exit keyword detection...")
    from utils import is_exit_keyword
    from config import EXIT_KEYWORDS
    
    test_inputs = [
        ("goodbye", True),
        ("Thanks for the chat", True),
        ("I need to go", False),
        ("exit the conversation", True),
    ]
    
    for text, expected in test_inputs:
        result = is_exit_keyword(text, EXIT_KEYWORDS)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}': {result}")

def test_chatbot_initialization():
    """Test chatbot initialization"""
    print("\nTesting chatbot initialization...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("✗ OPENAI_API_KEY not set in environment")
        return False
    
    try:
        from chatbot import HiringAssistantChatbot
        chatbot = HiringAssistantChatbot()
        print("✓ Chatbot initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Chatbot initialization failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("TalentScout Hiring Assistant - Test Suite")
    print("=" * 50)
    
    tests = [
        test_chatbot_imports,
        test_email_validation,
        test_phone_validation,
        test_tech_extraction,
        test_exit_keywords,
        test_chatbot_initialization,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result if isinstance(result, bool) else True)
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    print("=" * 50)
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
