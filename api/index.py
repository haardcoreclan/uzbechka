from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

TOKEN = os.environ.get("BOT_TOKEN")

# Временная память для обучения фраз
MEMORY = {
    "чë": "через плечо",
    "чё": "через плечо",
}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))

        # 1. Проверяем, не отредактировал ли кто-то сообщение
        if "edited_message" in update:
            msg = update["edited_message"]
            if "text" in msg and not msg.get("from", {}).get("is_bot", False):
                chat_id = msg["chat"]["id"]
                message_id = msg["message_id"]
                text = "🔆 Nega yozgan xabarni o'zgartirdingiz bilib qoldimaa 🔆 Mendan qolcholmaysiz."
                self.send_reply(chat_id, text, message_id)

        # 2. Проверяем обычные сообщения
        elif "message" in update and "text" in update["message"]:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            message_id = msg["message_id"]
            text = msg["text"]
            text_lower = text.strip().lower()
            
            if not msg.get("from", {}).get("is_bot", False):
                
                # А. Пасхалка на имя "Абзал"
                if "абзал" in text_lower:
                    self.send_reply(chat_id, "Мой папочка", message_id)

                # Б. Обучение: если это ответ (reply) на чье-то сообщение
                elif "reply_to_message" in msg and "text" in msg["reply_to_message"]:
                    original_text = msg["reply_to_message"]["text"].strip()
                    reply_text = text.strip()
                    # Запоминаем связку
                    MEMORY[original_text.lower()] = reply_text
                    
                    # Колоритный ответ с восточным вайбом и смайликами ✨
                    collab_text = (
                        f"Voy, qoyil! 🌸 Yozib qo‘ydim, jonim: "
                        f"endi «{original_text}» desalar — «{reply_text}» deb javob beraman! 💅✨"
                    )
                    self.send_reply(chat_id, collab_text, message_id)

                # В. Проверка: есть ли триггер в нашей памяти
                elif text_lower in MEMORY:
                    answer = MEMORY[text_lower]
                    self.send_reply(chat_id, answer, message_id)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def send_reply(self, chat_id, text, reply_to_id):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_to_message_id": reply_to_id
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Error: {e}")
