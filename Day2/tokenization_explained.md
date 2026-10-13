# How Claude, Gemini and ChatGPT break text into tokens

## Tokens in plain words

A token is a small chunk of text that the model reads. It can be a full word, part of a word, or a single sign like a comma. Models do not read sentences the way people do. They read one chunk at a time and guess the next chunk.

Think of it like cutting a sentence into puzzle pieces. Short and common words often stay as one piece. Long or rare words get cut into two or more pieces.

## How ChatGPT breaks text

ChatGPT uses a method called byte pair encoding. It starts with single letters and joins pairs that appear often in training text.

Common words like and or shop often stay as one token. A longer word like unhappy may split into un and happy. A sentence of 100 words is often about 130 tokens in English. Other languages may need more tokens for the same meaning.

OpenAI provides a public tool called a tokenizer where you can paste text and see the split.

## How Claude breaks text

Claude also groups letters based on how often they appear together. The idea is close to ChatGPT, but the exact list of pieces is different. Each model learns its own list during training.

Claude counts tokens in a similar way. English text of 100 words is often near 130 to 150 tokens. Code and mixed language text often take more tokens. Anthropic shows the token count in its console when you test a prompt.

## How Gemini breaks text

Gemini uses a method called SentencePiece. It can split text without needing spaces first, which helps with many languages.

For English, the result looks much like the other two. Common words stay whole. Rare names and web addresses split into many pieces. Google reports token counts in AI Studio so you can check cost before you send a request.

## One example

Take this review from a clothing store:

Love the black hoodie, super comfy!

A model may split it like this:

Love | the | black | hood | ie | comma | super | comf | y | exclamation-mark

Small words stay whole. Words like hoodie and comfy split because the model stores their parts, not the full form.
