from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('XZd38bxNXLI+M0YdskOL+oRAMMw7f4JU++etxlOXOHOZJ8/Ew9uLDgwmpLU5jlYhv2Qt6m0kTkDmgpOmLiJ7NBkTwHW6QdO7oeeMmJB6PIQnXAcmZQAe3FGtdurt/cKYIot9hwIru87oA69hbA4MkAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4434a122644c1185bef91e14d43da676')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)