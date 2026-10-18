import json
import os
import random
import threading
import time
import requests
from http.server import BaseHTTPRequestHandler

# बॉट टोकन: पहले Vercel के Environment Variable "BOT_TOKEN" से लेता है,
# वो न मिले तो नीचे वाला पुराना टोकन इस्तेमाल होता है (बाद में इसे हटा देना बेहतर है)
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8820307548:AAESeTJkFrwJU4oqLOov5n0ydr11XU0pO6o"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ---------------- सेटिंग्स ----------------
DELETE_AFTER_SECONDS = 5      # वेलकम मैसेज कितने सेकंड दिखे, फिर ऑटो डिलीट
DELETE_JOIN_NOTICE = True     # ग्रुप का "X joined the group" वाला सिस्टम मैसेज भी हटाओ

# YouTube Channel Link
YOUTUBE_LINK = "https://youtube.com/@s.kanhaiya.7m"

# Subscribe line (Roman Hindi — same for all)
SUBSCRIBE_LINE = f"Kya tumne channel subscribe kiya?\n👉 {YOUTUBE_LINK}"


# ============================================================
# WELCOME MESSAGES — (greeting, welcome line, closing)
# टेक्स्ट पहले जैसा ही है; ग्रुप और चैनल दोनों के लिए यही लिस्ट चलती है
# ============================================================
MESSAGES_EN = [
    ("Hello {name} 👋", "Welcome to {chat}", "Glad you're here ✨"),
    ("Hey {name} 👋",   "Welcome to {chat}", "So happy to have you ✨"),
    ("Hi {name} 👋",    "Welcome to {chat}", "Great to see you ✨"),
    ("Hello {name} 👋", "Welcome to {chat}", "You made it here ✨"),
    ("Hey {name} 👋",   "Welcome to {chat}", "You're part of us now ✨"),
]

MESSAGES_HI = [
    ("नमस्ते {name} 👋", "{chat} में आपका स्वागत", "आपका आना अच्छा लगा ✨"),
    ("नमस्ते {name} 👋", "{chat} में स्वागत है",   "आपको देखकर खुशी हुई ✨"),
    ("हेलो {name} 👋",   "{chat} में आपका स्वागत", "आपसे मिलकर अच्छा लगा ✨"),
    ("नमस्ते {name} 👋", "{chat} में स्वागत",      "आप यहाँ आ गए ✨"),
    ("हेलो {name} 👋",   "{chat} में आपका स्वागत", "अब आप हमारे परिवार का हिस्सा हैं ✨"),
]


def build_text(user_name, chat_title):
    """Random English/Hindi चुनकर छोटा (5 लाइन) मैसेज बनाता है।"""
    greet, welcome, closing = random.choice(
        random.choice([MESSAGES_HI, MESSAGES_EN])
    )
    # एक छोटी सजावट, बाकी लाइनें सीधी — कोई खाली लाइन नहीं
    return (
        f"✦ {greet.format(name=user_name)} ✦\n"
        f"{welcome.format(chat=chat_title)}\n"
        f"{closing}\n"
        f"{SUBSCRIBE_LINE}"
    )


def delete_message(chat_id, message_id):
    try:
        requests.post(
            f"{TELEGRAM_API_URL}/deleteMessage",
            json={"chat_id": chat_id, "message_id": message_id},
            timeout=5,
        )
    except Exception as err:
        print(f"Error deleting message: {err}")


def send_welcome_message(chat_id, user_name, chat_title, is_channel=False):
    """
    वेलकम मैसेज भेजता है, DELETE_AFTER_SECONDS रुकता है, फिर उसे डिलीट कर देता है।
    (मैसेज पिन नहीं किया जाता।)
    """
    payload = {
        "chat_id": chat_id,
        "text": build_text(user_name, chat_title),
        "parse_mode": "HTML",
        "disable_web_page_preview": True,   # thumbnail नहीं दिखेगा
        "disable_notification": True,       # आवाज़/नोटिफिकेशन नहीं
    }
    try:
        r = requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload, timeout=5)
        data = r.json()
    except Exception as err:
        print(f"Error sending message: {err}")
        return

    if not data.get("ok"):
        print(f"sendMessage failed: {data}")
        return

    message_id = data["result"]["message_id"]
    time.sleep(DELETE_AFTER_SECONDS)
    delete_message(chat_id, message_id)


def run_parallel(jobs):
    """कई यूज़र एक साथ जुड़ें तो सबका टाइमर साथ-साथ चले (इंतज़ार जुड़े नहीं)।"""
    threads = [threading.Thread(target=fn, args=args) for fn, args in jobs]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


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

        jobs = []

        # 1. Group में साधारण join event
        if "message" in update and "new_chat_members" in update["message"]:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            chat_title = msg["chat"].get("title", "the community")

            # "X joined the group" सिस्टम मैसेज हटाओ (बॉट को Delete messages अधिकार चाहिए)
            if DELETE_JOIN_NOTICE and "message_id" in msg:
                jobs.append((delete_message, (chat_id, msg["message_id"])))

            for member in msg["new_chat_members"]:
                if member.get("is_bot"):
                    continue
                name = member.get("first_name", "Member")
                jobs.append((send_welcome_message, (chat_id, name, chat_title, False)))

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
                    jobs.append((
                        send_welcome_message,
                        (
                            chat["id"],
                            user.get("first_name", "Member"),
                            chat.get("title", "the community"),
                            is_chan,
                        ),
                    ))

        run_parallel(jobs)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
