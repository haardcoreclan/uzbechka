from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

TOKEN = os.environ.get("BOT_TOKEN")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))

        if "message" in update and "text" in update["message"]:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            message_id = msg["message_id"]
            text = msg["text"]

            if not msg.get("from", {}).get("is_bot", False):
                self.send_reply(chat_id, text, message_id)

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
