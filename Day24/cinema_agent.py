import os
import json

from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# --------------------------------
# COMPANY DATABASE (DEMO)
# --------------------------------

bookings = {
    "BK201": "Confirmed - 2 tickets, Screen 3, 7:30 PM show",
    "BK202": "Cancelled - refund issued, reaches your account in 3-5 days"
}

menu = {
    "popcorn": 180,
    "nachos": 220,
    "coke": 120,
    "water": 40,
    "coffee": 100,
    "samosa": 60
}


# --------------------------------
# TOOLS
# --------------------------------

def track_booking(booking_id):
    booking_id = booking_id.upper()

    if booking_id in bookings:
        return bookings[booking_id]

    return "Booking not found."


def get_menu():
    result = ""

    for k, v in menu.items():
        result += k + " - Rs " + str(v) + "\n"

    return result


def check_price(item):
    item = item.lower()

    if item in menu:
        return item + " costs Rs " + str(menu[item])

    return item + " not on menu"


# --------------------------------
# TOOL EXECUTOR
# --------------------------------

def run_tool(name, args):

    if name == "track_booking":
        return track_booking(args["booking_id"])

    elif name == "get_menu":
        return get_menu()

    elif name == "check_price":
        return check_price(args["item"])

    else:
        return "Unknown tool"


# --------------------------------
# BOOKING TOOLS
# --------------------------------

booking_tools = [
    {
        "type": "function",
        "function": {
            "name": "track_booking",
            "description": "Track a cinema booking by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "string",
                        "description": "e.g. BK201"
                    }
                },
                "required": ["booking_id"]
            }
        }
    }
]


# --------------------------------
# SNACKS TOOLS
# --------------------------------

snacks_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get the full snacks menu with prices",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_price",
            "description": "Get the price of a snack or drink",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Snack or drink name"
                    }
                },
                "required": ["item"]
            }
        }
    }
]


# --------------------------------
# SPECIALIST AGENT
# --------------------------------

def run_specialist(system_prompt, query, tools):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:

        # Preserve assistant tool-call message
        messages.append(msg)

        for tc in msg.tool_calls:

            args = json.loads(tc.function.arguments)

            result = run_tool(
                tc.function.name,
                args
            )

            print(f"{tc.function.name} => {result}")

            messages.append({
                "role": "tool",
                "name": tc.function.name,
                "content": str(result),
                "tool_call_id": tc.id
            })

        final = client.chat.complete(
            model="mistral-small-latest",
            messages=messages
        )

        return final.choices[0].message.content

    return msg.content


# --------------------------------
# ROUTER AGENT
# --------------------------------

def route(query):

    r = client.chat.complete(
        model="mistral-small-latest",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                You are a query router.

                Reply with ONE word only:

                booking - Cinema ticket, booking, show, and seat questions.
                snacks  - Snacks menu and price questions.
                general - Everything else.
                """
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return r.choices[0].message.content.strip().lower()


# --------------------------------
# MAIN APPLICATION
# --------------------------------

query = input("Customer: ")

category = route(query)

print(f"Routed to: {category} Agent")


if category == "booking":

    answer = run_specialist(
        "You are a polite cinema booking support agent. Use the track_booking tool to help customers.",
        query,
        booking_tools
    )

elif category == "snacks":

    answer = run_specialist(
        "You are a friendly snacks counter assistant. Use get_menu and check_price to help customers.",
        query,
        snacks_tools
    )

else:

    answer = run_specialist(
        "You are a helpful cinema support agent. Answer the customer politely.",
        query,
        []
    )


print("Support:", answer)
