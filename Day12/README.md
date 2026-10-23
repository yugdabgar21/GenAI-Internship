# Day 12: AI Customer Support Dashboard

A Streamlit app that reads a customer support message, returns a structured triage, and drafts a reply.

## What it does

1. Takes a customer message in a text area.
2. Calls Mistral at a low temperature (0.2) with a JSON response format. The model returns sentiment, category, urgency, and the key issue.
3. Calls Mistral again at a higher temperature (0.7) to write the reply. The tone can be apologetic, professional, or friendly.
4. Shows urgency, sentiment, and category as metrics. The reply appears in an editable text box with a simulated send button.
5. Shows the token count and a rough cost estimate.

The tone can be picked by hand or set from the sentiment. Negative messages get an apologetic reply and positive messages get a friendly one.

## Files

- `customer_support_dashboard.py`: the app
- `requirements.txt`: dependencies
- `.env`: holds `MISTRAL_API_KEY` (not committed)
- `.gitignore`: keeps secrets and caches out of git

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
streamlit run customer_support_dashboard.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to GitHub.
2. Create a new app and point it at `Day12/customer_support_dashboard.py`.
3. Add `MISTRAL_API_KEY` under app secrets.

## Example

Input:

> I was charged twice for order #4521 and nobody is replying. This is unacceptable.

Output:

- Urgency: 4/5
- Sentiment: Negative
- Category: Billing
- Key issue: double charged
- Tone used: apologetic
- Reply: an apology with a refund next step, ready to edit before sending
