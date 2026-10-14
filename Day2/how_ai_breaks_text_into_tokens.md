# How Claude, Gemini and ChatGPT Break Text into Tokens

## First, what is a "token"?

When you type a message to an AI, the AI does not read it the way you do, word by word. Instead, it first chops your text into small pieces called **tokens**.

A token is a chunk of text. It can be:

- A whole word, like `cat`
- Part of a word, like `ing` in `running`
- A single letter or symbol, like `!`
- A space, or a piece of a space plus a word

Think of it like cutting a sentence into LEGO bricks. The AI works with the bricks, not with the sentence as a whole.

**Example:**

> "Unbelievable!"

might be split into:

`Un` + `believ` + `able` + `!`

That's four tokens, even though it looks like one word plus punctuation.

---

## Why do AIs use tokens instead of whole words?

There are three simple reasons:

1. **Words are endless.** Languages keep adding new words, names, slang, and typos. If the AI only knew whole words, it would be lost whenever it saw something new.
2. **Pieces can be reused.** If the AI knows the piece `un`, it can guess the meaning of `unhappy`, `unlock`, and `undo` without learning each one separately.
3. **It keeps the dictionary manageable.** A list of a few tens of thousands of pieces covers almost all text in every language.

---

## The basic idea of how the cutting works

Most modern AIs use a method called **Byte Pair Encoding (BPE)** or a close cousin of it. Here is the simple version:

1. Start with every single character as its own piece.
2. Look through a huge pile of text and find the two pieces that appear next to each other most often.
3. Glue them together into one new piece.
4. Repeat this thousands of times.

After enough rounds, common things like `the`, `ing`, and `tion` become single pieces, while rare words get split into smaller parts.

It's a bit like a child learning to read: first letters, then common syllables, then whole familiar words.

---

## How each AI does it

The exact recipes are secret or complicated, but here is the general picture.

### Claude (by Anthropic)

- Uses its own tokenizer, trained on a large mix of text.
- Splits ordinary English into fairly large chunks, often whole common words.
- Non-English text, code, and unusual symbols may take more tokens.
- The exact token count can differ from ChatGPT or Gemini for the same sentence.

### ChatGPT (by OpenAI)

- Uses tokenizers from OpenAI's "tiktoken" family, which are based on BPE.
- Newer versions have larger vocabularies, so common words in many languages are more likely to be one token.
- English is usually efficient. Some other languages and code may need more tokens.

### Gemini (by Google)

- Uses a tokenizer built by Google, trained on text in many languages.
- It is designed to handle many scripts (Hindi, Arabic, Chinese, and so on) reasonably well.
- Like the others, it breaks rare words and unusual text into smaller pieces.

**Key takeaway:** All three work on the same basic idea, but each has its own "cutting rules" and its own vocabulary of pieces. So the same sentence may split into different numbers of tokens depending on the AI.

---

## Why should you care?

Tokens matter to you in a few practical ways:

- **Cost:** Many AI services charge by the number of tokens read and written. More tokens means a higher bill.
- **Limits:** Every AI has a maximum "context window," which is the amount of text it can hold at once. This limit is counted in tokens, not words.
- **Language:** Languages with less training data (and some scripts) often need more tokens per sentence. This can make those languages slower and more expensive to use.
- **Odd behavior:** Sometimes an AI struggles to count letters in a word or spell a rare name correctly. That's often because it sees the word as a few chunks, not as individual letters.

---

## A rough rule of thumb

- In English, **1 token is roughly 3/4 of a word**, or about **4 characters**.
- So **100 tokens is roughly 75 English words**.
- Other languages and code can be quite different, so treat this as a rough guide only.


