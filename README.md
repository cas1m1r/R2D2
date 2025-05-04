# R2D2
AI Discord Bot for your Ollama instance.

# Setup
Create a `.env` file containing something for the following:
```
URL=IP_OF_LLAMA_INSTANCE
TOKEN=DISCORD_BOT_TOKEN
GUILD=DISCORD_SERVER_NAME
```
Note:
 * The code assumes your llama instance is running on port 11434 (the Ollama default).
 * The code will query 'gemma3:4b' and 'qwen2.5-coder:7b' models by default. Change the section in `bot.py` as below to use your own models for respective commands:
```python
llms = {'chat': ['gemma3:4b'],
        'code': ['qwen2.5-coder:7b']}
```
