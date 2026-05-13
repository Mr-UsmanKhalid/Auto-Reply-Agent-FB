from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from sheet import load_faq

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="qwen/qwen3-32b",
    temperature=0,
)

faq_data = load_faq()


# =========================
# FAQ Matching
# =========================
def faq_reply(msg):

    msg = msg.strip().lower()

    for k in faq_data:

        keyword = k.strip().lower()

        # Exact match
        if keyword == msg:
            return faq_data[k]

        # Partial match
        if keyword in msg:
            return faq_data[k]

    return None


# =========================
# AI Reply
# =========================
def ai_reply(msg):

    prompt = f"""
You are a helpful Facebook Marketplace assistant.

Rules:
- Reply short
- Friendly tone
- Human-like
- NOT spammy
- Avoid long paragraphs
- Avoid excessive emojis

User message:
{msg}
"""

    res = llm.invoke(prompt)

    return res.content.strip()


# =========================
# Main Function
# =========================
def get_reply(msg):

    reply = faq_reply(msg)

    if reply:
        return reply

    return ai_reply(msg)