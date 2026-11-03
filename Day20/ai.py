import os, json, sys
from mistralai.client import Mistral
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()

# Windows console can choke on unicode such as the rupee sign
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# cafe menu : item -> price
menu = {
    "espresso": 80,
    "americano": 100,
    "cappuccino": 120,
    "latte": 130,
    "mocha": 150,
    "cold brew": 140,
    "iced latte": 130,
    "matcha latte": 160,
    "hot chocolate": 120,
    "tea": 50,
    "croissant": 90,
    "muffin": 80,
    "brownie": 100,
    "cookies": 60,
    "sandwich": 150,
}

# create tool

def get_menu():
    res = []
    for item in menu:
        res.append(f"{item} - {menu[item]}")
    return json.dumps(res)

def web_search(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)

    if results:
        text = ""
        for result in results:
            body = result.get("body")
            if body:
                text += body + "\n"
        return text if text else f"{query} not found"
    else:
        return f"{query} not found"

def price(item):
    item = item.lower().strip()
    if item in menu:
        return f"{item} cost {menu[item]}"
    else:
        return "Item not found"

# tool schema

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "get the full cafe menu with items and prices",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search on web based on any topic which provide through user query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "string query to search on web"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "price",
            "description": "Show price of a particular item from the cafe menu",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "item to search price on menu"
                    }
                },
                "required": ["item"]
            }
        }
    },
]

# dispatcher

def tool_call(name, args):
    if name == "get_menu":
        return get_menu()
    elif name == "web_search":
        return web_search(args["query"])
    elif name == "price":
        return price(args["item"])
    else:
        return "Tool not found"


# AI agent : think -> act -> observe loop
# The model keeps control of the conversation. It can ask for one tool,
# read the result, then ask for another tool before giving the final answer.

def ai_agent(user_input):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly cafe helpdesk bot. "
                "Use the tools to answer questions about the menu and prices. "
                "If a question is about something outside the cafe, use web_search. "
                "Keep answers short and clear."
            ),
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    for step in range(5):
        # THINK : let the model decide whether it needs a tool
        msg = client.chat.complete(
            model="mistral-small-latest",
            temperature=0.2,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        if not msg or not msg.choices:
            return "No response received from Mistral."

        response = msg.choices[0].message

        if response is None:
            return "Mistral returned an empty message."

        # No tool needed, so this is the final answer
        if not response.tool_calls:
            return response.content or "No answer generated."

        # ACT : record the assistant message that contains the tool calls
        messages.append(response)

        for tc in response.tool_calls:
            print(f"Tool Used : {tc.function.name}")
            print(f"Arguments Used : {tc.function.arguments}")

            args = json.loads(tc.function.arguments)
            result = tool_call(tc.function.name, args)

            print("Tool Calling and O/P : ")
            print(f"TOOL NAME : {tc.function.name} => O/P : {result}")

            # OBSERVE : send the result back so the model can use it
            messages.append(
                {
                    "role": "tool",
                    "content": result if isinstance(result, str) else json.dumps(result),
                    "tool_call_id": tc.id,
                }
            )

    return "Agent stopped: maximum tool calls reached."


# Main program

if __name__ == "__main__":
    print("================================")
    print("         CAFE AI AGENT")
    print("================================")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "stop"]:
            print("AI Agent: Goodbye!")
            break

        try:
            answer = ai_agent(user_input)
            print("\nAI Agent:", answer)
        except Exception as e:
            print("\nError:", e)
