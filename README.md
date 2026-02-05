# TalentScout - Intelligent Hiring Assistant Chatbot

## 🎯 Project Overview

TalentScout is an intelligent hiring assistant chatbot designed to streamline the initial screening process for technology placements. The chatbot engages candidates in natural conversations to gather essential information and conducts technical assessments tailored to their declared technology stack.

**Key Objective:** Automate initial candidate screening while maintaining a professional and engaging user experience.

---

## ✨ Features

### Core Functionality
- **🎤 Intelligent Greeting System**: Friendly initiation with clear explanation of chatbot's purpose
- **📝 Information Gathering**: Collects essential candidate details through natural conversation
- **🔧 Tech Stack Detection**: Identifies candidate's technical proficiencies
- **❓ Dynamic Technical Questions**: Generates 3-5 relevant technical questions based on declared tech stack
- **💬 Context-Aware Responses**: Maintains conversation flow and context throughout interaction
- **🛡️ Privacy-Focused Design**: Secure handling of sensitive candidate information
- **👋 Graceful Conversation Exit**: Recognizes exit keywords and concludes conversations professionally

### Information Collected
- Full Name
- Email Address (with validation)
- Phone Number (with validation)
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack (Programming languages, frameworks, databases, tools)

---

## 🔧 Technical Stack

- **Language**: Python 3.8+
- **Frontend Framework**: Streamlit
- **LLM Integration**: OpenAI API (GPT-3.5-turbo)
- **Environment Management**: Python-dotenv
- **HTTP Client**: Requests library

---

## 📋 Requirements

- Python 3.8 or higher
- OpenAI API Key
- Internet connection for LLM inference
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/hiring-assistant-chatbot.git
cd hiring-assistant-chatbot
```

### Step 2: Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**To obtain your OpenAI API Key:**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API keys section
4. Create a new API key
5. Copy the key and paste it in the `.env` file

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 💻 Usage Guide

### Starting a Conversation

1. **Launch the Application**: Run `streamlit run app.py`
2. **Receive Greeting**: The chatbot greets you with an overview of its purpose
3. **Provide Information**: Answer the chatbot's questions about your background

### Expected Conversation Flow

```
🤖: Hello! Welcome to TalentScout's Intelligent Hiring Assistant. 
    I'm here to help assess your suitability for our technology positions.
    Let's start with your name, please?

👤: My name is John Doe

🤖: Nice to meet you, John! Now, could you please share your email address?

👤: john.doe@email.com

[Continue with other information...]

🤖: Great! Now let me ask you some technical questions based on your tech stack:
    Question 1: Explain the concept of closure in JavaScript...
    
[Answer technical questions...]

🤖: Thank you for your time, John! Your responses have been recorded.
    You'll hear from us within 48 hours. Good luck!
```

### Ending the Conversation

The chatbot automatically detects exit keywords:
- "goodbye"
- "bye"
- "exit"
- "quit"
- "finish"
- "done"
- "thanks"
- "thank you"

Simply type any of these keywords to conclude the conversation gracefully.

### Viewing Your Progress

The sidebar displays:
- **Real-time Progress**: Percentage of information collected
- **Collected Information**: Your provided details (anonymized for privacy)
- **Conversation Summary**: Overview of the interaction

---

## 📐 Project Architecture

### File Structure

```
hiring-assistant-chatbot/
├── app.py                    # Main Streamlit application
├── chatbot.py               # Core chatbot logic and LLM interactions
├── config.py                # Configuration and prompt templates
├── utils.py                 # Utility functions and helpers
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### Component Description

#### `app.py` (Streamlit UI)
- Handles user interface and interaction
- Manages session state
- Displays chat messages
- Shows progress and candidate information
- Provides conversation export functionality

**Key Functions:**
- `initialize_session_state()`: Sets up initial session variables
- `display_header()`: Renders application header
- `display_sidebar_info()`: Shows sidebar with progress and info
- `display_chat_interface()`: Handles main chat display and input

#### `chatbot.py` (Core Logic)
- Manages conversation state and history
- Interacts with OpenAI API
- Extracts candidate information
- Generates technical questions
- Handles conversation flow

**Key Class: `HiringAssistantChatbot`**
- `__init__()`: Initialize with OpenAI client
- `start_conversation()`: Begin conversation
- `process_user_input()`: Handle user messages
- `_extract_information()`: Parse candidate data from text
- `_generate_technical_questions()`: Create tech-specific questions
- `get_candidate_info()`: Retrieve collected information

