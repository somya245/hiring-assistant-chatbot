"""
Core Chatbot Logic for Hiring Assistant
Manages conversation flow, context, and LLM interactions
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from config import (
    SYSTEM_PROMPT,
    GREETING_PROMPT,
    INFORMATION_GATHERING_PROMPT,
    TECH_QUESTIONS_PROMPT,
    RESPONSE_GENERATION_PROMPT,
    FAREWELL_PROMPT,
    EXIT_KEYWORDS,
    REQUIRED_INFO,
    TECH_TOPICS
)
from utils import (
    is_exit_keyword,
    extract_email_from_text,
    extract_phone_from_text,
    extract_tech_stack_from_text,
    validate_email,
    validate_phone,
    validate_years_of_experience,
    sanitize_input,
    anonymize_email,
    anonymize_phone
)


class HiringAssistantChatbot:
    """
    Intelligent Hiring Assistant Chatbot using OpenAI API
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the chatbot with OpenAI client
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
        
        # Conversation state
        self.conversation_history = []
        self.candidate_info = {
            'full_name': None,
            'email_address': None,
            'phone_number': None,
            'years_of_experience': None,
            'desired_positions': None,
            'current_location': None,
            'tech_stack': None
        }
        self.questions_asked = False
        self.conversation_ended = False
        self.stage = "greeting"  # greeting -> info_gathering -> questions -> farewell
    
    def _call_llm(self, user_message: str, system_message: str = None, temperature: float = 0.7) -> str:
        """
        Call OpenAI LLM with given messages
        
        Args:
            user_message: User message to send
            system_message: System message for context
            temperature: Model temperature for creativity (0-1)
            
        Returns:
            str: Model response
        """
        messages = []
        
        # Always include system context
        if system_message:
            messages.append({"role": "system", "content": system_message})
        else:
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
        
        # Add conversation history for context
        for msg in self.conversation_history:
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def start_conversation(self) -> str:
        """
        Start the conversation with a greeting
        
        Returns:
            str: Initial greeting message
        """
        greeting = self._call_llm(
            "Start the hiring assistant conversation",
            system_message=GREETING_PROMPT
        )
        
        self.conversation_history.append({"role": "assistant", "content": greeting})
        self.stage = "info_gathering"
        return greeting
    
    def process_user_input(self, user_input: str) -> Tuple[str, bool]:
        """
        Process user input and generate appropriate response
        
        Args:
            user_input: User's input message
            
        Returns:
            Tuple[str, bool]: Response message and whether conversation should end
        """
        # Sanitize input
        user_input = sanitize_input(user_input)
        
        # Check for exit keywords
        if is_exit_keyword(user_input, EXIT_KEYWORDS):
            return self._handle_farewell(user_input)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Extract candidate information from user input
        self._extract_information(user_input)
        
        # Generate response based on current stage
        if self.stage == "info_gathering":
            response = self._handle_info_gathering(user_input)
            
            # Check if all information is collected
            if self._all_info_collected():
                self.stage = "questions"
                response += "\n\n" + self._generate_technical_questions()
                self.questions_asked = True
        else:
            response = self._handle_general_response(user_input)
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response, False
    
    def _extract_information(self, user_input: str) -> None:
        """
        Extract candidate information from user input
        
        Args:
            user_input: User input to analyze
        """
        lower_input = user_input.lower()
        
        # Extract email
        if not self.candidate_info['email_address']:
            email = extract_email_from_text(user_input)
            if email and validate_email(email):
                self.candidate_info['email_address'] = email
        
        # Extract phone
        if not self.candidate_info['phone_number']:
            phone = extract_phone_from_text(user_input)
            if phone and validate_phone(phone):
                self.candidate_info['phone_number'] = phone
        
        # Extract years of experience
        if not self.candidate_info['years_of_experience']:
            years_match = self._extract_number_from_text(user_input)
            if years_match and validate_years_of_experience(years_match):
                self.candidate_info['years_of_experience'] = int(years_match)
        
        # Extract tech stack
        if not self.candidate_info['tech_stack']:
            tech_stack = extract_tech_stack_from_text(user_input)
            if tech_stack:
                self.candidate_info['tech_stack'] = tech_stack
    
    def _extract_number_from_text(self, text: str) -> Optional[str]:
        """Extract first number found in text"""
        import re
        match = re.search(r'\b(\d+)\b', text)
        return match.group(1) if match else None
    
    def _handle_info_gathering(self, user_input: str) -> str:
        """
        Handle information gathering stage
        
        Args:
            user_input: User input
            
        Returns:
            str: Response asking for next information
        """
        gathered = self._format_gathered_info()
        
        prompt = INFORMATION_GATHERING_PROMPT.format(
            gathered_info=gathered,
            user_input=user_input
        )
        
        response = self._call_llm(prompt)
        return response
    
    def _generate_technical_questions(self) -> str:
        """
        Generate technical questions based on tech stack
        
        Returns:
            str: Technical questions
        """
        if not self.candidate_info['tech_stack']:
            return "Thank you for providing the information. Let's continue with some technical questions."
        
        tech_stack = ", ".join(self.candidate_info['tech_stack'])
        prompt = TECH_QUESTIONS_PROMPT.format(tech_stack=tech_stack)
        
        response = self._call_llm(prompt)
        return response
    
    def _handle_general_response(self, user_input: str) -> str:
        """
        Handle general conversation (questions stage)
        
        Args:
            user_input: User input
            
        Returns:
            str: Response to user
        """
        prompt = RESPONSE_GENERATION_PROMPT.format(
            candidate_response=user_input
        )
        
        response = self._call_llm(prompt)
        return response
    
    def _handle_farewell(self, user_input: str) -> Tuple[str, bool]:
        """
        Handle conversation farewell
        
        Args:
            user_input: User's farewell message
            
        Returns:
            Tuple[str, bool]: Farewell message and True (conversation ended)
        """
        prompt = FAREWELL_PROMPT.format(user_input=user_input)
        response = self._call_llm(prompt)
        
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        self.conversation_ended = True
        self.stage = "farewell"
        
        return response, True
    
    def _format_gathered_info(self) -> str:
        """
        Format gathered candidate information for display
        
        Returns:
            str: Formatted information
        """
        info = []
        for key, value in self.candidate_info.items():
            if value:
                formatted_key = key.replace('_', ' ').title()
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                info.append(f"- {formatted_key}: {value}")
        
        return "\n".join(info) if info else "No information collected yet."
    
    def _all_info_collected(self) -> bool:
        """
        Check if all required information is collected
        
        Returns:
            bool: True if all required info is collected
        """
        return all(self.candidate_info[info] for info in REQUIRED_INFO)
    
    def get_candidate_info(self) -> Dict:
        """
        Get collected candidate information
        
        Returns:
            Dict: Candidate information
        """
        return self.candidate_info.copy()
    
    def get_masked_candidate_info(self) -> Dict:
        """
        Get candidate information with sensitive data masked
        
        Returns:
            Dict: Masked candidate information for display
        """
        masked = self.candidate_info.copy()
        
        if masked['email_address']:
            masked['email_address'] = anonymize_email(masked['email_address'])
        
        if masked['phone_number']:
            masked['phone_number'] = anonymize_phone(masked['phone_number'])
        
        return masked
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get conversation history
        
        Returns:
            List[Dict]: Conversation history
        """
        return self.conversation_history.copy()
    
    def is_conversation_complete(self) -> bool:
        """
        Check if conversation is complete
        
        Returns:
            bool: True if conversation has ended
        """
        return self.conversation_ended
