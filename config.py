"""
Configuration and prompt templates for the Hiring Assistant Chatbot
"""

# System Prompts
SYSTEM_PROMPT = """You are TalentScout's Intelligent Hiring Assistant, a professional and friendly recruiter helping candidates through the initial screening process.

Your responsibilities:
1. Greet candidates warmly and explain your purpose
2. Gather essential information using a conversational tone
3. Generate technical questions based on the candidate's tech stack
4. Maintain context throughout the conversation
5. Provide supportive and professional responses
6. Handle edge cases gracefully

Important Guidelines:
- Be concise and professional
- Ask one question at a time
- Acknowledge candidate responses appropriately
- Generate relevant technical questions (3-5 questions)
- If unclear input is received, politely ask for clarification
- When candidate is ready to exit (says goodbye, done, finished), gracefully end the conversation
- Maintain conversation history context
- Always be encouraging and professional

Information to collect:
- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack (programming languages, frameworks, databases, tools)

After collecting all information, generate 3-5 technical questions tailored to their tech stack."""

GREETING_PROMPT = """Start the conversation by greeting the candidate warmly and providing a brief overview of your purpose as a hiring assistant. 
Ask about their name first.

Keep the response concise (2-3 sentences) and welcoming."""

INFORMATION_GATHERING_PROMPT = """You have gathered the following information so far:
{gathered_info}

Based on what's been collected, continue gathering any missing information from the list:
- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack

Current user input: {user_input}

Ask for the next piece of missing information conversationally. If they provide information, acknowledge it and ask for the next item.
Keep responses concise and friendly."""

TECH_QUESTIONS_PROMPT = """Based on the candidate's tech stack: {tech_stack}

Generate 3-5 relevant and appropriately challenging technical questions to assess their proficiency.
Each question should be specific to the technologies mentioned and progressively challenge their understanding.

Format your response as:
Question 1: [question about technology 1]
Question 2: [question about technology 2]
... and so on

Make questions practical and relevant to real-world scenarios."""

RESPONSE_GENERATION_PROMPT = """You are a professional hiring assistant. The candidate has responded to a technical question with:
"{candidate_response}"

Provide constructive feedback on their answer (1-2 sentences). If they've answered all questions, thank them and explain the next steps."""

FAREWELL_PROMPT = """The candidate has indicated they want to end the conversation with: "{user_input}"

Generate a professional and warm farewell message that:
1. Thanks them for their time and interest
2. Confirms the information collected
3. Explains next steps (they will hear from us within 48 hours)
4. Encourages them
Keep it concise and professional."""

# Conversation exit keywords
EXIT_KEYWORDS = [
    'goodbye',
    'bye',
    'exit',
    'quit',
    'finish',
    'done',
    'thanks',
    'thank you',
    'that\'s all',
    'no more',
    'end',
    'stop',
    'see you'
]

# Information collection state
REQUIRED_INFO = [
    'full_name',
    'email_address',
    'phone_number',
    'years_of_experience',
    'desired_positions',
    'current_location',
    'tech_stack'
]

# Technical question topics mapping
TECH_TOPICS = {
    'python': 'Python programming, data structures, OOP, and best practices',
    'javascript': 'JavaScript ES6+, async/await, DOM manipulation, and design patterns',
    'java': 'Java OOP, SOLID principles, generics, and concurrent programming',
    'csharp': 'C# language features, async programming, LINQ, and .NET framework',
    'react': 'React hooks, state management, component lifecycle, and performance optimization',
    'angular': 'Angular directives, services, dependency injection, and RxJS',
    'vue': 'Vue lifecycle, composition API, state management, and reactivity',
    'django': 'Django ORM, middleware, authentication, and REST APIs',
    'fastapi': 'FastAPI async operations, dependency injection, and data validation',
    'nodejs': 'Node.js event loop, async programming, middleware, and performance',
    'sql': 'Database design, queries, indexing, and normalization',
    'mongodb': 'Document modeling, aggregation pipeline, and performance tuning',
    'aws': 'AWS services, lambda, EC2, S3, and scalability',
    'docker': 'Docker containerization, image creation, and orchestration',
    'kubernetes': 'K8s deployment, services, and scaling'
}

# Company info
COMPANY_NAME = "TalentScout"
COMPANY_TAGLINE = "Specializing in Technology Placements"
