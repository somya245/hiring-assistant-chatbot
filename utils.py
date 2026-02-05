"""
Utility functions for the Hiring Assistant Chatbot
"""

import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional

def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (basic check)
    
    Args:
        phone: Phone number to validate
        
    Returns:
        bool: True if phone number looks valid, False otherwise
    """
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\+\(\)]+', '', phone)
    # Check if it has 7-15 digits
    return len(cleaned) >= 7 and cleaned.isdigit()


def validate_years_of_experience(years: str) -> bool:
    """
    Validate years of experience input
    
    Args:
        years: Years of experience string
        
    Returns:
        bool: True if valid integer between 0 and 60
    """
    try:
        years_int = int(years)
        return 0 <= years_int <= 60
    except ValueError:
        return False


def extract_email_from_text(text: str) -> Optional[str]:
    """
    Extract email address from text
    
    Args:
        text: Text to search for email
        
    Returns:
        str: Email address if found, None otherwise
    """
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone_from_text(text: str) -> Optional[str]:
    """
    Extract phone number from text
    
    Args:
        text: Text to search for phone number
        
    Returns:
        str: Phone number if found, None otherwise
    """
    # Look for common phone number patterns
    patterns = [
        r'\+?1?\s*\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})',  # US format
        r'\+\d{1,3}\s?\d{6,14}',  # International format
        r'\d{7,15}'  # Generic international
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


def extract_tech_stack_from_text(text: str) -> List[str]:
    """
    Extract potential tech stack items from text
    
    Args:
        text: Text to analyze
        
    Returns:
        List[str]: List of identified technologies
    """
    tech_keywords = {
        'python', 'javascript', 'typescript', 'java', 'csharp', 'c#',
        'go', 'rust', 'php', 'ruby', 'kotlin', 'swift',
        'react', 'angular', 'vue', 'svelte', 'next.js',
        'django', 'fastapi', 'flask', 'spring', 'asp.net',
        'nodejs', 'express', 'deno',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'jenkins',
        'git', 'github', 'gitlab', 'bitbucket',
        'linux', 'windows', 'macos',
        'rest', 'graphql', 'grpc', 'soap',
        'html', 'css', 'sass', 'tailwind',
        'junit', 'pytest', 'mocha', 'jest',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'pandas', 'numpy', 'matplotlib'
    }
    
    text_lower = text.lower()
    found_tech = []
    
    for tech in tech_keywords:
        if tech in text_lower:
            found_tech.append(tech.title())
    
    return list(set(found_tech))  # Remove duplicates


def anonymize_email(email: str) -> str:
    """
    Anonymize email for privacy
    
    Args:
        email: Email to anonymize
        
    Returns:
        str: Anonymized email representation
    """
    if '@' not in email:
        return "invalid_email"
    
    local, domain = email.split('@')
    anonymized_local = local[0] + '*' * (len(local) - 2) + local[-1] if len(local) > 1 else '*'
    return f"{anonymized_local}@{domain}"


def anonymize_phone(phone: str) -> str:
    """
    Anonymize phone number for privacy
    
    Args:
        phone: Phone to anonymize
        
    Returns:
        str: Anonymized phone representation
    """
    cleaned = re.sub(r'[\s\-\+\(\)]+', '', phone)
    if len(cleaned) < 4:
        return '*' * len(cleaned)
    return '*' * (len(cleaned) - 4) + cleaned[-4:]


def hash_sensitive_data(data: str) -> str:
    """
    Hash sensitive data for secure storage
    
    Args:
        data: Data to hash
        
    Returns:
        str: SHA256 hash of the data
    """
    return hashlib.sha256(data.encode()).hexdigest()


def is_exit_keyword(text: str, exit_keywords: List[str]) -> bool:
    """
    Check if text contains exit keywords
    
    Args:
        text: Text to check
        exit_keywords: List of keywords that indicate exit
        
    Returns:
        bool: True if exit keyword found
    """
    text_lower = text.lower().strip()
    for keyword in exit_keywords:
        if keyword in text_lower:
            return True
    return False


def format_candidate_info(info: Dict) -> str:
    """
    Format candidate information for display
    
    Args:
        info: Dictionary of candidate information
        
    Returns:
        str: Formatted candidate information
    """
    formatted = "\n".join([
        f"**{key.replace('_', ' ').title()}:** {value}"
        for key, value in info.items()
        if value
    ])
    return formatted


def get_timestamp() -> str:
    """
    Get current timestamp for logging
    
    Returns:
        str: Current timestamp in ISO format
    """
    return datetime.now().isoformat()


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        user_input: User input to sanitize
        
    Returns:
        str: Sanitized input
    """
    # Remove leading/trailing whitespace
    sanitized = user_input.strip()
    
    # Remove potentially harmful characters (but keep normal text)
    # Only allow alphanumeric, common punctuation, and whitespace
    sanitized = re.sub(r'[^\w\s\.\@\-\+\(\)\,\'\"\?\!]', '', sanitized)
    
    return sanitized


def log_interaction(user_input: str, assistant_response: str, candidate_info: Dict = None) -> Dict:
    """
    Create a structured log entry for an interaction
    
    Args:
        user_input: User input
        assistant_response: Assistant response
        candidate_info: Optional candidate information
        
    Returns:
        Dict: Structured log entry
    """
    return {
        'timestamp': get_timestamp(),
        'user_input': user_input,
        'assistant_response': assistant_response,
        'candidate_info_hash': hash_sensitive_data(str(candidate_info)) if candidate_info else None
    }
