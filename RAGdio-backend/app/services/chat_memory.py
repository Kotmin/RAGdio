from collections import defaultdict, deque
from app.core.logging_config import logger

from app.routers.llm import pipeline

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

def auto_summarize(chat_id: str):
    store = chat_history[chat_id]
    if len(store["turns"]) < 2:
        return  # wait for more conversation

    history_lines = []
    for turn in store["turns"]:
        role = "User" if turn["role"] == "user" else "Assistant"
        history_lines.append(f"{role}: {turn['content']}")

    full_history = "\n".join(history_lines)

    summary_prompt = (
        "Please summarize the following chat history in bulletpoints:\n\n"
        f"{full_history}"
    )

    try:
        # summary = pipeline.llm.ask(summary_prompt, [])
        result = pipeline.query(summary_prompt)
        summary = result["answer"]
        # summary = summarize_func(summary_prompt)
        chat_history[chat_id]["summary"] = summary.strip()
    except Exception as e:
        logger.warning(f"⚠️ Failed to auto-summarize: {e}")


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
