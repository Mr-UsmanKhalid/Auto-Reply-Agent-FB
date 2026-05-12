from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from sheet import load_faq

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="qwen/qwen3-32b",
    temperature=0,
)

faq_data = load_faq()


def faq_reply(msg):
    msg = msg.lower()

    for k in faq_data:
        if k in msg:
            return faq_data[k]

    return None


def ai_reply(msg):
    prompt = f"""
You are a helpful Marketplace assistant.
Reply short, polite, and NOT spammy.

User: {msg}
"""

    res = llm.invoke(prompt)

    return res.content


def get_reply(msg):
    reply = faq_reply(msg)

    if reply:
        return reply

    return ai_reply(msg)