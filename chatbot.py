import random
import re

# Load your messages from the exported chat
with open("_chat.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract only your messages
your_messages = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    match = re.match(r"\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2}.*\] Jeeven: (.*)", line)
    if match:
        your_messages.append(match.group(1))

# Style parameters
AVG_WORDS = 6
PUNCTUATION_PROB = 0.2
EMOJI_PROB = 0.02

# Context-aware reply generator
def generate_reply(context_messages, style_examples=15):
    friend_messages = [m for m in context_messages if not m.startswith("Jeeven:")]
    keywords = []
    for msg in friend_messages[-2:]:
        keywords += [w for w in re.findall(r'\w+', msg) if len(w) > 2]

    samples = random.sample(your_messages, min(style_examples, len(your_messages)))
    base_reply = random.choice(samples)

    words = base_reply.split()
    if len(words) > AVG_WORDS:
        words = words[:AVG_WORDS]
    elif len(words) < AVG_WORDS:
        filler = random.choice(samples).split()
        words += filler[:AVG_WORDS - len(words)]
    base_reply = ' '.join(words)

    if keywords:
        word_to_insert = random.choice(keywords)
        reply_words = base_reply.split()
        idx = random.randint(0, len(reply_words)-1)
        reply_words[idx] = word_to_insert
        base_reply = ' '.join(reply_words)

    if random.random() < PUNCTUATION_PROB:
        base_reply += "!" if random.random() < 0.5 else "?"

    if random.random() < EMOJI_PROB:
        base_reply += " 🙂"

    return base_reply

# Interactive chat loop
chat_history = []

print("=== Chat with AI Jeeven ===")
print("Type 'exit' to quit\n")

while True:
    user_message = input("Friend: ")
    if user_message.lower() == "exit":
        break

    chat_history.append("Friend: " + user_message)
    ai_reply = generate_reply(chat_history)
    chat_history.append("Jeeven: " + ai_reply)
    print("AI Jeeven:", ai_reply)
