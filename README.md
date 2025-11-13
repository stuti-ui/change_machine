# Chatbot Streamlit UI

A Streamlit-based user interface for a chatbot that sends user prompts to a POST API and displays the response.

## Features

- 💬 Clean and intuitive chat interface
- 🔌 Configurable API endpoint
- 📝 Chat history preservation
- 🎨 Modern UI with Streamlit chat components
- ⚙️ Easy configuration via sidebar

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Configure the API endpoint:
   - Open the sidebar (click the arrow on the left)
   - Enter your POST API endpoint URL
   - The API should accept JSON payloads with a `query` or `prompt` field

3. Start chatting:
   - Type your message in the chat input at the bottom
   - Press Enter or click Send
   - The chatbot response will appear in the chat

## API Requirements

The POST API endpoint should:
- Accept JSON payloads with `Content-Type: application/json`
- Accept a field named `query` or `prompt` containing the user's message
- Return a JSON response with the chatbot's reply

### Expected Request Format:
```json
{
  "query": "user's message here",
  "prompt": "user's message here"
}
```

### Expected Response Format:
The app will try to extract the response from common field names:
- `response`
- `message`
- `text`
- `answer`
- `content`
- `output`

If none of these are found, the entire JSON response will be displayed.

## Example API Response Formats

```json
{
  "response": "This is the chatbot's reply"
}
```

or

```json
{
  "message": "This is the chatbot's reply"
}
```

or

```json
{
  "answer": "This is the chatbot's reply"
}
```

## Customization

You can modify `app.py` to:
- Change the request payload format
- Adjust the response parsing logic
- Add authentication headers
- Customize the UI appearance

