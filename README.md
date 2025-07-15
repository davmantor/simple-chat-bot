# Simple Chatbot

This is a minimal chatbot project that uses **FastAPI** on the backend and a basic **HTML/JS** frontend. It sends messages to a real LLM (like Claude from Anthropic) and shows the response in a chat interface.

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/davmantor/simple-chat-bot.git
cd simple-chat-bot
```

### 2. Install dependencies

Make sure you have Python 3.10+ and `pip`.

```bash
pip install fastapi uvicorn python-dotenv httpx
```

### 3. Set up `.env`

Create a `.env` file in the root folder with these values:

```
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=https://api.anthropic.com/v1/messages
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

> ⚠️ **Important:** Add `.env` to your `.gitignore` file so you don’t accidentally commit your secret API key.

Example `.gitignore`:

```
.env
__pycache__/
```

### 4. Run the app

```bash
uvicorn main:app --reload
```

Then open your browser to:
**[http://localhost:8000](http://localhost:8000)**

---

## File Structure

```
.
├── main.py        # FastAPI backend
├── chat.html      # Frontend UI
├── .env           # Secret keys (not included in repo)
├── README.md
```

---

## Notes

* All the logic is in one HTML + one Python file.
* The `main.py` file handles the chat logic and sends messages to the LLM.
* The `chat.html` file handles the interface and shows the conversation.
* Never commit API keys. Always use `.env` and `.gitignore`.

---

## Using Other APIs

This project is set up for **Anthropic's API**, but you can adapt it for **OpenAI**, **Mistral**, or any other provider.

To switch:

* Update the `.env` with the new API base URL and model name.
* Modify the `chat()` function in `main.py` to match the new provider's payload format and response structure.

If you're using OpenAI, you'll probably send messages in a format like:

```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Hi there"}
  ]
}
```

You’ll also extract the bot's reply from something like `response["choices"][0]["message"]["content"]`.
