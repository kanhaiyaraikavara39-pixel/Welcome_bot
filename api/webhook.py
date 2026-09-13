import json
import os
import requests
from http.server import BaseHTTPRequestHandler

# आपका बॉट टोकन यहाँ फिक्स कर दिया गया है
BOT_TOKEN = "8820307548:AAESeTJkFrwJU4oqLOov5n0ydr11XU0pO6o"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_welcome_message(chat_id, user_name, chat_title, is_channel=False):
    if is_channel:
        text = (
            f"🎉 <b>New Subscriber Alert!</b> 🎉\n\n"
            f"🌟 <b>{user_name}</b> ने <b>{chat_title}</b> जॉइन कर लिया है!\n"
            f"हमारे चैनल में आपका स्वागत है। 🚀"
        )
    else:
        text = (
            f"✨ <b>Welcome to {chat_title}!</b> ✨\n\n"
            f"👋 नमस्ते <b>{user_name}</b>, ग्रुप में आपका स्वागत है! 🔥\n"
            f"📌 ग्रुप में एक्टिव रहें और नियमों का पालन करें।"
        )

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

        # 1. ग्रुप में साधारण जॉइन इवेंट चेक करें
        if "message" in update and "new_chat_members" in update["message"]:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            chat_title = msg["chat"].get("title", "our group")

            for member in msg["new_chat_members"]:
                if member.get("is_bot"):
                    continue
                name = member.get("first_name", "Member")
                send_welcome_message(
                    chat_id, name, chat_title, is_channel=False
                )

        # 2. चैनल या एडवांस्ड ग्रुप जॉइन (Chat Member Update)
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
