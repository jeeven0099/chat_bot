# AI Jeeven — Personalized Chatbot

**AI Jeeven** is a personal conversational agent fine-tuned to mimic your texting style. It uses your exported WhatsApp chats to train a LoRA-adapted LLaMA-2 model to reply like you would — short, natural, and context-aware.

---

##  Features

- Mimics *your voice* by learning from real WhatsApp conversations  
- Supports **mixed formatting styles**: one-word replies, multi-line bursts, etc.  
- Efficient fine-tuning using **LoRA / QLoRA** — only small adapter weights are trained  
- Quantization (4-bit) + memory optimizations to run on limited hardware  
- Auto-resume support: if training stops (e.g. disconnect), it picks up from the last checkpoint  
- Chat interface (in Colab or local) with context history and filtering to keep responses coherent  

---

##  Repository Structure

chat_bot/
├── prepare_whatsapp/ # scripts for cleaning & formatting WhatsApp exports
│ └── (e.g. parse, filtering)
├── train_qlora.py # script to fine-tune LLaMA-2 with LoRA adapters
├── chatbot.py # inference / interactive chat script
├── check.py / classify_texts.py # utility / analysis scripts
└── README.md # this file

---

##  Getting Started

### 1. Export & clean your WhatsApp chat

- Export the chat from WhatsApp (TXT format).  
- Use `prepare_whatsapp/` scripts to clean the file (remove metadata like “This message was edited”, merge lines, filter out noise).  
- The cleaned file should look like:
  

### 2. Generate your training data

Run the preprocessing script (e.g. inside `prepare_whatsapp/`) to convert the cleaned WhatsApp export into a JSONL file. The JSONL entries should be in chat-style format (system + conversation context + target reply).  

### 3. Fine-tune the model (train_qlora.py)

Use a script like `train_qlora.py` (or your Colab version) to fine-tune LLaMA-2 with LoRA adapters.

Key steps:

- Load the JSONL dataset  
- Tokenize text (with truncation, padding)  
- Load base model with quantization config  
- Wrap with LoRA adapters  
- Train with `Trainer`, saving checkpoints frequently  
- Auto-resume logic to continue on disconnections  

### 4. Chat / Inference

Use `chatbot.py` (or interactive Colab notebook) to talk with your AI Jeeven. That script:

- Loads the base + LoRA adapter  
- Maintains a conversation history (so context is remembered)  
- Generates replies using your style  
- Filters out extraneous speaker labels or role confusion  

---

## 📋 Key Design Decisions & Trade-offs

| Decision | Why / Benefit | Trade-off / Risk |
|---|---|---|
| **LoRA / QLoRA** | Efficient — only trains small adapter layers | May have less expressiveness than full fine-tuning |
| **4-bit quantization** | Enables large model on limited GPU | Slight loss in precision / performance |
| **Mixed formatting in dataset** | Captures how you actually text | If dataset unbalanced, model may mispredict style |
| **Auto-resume checkpoints** | Allows longer training sessions despite disconnections | Requires careful checkpoint management |
| **Filtering outputs** | Keeps responses coherent (removes “Lauren:” lines, etc.) | Risk of trimming legitimate content if filter too strict |

---

##  Example Usage (Colab / Local)

### Colab (GPU-enabled)

1. Mount Google Drive  
2. Upload JSONL dataset  
3. Run `train_qlora.py` (or the Colab-adapted script)  
4. Resume if disconnected  
5. After training, use `chatbot.py` to chat interactively  

### Local (Inference only)

You can also deploy the chatbot locally (if you have enough GPU) using the same loading code:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# Quantization config
bnb = BitsAndBytesConfig(
  load_in_4bit=True,
  bnb_4bit_compute_dtype="float16",
  bnb_4bit_quant_type="nf4",
  bnb_4bit_use_double_quant=True
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
base = AutoModelForCausalLM.from_pretrained(MODEL_ID, quantization_config=bnb, device_map="auto")
model = PeftModel.from_pretrained(base, OUT_DIR)

# Then do generation, with context and filtering as in chatbot.py
