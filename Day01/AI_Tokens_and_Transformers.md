# How AI Chatbots Read Words and Use Transformers

*A plain-English guide*

## Part 1: Tokenization and Embeddings

Computers do not read words the way we do. They only work with numbers, so every piece of text has to be converted first. This happens in two steps.

**Step 1 - Tokenization.** The text is chopped into small pieces called tokens. A token is often a whole word, but long or unusual words get split up. For example, "unbelievable" might become "un", "believ" and "able". On average, one token is about three-quarters of an English word. Each token is then swapped for a number from a fixed list (the "vocabulary") that usually holds around 100,000 tokens.

**Step 2 - Embeddings.** Each token number is turned into a long list of numbers (called a vector, often hundreds or thousands of values long). This list is the token's "meaning fingerprint." During training, the model learns these fingerprints so that words with related meanings end up close together. "King" sits near "queen," and "dog" sits near "puppy." Even relationships are captured: the difference between "king" and "man" is similar to the difference between "queen" and "woman."

**Simple analogy:** Tokenization is like cutting a sentence into labeled puzzle pieces. Embeddings are like placing each piece on a giant map of meaning, where similar ideas live in the same neighborhood.

## Part 2: How Companies Use Transformers

**What is a transformer?** A transformer is the design behind almost every modern AI chatbot. It was introduced in a 2017 paper titled "Attention Is All You Need." Its key trick is **attention**: every word in a sentence looks at every other word to decide which ones matter most. In "The bank by the river was muddy," attention helps the model understand that "bank" means a riverbank, not a money bank.

**How chatbots write.** The model reads your tokens, then predicts the most likely next token. It adds that token, predicts the next one, and repeats until the answer is complete. It does this very fast, which is why the text appears to "type out."

Most leading AI companies start from the same transformer design, then differ in how they train and shape their models:

| Company | AI model | How it uses transformers |
| --- | --- | --- |
| OpenAI | ChatGPT (GPT models) | Large transformer trained on huge amounts of text, then fine-tuned with human feedback so answers are more helpful. Handles text, images and voice. |
| Anthropic | Claude | Transformer model trained with a focus on safety and clear written principles. Known for handling very long documents and careful, detailed writing. |
| Google | Gemini | Built to understand text, images, audio and video together from the start. Connected to Google Search and apps like Gmail and Docs. Google also wrote the original transformer paper in 2017. |
| Meta | Llama | Transformer models released with open weights, so anyone can download, run and modify them. Popular for building custom apps. |
| Others | Mistral, DeepSeek, etc. | Many use the same core design but focus on being smaller, cheaper to run, or cheaper to train. |

**Common techniques across companies:**

- **Scaling up:** training on more data with more computing power, which tends to make models more capable.
- **Human feedback:** people rate answers, and the model learns to give responses people prefer.
- **Long memory:** smarter attention methods let models read very long documents or conversations.
- **Mixture of experts:** only a small part of a large model works on each token, which saves time and cost.
- **Tools and search:** models can call calculators, browse the web or use apps to get facts they do not already know.

**Note:** AI companies update their models often, so specific features and rankings change over time. Check each company's website for the latest details.