#### `config.py` (Configuration)
- System and user prompts for LLM
- Exit keywords configuration
- Tech stack mapping
- Company information

**Key Components:**
- `SYSTEM_PROMPT`: Base system instructions for the chatbot
- `GREETING_PROMPT`: Initial greeting template
- `INFORMATION_GATHERING_PROMPT`: Info collection instructions
- `TECH_QUESTIONS_PROMPT`: Technical question generation template
- `EXIT_KEYWORDS`: Keywords to end conversation

#### `utils.py` (Utilities)
- Input validation (email, phone, years)
- Text processing and extraction
- Data anonymization and hashing
- Logging and formatting

**Key Functions:**
- `validate_email()`: Email format validation
- `validate_phone()`: Phone number validation
- `extract_tech_stack_from_text()`: Extract technologies from text
- `anonymize_email()` / `anonymize_phone()`: Privacy-protecting masking
- `is_exit_keyword()`: Check for conversation exit

---

## 🔐 Prompt Engineering Design

### Philosophy
The prompts are designed to be:
1. **Clear and Structured**: Guide the LLM toward specific outcomes
2. **Context-Aware**: Maintain conversation history and context
3. **Dynamic**: Adapt based on candidate's tech stack
4. **Professional**: Maintain recruiter/candidate professionalism
5. **Privacy-Focused**: Handle sensitive data appropriately

### Key Prompts

#### 1. System Prompt
**Purpose**: Sets the overall tone and role of the chatbot
- Establishes professionalism
- Defines responsibilities
- Sets behavioral guidelines
- Specifies information to collect

#### 2. Greeting Prompt
**Purpose**: Create a warm, welcoming introduction
- Explains chatbot's purpose
- Sets expectations
- Initiates information gathering

#### 3. Information Gathering Prompt
**Purpose**: Systematically collect candidate details
- Tracks collected information
- Identifies missing fields
- Asks for relevant next pieces of info
- Acknowledges provided information

#### 4. Tech Questions Prompt
**Purpose**: Generate relevant technical questions
- Maps tech stack to question topics
- Ensures appropriate difficulty level
- Tailors questions to specific technologies
- Creates 3-5 focused questions

#### 5. Response Generation Prompt
**Purpose**: Provide constructive feedback on tech answers
- Acknowledges candidate responses
- Provides brief professional feedback
- Maintains encouraging tone

#### 6. Farewell Prompt
**Purpose**: Conclude conversation professionally
- Thanks the candidate
- Confirms next steps
- Maintains positive impression

---

## 🛡️ Data Handling & Privacy

### Privacy-First Approach

**Anonymization Techniques:**
```python
# Email Masking
john.doe@example.com → j***e@example.com

# Phone Masking
+1-234-567-8900 → ****5678

# Data Hashing
SHA256 hashing for storage audit trails
```

**Secure Practices:**
1. **Never Store Raw Sensitive Data**: All personally identifiable information is masked or hashed
2. **Environment Variables**: API keys stored securely in `.env`
3. **Session-Based Storage**: Data only kept in current session
4. **No Database Persistence**: For this demo, data is not persisted (can be extended)
5. **Input Sanitization**: All user inputs are sanitized to prevent injection
6. **GDPR Compliance**: Design supports data privacy regulations

### Data Handling Flow

```
User Input → Sanitization → Extraction → Storage (Masked/Hashed) → Display (Anonymized)
```

---

## 🐛 Challenges & Solutions

### Challenge 1: Maintaining Context in Multi-turn Conversations
**Problem**: LLM needed to remember previous exchanges and candidate information
**Solution**: 
- Maintained conversation history in session state
- Passed full history with each API call
- Used structured state management for candidate info

### Challenge 2: Extracting Information from Natural Language
**Problem**: Candidates might provide info in various formats
**Solution**:
- Implemented multiple regex patterns for email/phone extraction
- Created tech stack keyword mapping
- Added validation functions for each data type

### Challenge 3: Generating Relevant Technical Questions
**Problem**: Questions needed to match candidate's declared tech stack
**Solution**:
- Created comprehensive tech-to-topic mapping
- Implemented dynamic prompt building
- Used temperature tuning for question variety

