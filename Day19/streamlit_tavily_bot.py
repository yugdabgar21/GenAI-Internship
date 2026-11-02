import os, json
import streamlit as st
from mistralai.client import Mistral
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Stationery & Art Supplies Bot",
    page_icon="🎨",
    layout="centered",
)

st.title("🎨 Stationery & Art Supplies Bot")
st.caption("Ask about items, prices, or art techniques. Powered by Mistral + Tavily.")

# stationery and art supplies : item -> price
menu = {
    "ballpoint pen": 10,
    "gel pen": 25,
    "pencil (pack of 10)": 60,
    "eraser": 8,
    "sharpener": 12,
    "notebook (200 pages)": 90,
    "sketchbook (A4)": 250,
    "watercolor set (12 shades)": 320,
    "acrylic paint (12 tubes)": 450,
    "paint brush set": 180,
    "canvas (12x16 inch)": 300,
    "marker set (24 colors)": 280,
    "highlighter (pack of 5)": 100,
    "geometry box": 150,
    "file folder": 40,
    "sticky notes": 35,
}


# create tool

def get_menu():
    res = []
    for item in menu:
        res.append(f"{item} - {menu[item]}")
    return json.dumps(res)


def price(item):
    if item in menu:
        return f"{item} cost {menu[item]}"
    else:
        return "Item not found"


def web_search(query, tavily_key):
    if not tavily_key:
        return "Tavily API key is missing. Add it in the sidebar or .env."

    tavily_client = TavilyClient(api_key=tavily_key)
    response = tavily_client.search(query, max_results=3)
    results = response.get("results", [])

    if not results:
        return f"{query} not found"

    text = ""
    for result in results:
        text += result.get("content", "") + "\n"
    return text.strip()


# tool schema

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "get the full stationery and art supplies menu with items and prices",
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
            "description": "Search the web using Tavily for art techniques, product info or any other topic",
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
            "description": "Show price of a particular item from the store menu",
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

def tool_call(name, args, tavily_key):
    if name == "get_menu":
        return get_menu()
    elif name == "web_search":
        return web_search(args["query"], tavily_key)
    elif name == "price":
        return price(args["item"])
    else:
        return "Tool not found"


# sidebar keys

with st.sidebar:
    st.header("API keys")
    mistral_key = st.text_input(
        "Mistral API key",
        value=os.getenv("MISTRAL_API_KEY", ""),
        type="password",
    )
    tavily_key = st.text_input(
        "Tavily API key",
        value=os.getenv("TAVILY_API_KEY", ""),
        type="password",
    )
    st.caption("Keys are loaded from .env when present.")

system_prompt = (
    "You are a friendly stationery and art supplies store helpdesk bot. "
    "Use get_menu for menu questions and price for a specific item price. "
    "Use web_search for art techniques, product details or anything outside the store. "
    "Keep answers short and clear."
)

# chat history

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

for m in st.session_state.messages:
    role = m["role"] if isinstance(m, dict) else getattr(m, "role", "")
    content = m["content"] if isinstance(m, dict) else getattr(m, "content", "")
    if role in ("user", "assistant") and content:
        st.chat_message(role).write(content)

prompt = st.chat_input("Ask about stationery or art supplies...")

if prompt:
    if not mistral_key:
        st.error("Add your Mistral API key in the sidebar or .env.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = Mistral(api_key=mistral_key)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        # tool calling loop : keep calling the model until it stops asking for tools
        for _ in range(5):
            msg = client.chat.complete(
                model="mistral-small-latest",
                temperature=0.2,
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto",
            )

            response = msg.choices[0].message

            if not response.tool_calls:
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.content}
                )
                placeholder.write(response.content)
                break

            st.session_state.messages.append(response)

            for tc in response.tool_calls:
                args = json.loads(tc.function.arguments)
                result = tool_call(tc.function.name, args, tavily_key)

                st.session_state.messages.append(
                    {
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tc.id,
                    }
                )

                with st.expander(f"Tool used: {tc.function.name}", expanded=False):
                    st.write(f"Arguments: `{tc.function.arguments}`")
                    st.write(result)
        else:
            placeholder.warning("The model kept asking for tools. Try rephrasing.")
