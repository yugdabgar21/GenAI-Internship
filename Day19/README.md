# Day 19: Cafe menu bot with tool calling

A CLI bot that answers questions about a cafe menu. The model does not know the menu or prices; it calls tools and replies from the result.

## What it does

1. You type a question such as "how much is a cappuccino?".
2. The model returns a tool call such as `price` or `get_menu` instead of answering from memory.
3. The script runs the matching function and sends the output back as a `tool` message.
4. The model answers from the tool output.

## Tools

- `get_menu`: returns the full menu with prices. Takes no arguments.
- `price`: takes one `item` argument and returns its price, or "Item not found".
- `web_search`: takes one `query` argument and returns the top 3 search result snippets.

## Files

- `cafe_bot.py`: menu data, tool functions, tool schema, dispatcher and the tool-call flow
- `requirements.txt`: dependencies
- `.env.example`: copy this to `.env` and add your key
- `.gitignore`: keeps the key out of git

## Run locally

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
MISTRAL_API_KEY=your_key_here
```

Start the bot:

```bash
python cafe_bot.py
```

## Sample questions

- What is on the menu?
- How much is a cappuccino?
- Do you have cold brew?
- What is a flat white? (the model can use `web_search`)
- Which item is cheapest?

## Notes

- The menu is a hardcoded dict in the script. Change it to use your own items and prices.
- The `price` tool schema uses `required: ["item"]`, matching the handler.
- `web_search` joins the top 3 result snippets into one string.
