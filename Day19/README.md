# Day 19: Tool-calling bots

This folder has two bots built on the same idea: the model does not know the data, so it calls tools and answers from the tool result. They differ in domain, web search provider, and interface.

- `cafe_bot.py`: command line cafe menu bot, uses DDGS for web search
- `streamlit_tavily_bot.py`: Streamlit stationery and art supplies bot, uses Tavily for web search

## 1. Cafe menu bot (CLI, DDGS)

A CLI bot that answers questions about a cafe menu.

### What it does

1. You type a question such as "how much is a cappuccino?".
2. The model returns a tool call such as `price` or `get_menu` instead of answering from memory.
3. The script runs the matching function and sends the output back as a `tool` message.
4. The model answers from the tool output.

### Tools

- `get_menu`: returns the full menu with prices. Takes no arguments.
- `price`: takes one `item` argument and returns its price, or "Item not found".
- `web_search`: takes one `query` argument and returns the top 3 DDGS snippets.

### Run

```bash
python cafe_bot.py
```

### Sample questions

- What is on the menu?
- How much is a cappuccino?
- Do you have cold brew?
- What is a flat white? (uses `web_search`)
- Which item is cheapest?

## 2. Stationery and art supplies bot (Streamlit, Tavily)

A Streamlit chat app for a stationery and art supplies store. Web search runs through the Tavily API.

### What it does

1. You type a question in the chat box.
2. The model can call `get_menu`, `price`, or `web_search`.
3. Tool results are sent back to the model, which writes the final answer.
4. Each tool call is shown in an expander under the answer.

### Tools

- `get_menu`: returns the full store menu with prices. Takes no arguments.
- `price`: takes one `item` argument and returns its price, or "Item not found".
- `web_search`: takes one `query` argument, calls Tavily, and returns the top 3 result snippets.

### Run

```bash
streamlit run streamlit_tavily_bot.py
```

The app opens in a browser. You can enter keys in the sidebar or keep them in `.env`.

### Sample questions

- Show the full menu, search the web for what gouache paint is, and tell me the price of a sketchbook.
- How much is a marker set?
- Difference between acrylic and watercolor paint
- Which item is the cheapest?

## Files

- `cafe_bot.py`: cafe menu data, tools, dispatcher and the CLI tool-call flow
- `streamlit_tavily_bot.py`: stationery menu data, tools, Tavily search and the Streamlit chat UI
- `requirements.txt`: dependencies for both bots
- `.env.example`: copy this to `.env` and add your keys
- `.gitignore`: keeps `.env` out of git

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
MISTRAL_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

`TAVILY_API_KEY` is only needed for the Streamlit bot.

## Notes

- Both menus are hardcoded dicts. Change them to use your own items and prices.
- The `price` tool schema uses `required: ["item"]`, matching the handler.
- `web_search` joins the top 3 result snippets into one string.
- The CLI bot handles one round of tool calls. The Streamlit bot uses a loop of up to 5 rounds, so it can chain tools across steps.
