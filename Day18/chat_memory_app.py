import os
import json

import streamlit as st
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

st.set_page_config(
    page_title="Chat Memory App",
    page_icon="💬",
    layout="centered",
)

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


def get_day_schedule(day):
    key = day.strip().lower()
    if key not in timetable:
        return f"No schedule found for '{day}'."
    lines = [f"{time} - {subject} ({room})" for time, subject, room in timetable[key]]
    return f"{key.title()} schedule:\n" + "\n".join(lines)


def find_subject(name):
    needle = name.strip().lower()
    matches = []
    for day, entries in timetable.items():
        for time, subject, room in entries:
            if needle in subject.lower():
                matches.append(f"{day.title()} {time} - {subject} ({room})")
    if not matches:
        return f"Subject '{name}' not found in the timetable."
    return "\n".join(matches)


# tool schemas

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_day_schedule",
            "description": "List all classes on a single weekday (monday to friday).",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "Weekday name, e.g. monday, tuesday.",
                    }
                },
                "required": ["day"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_subject",
            "description": "Find when and where a subject is taught in the timetable.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Subject name to search for.",
                    }
                },
                "required": ["name"],
            },
        },
    },
]


def run_tool(name, args):
    if name == "get_day_schedule":
        day = args.get("day") if isinstance(args, dict) else None
        if not isinstance(day, str) or not day.strip():
            return "Error: missing or invalid 'day' argument."
        return get_day_schedule(day)
    if name == "find_subject":
        subject_name = args.get("name") if isinstance(args, dict) else None
        if not isinstance(subject_name, str) or not subject_name.strip():
            return "Error: missing or invalid 'name' argument."
        return find_subject(subject_name)
    return f"Error: unknown tool '{name}'."


system_prompt = (
    "You are a college helpdesk bot for an IT department. "
    "Use get_day_schedule to list classes on a weekday and find_subject to locate a subject. "
    "Answer in 2 or 3 short lines and mention the day, time and room. "
    "If the timetable does not contain the answer, say so."
)

# sidebar

with st.sidebar:
    st.header("Chat controls")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
    st.caption("Chat history is kept in session state.")

st.title("Chat Memory App")
st.caption("Ask about the college timetable. Powered by Mistral.")

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    st.error("MISTRAL_API_KEY is missing. Add it to your .env file.")
    st.stop()

# chat history

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    role = m["role"] if isinstance(m, dict) else getattr(m, "role", "")
    content = m["content"] if isinstance(m, dict) else getattr(m, "content", "")
    if role in ("user", "assistant") and content:
        st.chat_message(role).write(content)

prompt = st.chat_input("Ask about classes, subjects, timings or rooms...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = Mistral(api_key=api_key)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        for _ in range(5):
            api_messages = [{"role": "system", "content": system_prompt}] + list(
                st.session_state.messages[-10:]
            )

            msg = client.chat.complete(
                model="mistral-small-latest",
                temperature=0.2,
                messages=api_messages,
                tools=tools,
                tool_choice="auto",
            )

            response = msg.choices[0].message

            if not response.tool_calls:
                content = response.content or ""
                st.session_state.messages.append(
                    {"role": "assistant", "content": content}
                )
                placeholder.write(content)
                break

            st.session_state.messages.append(response)

            for tc in response.tool_calls:
                raw_args = getattr(tc.function, "arguments", None)
                try:
                    if raw_args is None or (
                        isinstance(raw_args, str) and not raw_args.strip()
                    ):
                        raise ValueError("missing arguments")
                    args = json.loads(raw_args)
                    if not isinstance(args, dict):
                        raise ValueError("invalid arguments")
                except (json.JSONDecodeError, ValueError, TypeError):
                    result = "Error: tool arguments are missing or invalid JSON."
                else:
                    result = run_tool(tc.function.name, args)

                st.session_state.messages.append(
                    {
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tc.id,
                    }
                )

                with st.expander(f"Tool used: {tc.function.name}", expanded=False):
                    st.write(f"Arguments: `{raw_args}`")
                    st.write(result)
        else:
            placeholder.warning("The model kept asking for tools. Try rephrasing.")
