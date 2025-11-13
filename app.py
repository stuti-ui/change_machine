import streamlit as st
import requests
import json
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Change machine chatbot",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_url" not in st.session_state:
    st.session_state.api_url = ""

def send_query_to_api(query: str, api_url: str) -> Optional[dict]:
    """
    Send user query to POST API endpoint
    
    Args:
        query: User's input query
        api_url: API endpoint URL
        
    Returns:
        API response as dictionary or None if error
    """
    try:
        # Prepare the request payload
        payload = {
            "query": query# Some APIs might expect "prompt" instead of "query"
        }
        
        
        # Make POST request
        response = requests.post(
            api_url,
            json=payload
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Return response as JSON
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None
    except json.JSONDecodeError:
        st.error("Error: API returned invalid JSON response")
        return None

def main():
    st.title("💬 Change Machine ChatBot")
    st.session_state.api_url = "https://stuti-ui.app.n8n.cloud/webhook/rag-webhook"

    if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    if st.button("Refresh database"):
        # Make POST request
        response = requests.post(
            "",
            json={}
        )
        response.raise_for_status()
        st.rerun()
    
    # Main chat interface
    if not st.session_state.api_url:
        st.info("👈 Please configure the API endpoint URL in the sidebar to start chatting.")
    else:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        user_query = st.chat_input("Type your message here...")
        
        if user_query:
            # Add user message to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": user_query
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_query)
            
            # Get response from API
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    api_response = send_query_to_api(user_query, st.session_state.api_url)
                    
                    if api_response:
                        # Try to extract the response text from various possible response formats
                        response_text = None
                        
                        if isinstance(api_response, dict):
                            # Common response field names
                            for key in ["response", "message", "text", "answer", "content", "output"]:
                                if key in api_response:
                                    response_text = api_response[key]
                                    break
                            
                            # If no common key found, display the whole response
                            if response_text is None:
                                response_text = ""
                        elif isinstance(api_response, str):
                            response_text = api_response
                        else:
                            response_text = str(api_response)
                        
                        # Display the response
                        st.markdown(response_text)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text
                        })
                    else:
                        error_msg = "Sorry, I encountered an error processing your request."
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })

if __name__ == "__main__":
    main()

