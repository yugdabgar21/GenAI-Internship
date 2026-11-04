# Day 21: Single and sequential agent variants

Two CLI agents built on Mistral. Both take a topic and print the result.

## Files

- `single_ai_agent.py`: one Mistral call does research + writing + editing and returns a LinkedIn post.
- `multi_ai_agent.py`: three sequential Mistral calls (Research -> Write -> Edit) that return a product review.

## Single agent (`single_ai_agent.py`)

1. You type a topic.
2. One Mistral call (system role = researcher + writer + editor) generates a LinkedIn post.
3. The result is printed: hook, short paragraphs, call to action, hashtags.

## Sequential multi-agent (`multi_ai_agent.py`)

1. You type a product or topic.
2. **Research agent** gathers facts, specs, pros, cons, and feedback.
3. **Writer agent** turns the research into a draft review.
4. **Editor agent** polishes the draft into a publication-ready review.
5. The final review is printed.

The agents run one after another, so each stage feeds the next.

## Run locally

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
MISTRAL_API_KEY=your_key_here
```

Start the single agent:

```bash
python single_ai_agent.py
```

Start the sequential multi-agent:

```bash
python multi_ai_agent.py
```

## Notes

- Sequential means output order matters: the writer needs the research, the editor needs the draft.
- Change the system prompts to target another output type.
- Keep LinkedIn posts under 1300 characters so they fit the platform limit.
