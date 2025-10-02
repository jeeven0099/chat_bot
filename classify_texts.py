import emoji
from statistics import mean
import re

# Load your exported chat
with open("_chat.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract only your messages (Jeeven)
your_messages = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    # WhatsApp format: [date, time] Name: message
    match = re.match(r"\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2}.*\] Jeeven: (.*)", line)
    if match:
        your_messages.append(match.group(1))

# Compute style metrics
avg_words = round(mean(len(m.split()) for m in your_messages), 1)
emoji_count = sum(1 for m in your_messages for ch in m if ch in emoji.EMOJI_DATA)
emoji_rate = round(emoji_count / len(your_messages), 2)
punctuation_count = sum(m.count('!') + m.count('?') for m in your_messages)
punctuation_density = round(punctuation_count / len(your_messages), 2)

# Common openers and closers
openers = [m.split()[0] for m in your_messages if len(m.split()) > 0]
closers = [m.split()[-1] for m in your_messages if len(m.split()) > 0]
common_openers = list(set(openers))[:10]
common_closers = list(set(closers))[:10]

print("Number of messages:", len(your_messages))
print("Average words per message:", avg_words)
print("Emoji rate per message:", emoji_rate)
print("Punctuation density:", punctuation_density)
print("Common openers:", common_openers)
print("Common closers:", common_closers)
