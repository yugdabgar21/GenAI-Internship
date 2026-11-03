# Day 20: Cafe AI agent with a think, act, observe loop

A CLI cafe bot that is driven by the user prompt. The model decides which tool to call, reads the result, and can call another tool before it writes the final answer.

## What it does

1. You type a question such as "what is on the menu and how much is a cappuccino?".
2. The model reads the prompt and asks for a tool, for example `get_menu`.
3. The script runs the tool and appends the output as a `tool` message.
4. The model reads that output and either asks for another tool or writes the answer.

Because the request sits in a loop, the model can chain calls. For example, it can fetch the menu first and then check a single item price.

## The loop

Each pass has three parts:

- **Think:** call the model with `tools=tools` and `tool_choice="auto"`.
- **Act:** if the model returns tool calls, run each one through `tool_call`.
- **Observe:** append each result with its `tool_call_id` and call the model again.

The loop stops when the model returns a message with no tool calls. It also stops after 5 rounds and prints a message instead of hanging.

## Tools

- `get_menu`: returns the full cafe menu with prices. Takes no arguments.
- `price`: takes one `item` argument and returns its price, or "Item not found".
- `web_search`: takes one `query` argument and returns the top 3 DDGS snippets. It is used for topics outside the cafe.

## Files

- `ai.py`: menu data, tools, dispatcher and the agent loop
- `requirements.txt`: dependencies
- `.env.example`: copy this to `.env` and add your key
- `.gitignore`: keeps `.env` out of git

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
python ai.py
```

Type `exit`, `quit` or `stop` to end the chat.

## Sample questions

- What is on the menu?
- How much is a cappuccino?
- Do you have cold brew, and what does it cost?
- Show the menu and tell me the cheapest item.
- What is a flat white? (uses `web_search`)
- Is matcha latte cheaper than mocha?

## Notes

- The menu is a hardcoded dict in `ai.py`. Change it to use your own items and prices.
- The system prompt tells the model to use tools for menu and price questions, so it does not guess numbers.
- A single prompt can trigger several tools across several loop rounds.
- If the model keeps asking for tools after 5 rounds, the agent stops with a short message.
