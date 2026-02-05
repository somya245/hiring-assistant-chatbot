"""
Streamlit UI for TalentScout Hiring Assistant Chatbot
"""

import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import HiringAssistantChatbot
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TalentScout - Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        margin: 1rem 0;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
def initialize_session_state():
    """Initialize session state variables"""
    if "chatbot" not in st.session_state:
        try:
            st.session_state.chatbot = HiringAssistantChatbot()
            st.session_state.messages = []
            st.session_state.conversation_started = False
        except ValueError as e:
            st.session_state.chatbot = None
            st.session_state.error = str(e)

def save_candidate_data(candidate_info: dict):
    """
    Save candidate data (anonymized) for demonstration
    
    Args:
        candidate_info: Dictionary of candidate information
    """
    timestamp = datetime.now().isoformat()
    
    # Create anonymized record
    anonymized_record = {
        'timestamp': timestamp,
        'candidate_info_hash': hash(str(candidate_info))
    }
    
    # In a production app, this would save to a database
    # For now, we just demonstrate the concept
    return anonymized_record

def display_header():
    """Display application header"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="header-container">
            <h1>🤖 TalentScout</h1>
            <h3>Intelligent Hiring Assistant</h3>
            <p><em>Specializing in Technology Placements</em></p>
        </div>
        """, unsafe_allow_html=True)

def display_sidebar_info():
    """Display information in sidebar"""
    with st.sidebar:
        st.markdown("### 📋 Conversation Status")
        
        if st.session_state.conversation_started and st.session_state.chatbot:
            candidate_info = st.session_state.chatbot.get_candidate_info()
            
            # Show collected information
            collected_count = sum(1 for v in candidate_info.values() if v)
            progress = collected_count / 7  # 7 total fields
            
            st.progress(progress)
            st.markdown(f"**Information Collected:** {collected_count}/7")
            
            # Show masked candidate info
            if candidate_info['full_name']:
                st.markdown("#### ✅ Collected Information:")
                
                # Display only non-empty fields with masking for sensitive data
                if candidate_info['full_name']:
                    st.markdown(f"- **Name:** {candidate_info['full_name']}")
                if candidate_info['email_address']:
                    masked_email = anonymize_email_display(candidate_info['email_address'])
                    st.markdown(f"- **Email:** {masked_email}")
                if candidate_info['phone_number']:
                    masked_phone = anonymize_phone_display(candidate_info['phone_number'])
                    st.markdown(f"- **Phone:** {masked_phone}")
                if candidate_info['years_of_experience']:
                    st.markdown(f"- **Experience:** {candidate_info['years_of_experience']} years")
                if candidate_info['desired_positions']:
                    st.markdown(f"- **Desired Positions:** {candidate_info['desired_positions']}")
                if candidate_info['current_location']:
                    st.markdown(f"- **Location:** {candidate_info['current_location']}")
                if candidate_info['tech_stack']:
                    tech_str = ", ".join(candidate_info['tech_stack'])
                    st.markdown(f"- **Tech Stack:** {tech_str}")
        
        st.markdown("---")
        st.markdown("### ℹ️ About This Chatbot")
        st.markdown("""
        **Purpose:** Initial candidate screening and technical assessment
        
        **Features:**
        - Collect candidate information
        - Generate tech-specific questions
        - Professional conversation flow
        - Privacy-focused design
        
        **Tech Stack:**
        - Python
        - Streamlit
        - OpenAI API
        - GPT-3.5-turbo
        """)
        
        st.markdown("---")
        
        # Export conversation option
        if st.session_state.conversation_started and st.session_state.messages:
            if st.button("📥 Download Conversation", key="download_conv"):
                # Create a summary of the conversation
                summary = {
                    "timestamp": datetime.now().isoformat(),
                    "total_messages": len(st.session_state.messages),
                    "candidate_info": st.session_state.chatbot.get_masked_candidate_info(),
                    "conversation_ended": st.session_state.chatbot.is_conversation_complete()
                }
                
                summary_json = json.dumps(summary, indent=2)
                st.download_button(
                    label="📄 Download as JSON",
                    data=summary_json,
                    file_name=f"talentscout_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

def anonymize_email_display(email: str) -> str:
    """Display anonymized email"""
    if '@' not in email:
        return "***"
    local, domain = email.split('@')
    if len(local) > 2:
        anonymized = local[0] + '*' * (len(local) - 2) + local[-1]
    else:
        anonymized = '*' * len(local)
    return f"{anonymized}@{domain}"

def anonymize_phone_display(phone: str) -> str:
    """Display anonymized phone"""
    import re
    cleaned = re.sub(r'[\s\-\+\(\)]+', '', phone)
    return '*' * (len(cleaned) - 4) + cleaned[-4:] if len(cleaned) > 4 else '*' * len(cleaned)

def display_chat_interface():
    """Display the main chat interface"""
    # Initialize session state
    initialize_session_state()
    
    # Check for errors
    if st.session_state.chatbot is None:
        st.error(f"❌ Error: {st.session_state.error}")
        st.info("Please set up your OpenAI API key in the `.env` file with `OPENAI_API_KEY=your_key_here`")
        return
    
    # Start conversation if not started
    if not st.session_state.conversation_started:
        greeting = st.session_state.chatbot.start_conversation()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.session_state.conversation_started = True
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])
    
    # Chat input
    if not st.session_state.chatbot.is_conversation_complete():
        user_input = st.chat_input("Your message:", key="user_input_field")
        
        if user_input:
            # Display user message
            with st.chat_message("user", avatar="👤"):
                st.write(user_input)
            
            # Get chatbot response
            with st.spinner("🤔 Thinking..."):
                response, conversation_ended = st.session_state.chatbot.process_user_input(user_input)
            
            # Display assistant response
            with st.chat_message("assistant", avatar="🤖"):
                st.write(response)
            
            # Add to message history
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Handle conversation end
            if conversation_ended:
                st.markdown("""
                <div class="success-box">
                    <strong>✅ Conversation Ended</strong>
                    <p>Thank you for using TalentScout's Hiring Assistant!</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Offer to view summary
                st.markdown("### 📊 Conversation Summary")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📋 View Full Summary"):
                        summary = {
                            "timestamp": datetime.now().isoformat(),
                            "total_messages": len(st.session_state.messages),
                            "candidate_info": st.session_state.chatbot.get_masked_candidate_info(),
                            "conversation_ended": True
                        }
                        st.json(summary)
                
                with col2:
                    # Option to start new conversation
                    if st.button("🔄 Start New Conversation"):
                        st.session_state.clear()
                        st.rerun()
            
            st.rerun()
    else:
        # Conversation has ended, show summary or start new
        st.markdown("""
        <div class="success-box">
            <strong>✅ Thank You!</strong>
            <p>Your conversation with the Hiring Assistant has been completed.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Start New Conversation"):
            st.session_state.clear()
            st.rerun()

def main():
    """Main application function"""
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar_info()
    
    # Display main chat interface
    display_chat_interface()

if __name__ == "__main__":
    main()
