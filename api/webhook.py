import json
import random
import requests
from http.server import BaseHTTPRequestHandler

# आपका बॉट टोकन यहाँ फिक्स कर दिया गया है
BOT_TOKEN = "8820307548:AAESeTJkFrwJU4oqLOov5n0ydr11XU0pO6o"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# YouTube Channel Link
YOUTUBE_LINK = "https://youtube.com/@s.kanhaiya.7m"

# Subscribe line (Roman Hindi — same for all)
SUBSCRIBE_LINE = f"Kya tumne channel subscribe kiya?\n👉 {YOUTUBE_LINK}"


# ============================================================
# GROUP WELCOME MESSAGES (English + Hindi)
# ============================================================
GROUP_MESSAGES_EN = [
    "✦ ─────────────────── ✦\n"
    "   Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "Glad you're here ✨",

    "✦ ─────────────────── ✦\n"
    "   Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "So happy to have you ✨",

    "✦ ─────────────────── ✦\n"
    "   Hi {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "Great to see you ✨",

    "✦ ─────────────────── ✦\n"
    "   Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "You made it here ✨",

    "✦ ─────────────────── ✦\n"
    "   Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "You're part of us now ✨",
]

GROUP_MESSAGES_HI = [
    "✦ ─────────────────── ✦\n"
    "   नमस्ते {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "आपका आना अच्छा लगा ✨",

    "✦ ─────────────────── ✦\n"
    "   नमस्ते {name} 👋\n"
    "   {chat} में स्वागत है\n"
    "✦ ─────────────────── ✦\n\n"
    "आपको देखकर खुशी हुई ✨",

    "✦ ─────────────────── ✦\n"
    "   हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "आपसे मिलकर अच्छा लगा ✨",

    "✦ ─────────────────── ✦\n"
    "   नमस्ते {name} 👋\n"
    "   {chat} में स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "आप यहाँ आ गए ✨",

    "✦ ─────────────────── ✦\n"
    "   हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "अब आप हमारे परिवार का हिस्सा हैं ✨",
]


# ============================================================
# CHANNEL WELCOME MESSAGES (English + Hindi)
# ============================================================
CHANNEL_MESSAGES_EN = [
    "✦ ─────────────────── ✦\n"
    "   Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "Glad you're here ✨",

    "✦ ─────────────────── ✦\n"
    "   Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "So happy to have you ✨",

    "✦ ─────────────────── ✦\n"
    "   Hi {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "Great to see you ✨",

    "✦ ─────────────────── ✦\n"
    "   Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "You made it here ✨",

    "✦ ─────────────────── ✦\n"
    "   Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "✦ ─────────────────── ✦\n\n"
    "You're part of us now ✨",
]

CHANNEL_MESSAGES_HI = [
    "✦ ─────────────────── ✦\n"
    "   नमस्ते {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "आपका आना अच्छा लगा ✨",

    "✦ ─────────────────── ✦\n"
    "   नमस्ते {name} 👋\n"
    "   {chat} में स्वागत है\n"
    "✦ ─────────────────── ✦\n\n"
    "आपको देखकर खुशी हुई ✨",

    "✦ ─────────────────── ✦\n"
    "   हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "आपसे मिलकर अच्छा लगा ✨",

    "✦ ─────────────────── ✦\n"
    "   नमस्ते {name} 👋\n"
    "   {chat} में स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "आप यहाँ आ गए ✨",

    "✦ ─────────────────── ✦\n"
    "   हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "✦ ─────────────────── ✦\n\n"
    "अब आप हमारे परिवार का हिस्सा हैं ✨",
]


def send_welcome_message(chat_id, user_name, chat_title, is_channel=False):
    """
    Random English या Hindi message चुनकर भेजता है।
    साथ में YouTube subscribe line भी जोड़ता है।
    """
    # English या Hindi — random pick
    use_hindi = random.choice([True, False])

    if is_channel:
        templates = CHANNEL_MESSAGES_HI if use_hindi else CHANNEL_MESSAGES_EN
    else:
        templates = GROUP_MESSAGES_HI if use_hindi else GROUP_MESSAGES_EN

    template = random.choice(templates)
    welcome_text = template.format(name=user_name, chat=chat_title)

    # Welcome + Subscribe line जोड़ो
    full_text = f"{welcome_text}\n\n{SUBSCRIBE_LINE}"

    payload = {
        "chat_id": chat_id,
        "text": full_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,   # thumbnail नहीं दिखेगा
    }
    try:
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload, timeout=5)
    except Exception as err:
        print(f"Error sending message: {err}")


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)

        try:
            update = json.loads(body.decode("utf-8"))
        except Exception:
            self.send_response(400)
            self.end_headers()
            return

        # 1. Group में साधारण join event
        if "message" in update and "new_chat_members" in update["message"]:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            chat_title = msg["chat"].get("title", "the community")

            for member in msg["new_chat_members"]:
                if member.get("is_bot"):
                    continue
                name = member.get("first_name", "Member")
                send_welcome_message(
                    chat_id, name, chat_title, is_channel=False
                )

        # 2. Channel या advanced group join (Chat Member Update)
        elif "chat_member" in update:
            cm = update["chat_member"]
            chat = cm["chat"]
            new_status = cm["new_chat_member"]["status"]
            old_status = cm["old_chat_member"]["status"]
            user = cm["new_chat_member"]["user"]

            if not user.get("is_bot"):
                was_member = old_status in ["member", "administrator", "creator"]
                is_member = new_status == "member"

                if not was_member and is_member:
                    is_chan = chat.get("type") == "channel"
                    send_welcome_message(
                        chat["id"],
                        user.get("first_name", "Member"),
                        chat.get("title", "the community"),
                        is_channel=is_chan,
                    )

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")