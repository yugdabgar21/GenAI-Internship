# Day 18: Chat memory app with tools

A Streamlit chat app that remembers the conversation and answers timetable questions through two tools. The model does not know the schedule; it calls a tool and replies from the result.

## What it does

1. You type a question in the chat box.
2. The conversation is stored in `st.session_state.messages` and drawn again on every rerun.
3. Each request sends the system prompt plus the last 10 messages to Mistral.
4. The model can call a tool. The app runs the tool and appends the result, then asks the model again.
5. The tool loop allows up to 5 rounds per question.
6. The sidebar has a Clear chat button that empties the history.

## Tools

- `get_day_schedule(day)`: lists every class on one weekday. Returns each class with its time and room, or a message when the day is unknown.
- `find_subject(name)`: searches all days for a subject name and returns when and where it is taught. The match is case-insensitive and partial.

Both tools require one string argument. The app parses `tc.function.arguments` with `json.loads`. If the arguments are missing, empty or invalid JSON, the tool result is an error message instead of a crash. Missing or wrong argument names also return an error message.

## Files

- `chat_memory_app.py`: timetable data and the Streamlit chat flow
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

Start the app:

```bash
streamlit run chat_memory_app.py
```

The app opens in a browser. If `MISTRAL_API_KEY` is missing, it shows an error and stops.

## Sample questions

- What is on Thursday?
- When is my Python lab?
- Which room is DBMS in?
- When and where is Machine Learning taught?
- What time does the seminar start on Friday?
- Do I have a free slot on Monday?

## Notes

- The timetable is a hardcoded dict in `chat_memory_app.py`. Change the dict to use your own schedule.
- The last 10 messages include tool messages. A long tool chain can push older user and assistant turns out of the request.
- Tool results appear in an expander under the answer, so you can see the arguments and the raw output.
- The app uses `mistral-small-latest` with `temperature=0.2`.
