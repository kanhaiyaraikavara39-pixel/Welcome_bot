import json
import os
import random
import requests
from http.server import BaseHTTPRequestHandler

# आपका बॉट टोकन यहाँ फिक्स कर दिया गया है
BOT_TOKEN = "8820307548:AAESeTJkFrwJU4oqLOov5n0ydr11XU0pO6o"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ============================================================
# GROUP WELCOME MESSAGES (English + Hindi)
# ============================================================
GROUP_MESSAGES_EN = [
    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "Glad you're here ✨\n"
    "Feel free to chat 💬",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "So happy to have you ✨\n"
    "Jump in and say hi 💬",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hi {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "You made it here ✨\n"
    "Enjoy your stay 🌸",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "Great to see you ✨\n"
    "Be active and enjoy 🚀",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "You're part of us now ✨\n"
    "Let's have fun together 🎉",
]

GROUP_MESSAGES_HI = [
    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     नमस्ते {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आपका आना अच्छा लगा ✨\n"
    "बेझिझक बात करें 💬",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     नमस्ते {name} 👋\n"
    "   {chat} में स्वागत है\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आपसे मिलकर खुशी हुई ✨\n"
    "बातचीत में शामिल हों 💬",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आप यहाँ आ गए ✨\n"
    "खूब मज़ा करें 🌸",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     नमस्ते {name} 👋\n"
    "   {chat} में स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आपको देखकर अच्छा लगा ✨\n"
    "सक्रिय रहें और मज़े करें 🚀",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "अब आप हमारे परिवार का हिस्सा हैं ✨\n"
    "चलो साथ में मज़ा करें 🎉",
]


# ============================================================
# CHANNEL WELCOME MESSAGES (English + Hindi)
# ============================================================
CHANNEL_MESSAGES_EN = [
    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "Glad you're here ✨\n"
    "Thanks for subscribing 💫",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "So happy to have you ✨\n"
    "Stay tuned for updates 🔔",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hi {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "You made it here ✨\n"
    "Thanks for joining 💫",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hello {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "Great to see you ✨\n"
    "Enjoy the content 🚀",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     Hey {name} 👋\n"
    "   Welcome to {chat}\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "You're part of us now ✨\n"
    "More amazing stuff coming 🌟",
]

CHANNEL_MESSAGES_HI = [
    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     नमस्ते {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आपका आना अच्छा लगा ✨\n"
    "जॉइन करने के लिए शुक्रिया 💫",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     नमस्ते {name} 👋\n"
    "   {chat} में स्वागत है\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आपसे मिलकर खुशी हुई ✨\n"
    "नई अपडेट्स के लिए तैयार रहें 🔔",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आप यहाँ आ गए ✨\n"
    "जॉइन करने के लिए धन्यवाद 💫",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     नमस्ते {name} 👋\n"
    "   {chat} में स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "आपको देखकर अच्छा लगा ✨\n"
    "कंटेंट का मज़ा लें 🚀",

    "╭━━━━━━━━━━━━━━━━━━━━╮\n"
    "     हेलो {name} 👋\n"
    "   {chat} में आपका स्वागत\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    "अब आप हमारे परिवार का हिस्सा हैं ✨\n"
    "और मज़ेदार चीज़ें आ रही हैं 🌟",
]


def send_welcome_message(chat_id, user_name, chat_title, is_channel=False):
    """
    Random English या Hindi message चुनकर भेजता है।
    Group और Channel के लिए अलग template use होते हैं।
    """
    # English या Hindi — random pick
    use_hindi = random.choice([True, False])

    if is_channel:
        templates = CHANNEL_MESSAGES_HI if use_hindi else CHANNEL_MESSAGES_EN
    else:
        templates = GROUP_MESSAGES_HI if use_hindi else GROUP_MESSAGES_EN

    template = random.choice(templates)
    text = template.format(name=user_name, chat=chat_title)

    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
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
