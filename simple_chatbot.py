"""
Part 1: Simple Chatbot - Build this together!

This is the starting point. We'll build this step-by-step,
then add RAG and search capabilities later.
"""

import streamlit as st
from ollama import chat

# Set up the page
st.title("🤖 My First AI Chatbot")
st.write("Let's build a chatbot together!")

# Initialize session state - this keeps data between page refreshes
# Think of it like the chatbot's memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if prompt := st.chat_input("Type your message here..."):
    
    # Add user message to our history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from AI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call Ollama with our chat history
            response = chat(
                model='llama3.2',  # The AI model we're using
                messages=st.session_state.messages  # Send all previous messages
            )
            
            # Extract the response text
            ai_response = response['message']['content']
            
            # Display it
            st.write(ai_response)
    
    # Add AI response to our history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Add a button to clear the chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Instructions
st.divider()
st.caption("💡 The AI remembers your conversation because we store messages in session_state!")
