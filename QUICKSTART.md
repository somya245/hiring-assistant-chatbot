# Quick Start Guide - TalentScout Hiring Assistant

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- OpenAI API Key ([Get one here](https://platform.openai.com/api_keys))

### Step 1: Set Up (2 minutes)

```bash
# Clone or download the project
cd hiring-assistant-chatbot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# OR: source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key (1 minute)

**Option A: Using .env file (Recommended)**
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

**Option B: Set environment variable directly**
```bash
# Windows
setx OPENAI_API_KEY "sk-..."

# macOS/Linux
export OPENAI_API_KEY="sk-..."
```

### Step 3: Run the Application (1 minute)

```bash
streamlit run app.py
```

The chatbot will open automatically in your browser at `http://localhost:8501`

### Step 4: Test the Chatbot (1 minute)

The chatbot will:
1. Greet you
2. Ask for your information
3. Generate technical questions based on your tech stack
4. Provide a summary and farewell

**Sample Conversation:**
```
You: Hi there!
Bot: Hello! Welcome to TalentScout...

You: My name is Alex
Bot: Nice to meet you, Alex! What's your email address?

You: alex@example.com
Bot: [continues with the conversation flow...]
```

---

## ⚙️ Configuration

### Environment Variables

**Required:**
- `OPENAI_API_KEY`: Your OpenAI API key

**Optional:**
- `MODEL`: Model to use (default: gpt-3.5-turbo)
- `MAX_TOKENS`: Maximum response tokens (default: 500)
- `TEMPERATURE`: Response creativity (0-1, default: 0.7)

### Customization

Edit `config.py` to customize:
- System prompts
- Exit keywords
- Required information fields
- Tech stack topics

---

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_chatbot.py
```

Expected output:
```
==================================================
TalentScout Hiring Assistant - Test Suite
==================================================
Testing imports...
✓ All imports successful
Testing email validation...
✓ john@example.com: True
...
Tests passed: 6/6
==================================================
```

---

## 🔧 Troubleshooting

### Issue: "OpenAI API key not found"
**Solution:** Make sure your `.env` file has `OPENAI_API_KEY=sk-...` and is in the project root

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Run `pip install -r requirements.txt` again

### Issue: Slow responses
**Solution:** Check your internet connection and OpenAI API status

### Issue: API Rate Limit
**Solution:** Wait a few minutes before continuing. Free tier has limits.

---

## 📊 Project Structure

```
hiring-assistant-chatbot/
├── app.py              # Main Streamlit app
├── chatbot.py         # Core chatbot logic
├── config.py          # Configurations and prompts
├── utils.py           # Helper functions
├── test_chatbot.py    # Test suite
├── requirements.txt   # Dependencies
├── README.md          # Full documentation
├── QUICKSTART.md      # This file
└── .env.example       # Environment template
```

---

## 📚 File Purposes

| File | Purpose |
|------|---------|
| **app.py** | Streamlit UI, chat interface, sidebar |
| **chatbot.py** | LLM interaction, conversation management |
| **config.py** | Prompts, keywords, configurations |
| **utils.py** | Validation, extraction, anonymization |
| **test_chatbot.py** | Automated testing |

---

## 💡 Next Steps

1. **Customize Prompts**: Edit `config.py` to personalize the chatbot
2. **Add Data Storage**: Integrate with a database to persist candidate info
3. **Deploy**: Push to GitHub and deploy on Streamlit Cloud or AWS
4. **Enhance Features**: Add sentiment analysis or multilingual support

---

## 🆘 Need Help?

1. Check the full [README.md](README.md)
2. Review [Streamlit Documentation](https://docs.streamlit.io/)
3. Check [OpenAI API Guide](https://platform.openai.com/docs)

---

**Version**: 1.0.0 | **Last Updated**: February 2026
