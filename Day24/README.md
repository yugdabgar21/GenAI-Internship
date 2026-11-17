# Day 24: Cinema support agent with a router and two specialists

A CLI chatbot built on Mistral. A router reads the customer question and sends it to one specialist: booking support, snacks counter, or general support.

## How it works

1. You type a question such as "Where is my booking BK201?" or "How much is popcorn?".
2. A router call (temperature 0) replies with one word: `booking`, `snacks`, or `general`.
3. The matching specialist answers:
   - **booking**: has the `track_booking` tool and reads booking status from a demo table.
   - **snacks**: has the `get_menu` and `check_price` tools for the snacks menu.
   - **general**: no tools, plain polite answer.
4. Each tool call is printed, then the final answer is printed after `Support:`.

This is a single tool round, not a loop: the specialist can call a tool once per question, then writes its answer.

## Demo data

- Bookings: `BK201` (confirmed, 2 tickets, Screen 3, 7:30 PM), `BK202` (cancelled, refund on the way).
- Snacks: popcorn, nachos, coke, water, coffee, samosa.

## Files

- `cinema_agent.py`: the router, the two specialists, the tools, and the CLI.
- `requirements.txt`: the Python packages you need.
- `.env.example`: the key the app expects.

## Setup

Install the packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
MISTRAL_API_KEY=your_mistral_key_here
```

## Run

```bash
python cinema_agent.py
```

## Test inputs

- Where is my booking BK201?
- Can I get a refund for BK202?
- What snacks do you sell?
- How much is popcorn?
- Do you have parking?

## Notes

- The router only knows the three labels. An unclear question usually falls to `general`.
- Booking IDs are case-insensitive because the tool upper-cases them.
- Prices are demo values in rupees.
- `.env` holds the real key. It is ignored by git.
