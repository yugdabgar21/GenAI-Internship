import os, json
from mistralai.client import Mistral
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()

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
    ddgs = DDGS()
    results = ddgs.text(query, max_results=3)
    if results:
        text = ""
        for result in results:
            text += result["body"] + "\n"
        return text
    else:
        return f"{query} not found"

def price(item):
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


user_input = input("BOT : ")

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

msg = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

response = msg.choices[0].message

if response.tool_calls:
    messages.append(response)
    for tc in response.tool_calls:
        print(f"Tool Used : {tc.function.name}")
        print(f"Arguments Used : {tc.function.arguments}")

        args = json.loads(tc.function.arguments)
        result = tool_call(tc.function.name, args)
        print("Tool Calling and O/P : ")
        print(f"TOOL NAME : {tc.function.name} => O/P : {result}")
        messages.append(
            {
                "role": "tool",
                "content": result,
                "tool_call_id": tc.id
            }
        )

    final = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.2,
        messages=messages
    )

    print(final.choices[0].message.content)

else:
    print(response.content)
