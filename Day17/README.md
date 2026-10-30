# Day 17: College timetable bot with tool calling

A CLI bot that answers timetable questions. The model does not know the schedule; it calls a `get_timetable` tool and replies from the result.

## What it does

1. You type a question such as "when is my Python lab?".
2. The model returns a tool call for `get_timetable` instead of answering from memory.
3. The script runs `get_timetable()`, which flattens the weekly timetable into plain lines, then sends those lines back as a `tool` message.
4. The model answers from the tool output. If the subject is not in the timetable, it says so.

The tool takes no arguments, so the whole schema is `{"type": "object", "properties": {}}`.

## Files

- `timetable_bot.py`: everything runs from here, including the timetable data and the tool loop
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
python timetable_bot.py
```

## Sample questions

- What is on Thursday?
- When is my Python lab?
- Which room is DBMS in?
- What time does Machine Learning start on Wednesday?
- Do I have a free slot on Friday?

## The tool loop

The model can ask for a tool more than once, so the request sits in a loop:

- Call the model with `tools=tools` and `tool_choice="auto"`.
- If there are no tool calls, print the answer.
- If there are tool calls, append the assistant message, then run each tool and append one tool message per call with its `tool_call_id`.
- The loop allows 5 rounds, then exits with a message instead of hanging.

## Notes

- The timetable is a hardcoded dict in the script. Change the dict to use your own schedule.
- The system prompt forces a tool call before any schedule answer, so the model cannot invent a lecture.
- The answer quality is limited by the data. Add subjects to the dict if the bot says something is missing.
