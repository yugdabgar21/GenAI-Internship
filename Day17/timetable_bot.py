import os, json
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# college timetable : day -> list of (time, subject, room)
timetable = {
    "monday": [
        ("9:00", "DBMS", "B-204"),
        ("10:00", "Operating Systems", "B-204"),
        ("11:30", "Python Lab", "Lab-2"),
        ("2:00", "Mini Project", "Lab-3"),
    ],
    "tuesday": [
        ("9:00", "Computer Networks", "B-206"),
        ("10:00", "DBMS", "B-206"),
        ("11:30", "Web Development Lab", "Lab-1"),
        ("2:00", "Soft Skills", "A-101"),
    ],
    "wednesday": [
        ("9:00", "Operating Systems", "B-204"),
        ("10:00", "Machine Learning", "B-208"),
        ("11:30", "Machine Learning Lab", "Lab-4"),
    ],
    "thursday": [
        ("9:00", "Computer Networks", "B-206"),
        ("10:00", "Python Lab", "Lab-2"),
        ("11:30", "Mini Project", "Lab-3"),
        ("2:00", "Library / Self Study", "Library"),
    ],
    "friday": [
        ("9:00", "Machine Learning", "B-208"),
        ("10:00", "Web Development Lab", "Lab-1"),
        ("11:30", "Seminar", "A-102"),
    ],
}

# create tool

def get_timetable():
    res = []
    for day in timetable:
        for time, subject, room in timetable[day]:
            res.append(f"{day.title()} {time} - {subject} ({room})")
    return res

# print(get_timetable())

# tool schema

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_timetable",
            "description": "get the full weekly college timetable with day, time, subject and room",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

system_prompt = (
    "You are a college helpdesk bot for an IT department. "
    "Always call get_timetable before answering any question about classes, subjects, timings or rooms. "
    "Answer in 2 or 3 short lines and mention the day, time and room. "
    "If the timetable does not contain the answer, say so."
)

user_input = input("BOT : ")

messages = [
    {
        "role": "system",
        "content": system_prompt,
    },
    {
        "role": "user",
        "content": user_input,
    }
]

# tool calling loop : keep calling the model until it stops asking for tools

for _ in range(5):
    msg = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.2,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response = msg.choices[0].message

    if not response.tool_calls:
        print(response.content)
        break

    messages.append(response)

    for tc in response.tool_calls:
        if tc.function.name == "get_timetable":
            result = get_timetable()
        else:
            result = {"error": f"unknown tool : {tc.function.name}"}

        messages.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tc.id,
            }
        )
else:
    print("BOT : the model kept asking for tools, please try again")
