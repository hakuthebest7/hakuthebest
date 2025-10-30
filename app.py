from flask import Flask, render_template, request, jsonify
import requests
import datetime

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def local_reply(user_message):
    """Câu trả lời sẵn (offline)"""
    you = user_message.lower().strip()
    if you == "xin chào":
        return "AI: xin chào bạn!"
    elif you == "bây giờ là mấy giờ":
        now = datetime.datetime.now()
        return f"AI: bây giờ là {now.hour} giờ {now.minute} phút."
    elif you == "hôm nay là ngày bao nhiêu":
        today = datetime.date.today()
        return f"AI: hôm nay là ngày {today.day}/{today.month}/{today.year}."
    elif you == "tạm biệt":
        return "AI: tạm biệt bạn!"
    return None  # nếu không khớp thì gọi API

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        # Nếu trùng với câu trả lời sẵn thì trả luôn
        reply = local_reply(user_message)
        if reply:
            return jsonify({"reply": reply})

        # Nếu không trùng -> gọi Groq API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.7
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return jsonify({"reply": f"⚠️ Lỗi API ({response.status_code}): {response.text}"})

        ai_reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"reply": f"❌ Lỗi hệ thống: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