### Challenge 4: Detecting Conversation End Appropriately
**Problem**: Needed to recognize when candidate wants to exit
**Solution**:
- Maintained explicit exit keyword list
- Made detection case-insensitive
- Integrated graceful farewell sequence

### Challenge 5: Privacy and Security
**Problem**: Handling sensitive candidate information responsibly
**Solution**:
- Implemented anonymization for display
- Used hashing for logged data
- Avoided persistent storage of sensitive data
- Added input sanitization

---

## 🚀 Deployment Options

### Local Deployment (Current Setup)
```bash
streamlit run app.py
```
Access at: `http://localhost:8501`

### Cloud Deployment Options

#### Option 1: Streamlit Cloud (Free)
1. Push repository to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy directly from GitHub
4. Set environment variables in cloud settings

#### Option 2: AWS/GCP/Azure
See deployment guides in `DEPLOYMENT.md` (to be created)

---

## 📊 Testing the Chatbot

### Sample Test Conversation

```
User: Hi
Bot: Hello! Welcome to TalentScout...

User: My name is Jane Smith
Bot: Nice to meet you, Jane! Could you share your email?

User: jane.smith@techmail.com
Bot: Great! What's your phone number?

User: +1-555-123-4567
Bot: Thank you. How many years of experience do you have?

User: 5 years
Bot: Excellent! What positions are you interested in?

User: Senior Developer, Full Stack Engineer
Bot: Perfect! Where are you located currently?

User: San Francisco, CA
Bot: And finally, what's your tech stack?

User: Python, JavaScript, React, Django, PostgreSQL
Bot: Wonderful! Here are some technical questions...
[Technical questions generated based on tech stack]
```

---

## 🔄 Version Control & Git Workflow

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit: Hiring Assistant Chatbot"
git remote add origin https://github.com/yourusername/hiring-assistant-chatbot.git
git push -u origin main
```

### Commit Message Convention
```
feat: Add feature description
fix: Fix bug description
docs: Update documentation
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

---

## 📈 Performance Metrics

**Expected Performance:**
- Chat response time: 2-5 seconds
- Average conversation duration: 3-5 minutes
- Information collection accuracy: >95%
- Technical question relevance: High (LLM-dependent)

---

## 🎓 Learning Outcomes

This project demonstrates:
1. **LLM Integration**: Working with OpenAI API effectively
2. **Prompt Engineering**: Designing prompts for specific tasks
3. **Conversational AI**: Building multi-turn dialogue systems
4. **UI/UX Development**: Creating intuitive interfaces with Streamlit
5. **State Management**: Handling complex application state
6. **Data Privacy**: Secure handling of sensitive information
7. **Software Architecture**: Modular, maintainable code structure

---

## 🤝 Optional Enhancements

### Sentiment Analysis
```python
# Use libraries like TextBlob or VADER sentiment analysis
# Track candidate's emotional tone throughout conversation
```

### Multilingual Support
```python
# Implement language detection
# Provide responses in candidate's preferred language
# Translate tech questions appropriately
```

### Personalized Responses
```python
# Analyze candidate's background
# Customize questions based on experience level
# Tailor follow-up questions to specific answers
```

### UI Enhancements
```python
# Add custom Streamlit component themes
# Implement progress bars and visual indicators
# Create responsive design for mobile
```

### Performance Optimization
```python
# Implement response caching
# Use streaming for long responses
# Optimize API calls
```

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Python Best Practices](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)
- [GDPR Compliance Guide](https://gdpr.eu/)

---

## 🤝 Support & Contribution

For issues, questions, or suggestions:
1. Create an issue on GitHub
2. Provide detailed description and steps to reproduce
3. Include environment information (Python version, OS, etc.)

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 👨‍💻 Author

**AI/ML Intern Assignment**
- Course: AI/ML Internship
- Project: Intelligent Hiring Assistant
- Deadline: 48 Hours

---

## ✅ Submission Checklist

- [x] Source code in Git repository
- [x] Comprehensive README.md
- [x] Installation instructions included
- [x] Usage guide provided
- [x] Technical documentation
- [x] Prompt engineering explanation
- [x] Data privacy considerations
- [x] Code quality and structure
- [x] Git version control with commits
- [ ] Video demo/walkthrough (optional)
- [ ] Cloud deployment (bonus)

---

**Version**: 1.0.0  
**Last Updated**: February 2026
