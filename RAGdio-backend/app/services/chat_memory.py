from collections import defaultdict, deque

# Store only per-chat session (up to 10 turns), not user-specific
chat_history = defaultdict(lambda: {
    "turns": deque(maxlen=10),   # rolling memory
    "summary": "",               # optional summary
    "context": ""                # injected background (RAG/system)
})

def get_chat_context(chat_id: str):
    return chat_history[chat_id]

def append_turn(chat_id: str, role: str, content: str):
    chat_history[chat_id]["turns"].append({
        "role": role,
        "content": content,
    })

def build_prompt(chat_id: str, user_input: str):
    store = chat_history[chat_id]
    summary = store["summary"]
    context = store["context"]

    full_prompt = ""
    if summary:
        full_prompt += f"[Summary]: {summary}\n\n"
    if context:
        full_prompt += f"[Context]: {context}\n\n"
    
    for turn in store["turns"]:
        full_prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
    full_prompt += f"User: {user_input}"
    return full_prompt
