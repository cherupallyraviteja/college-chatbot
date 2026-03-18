import requests
import os

META_ACCESS_TOKEN="EAARnz4xjsZAgBQjeZCWwJaNV4gAuvZAPVx9zSZBAqURzgoiPBtBd8VI6gK05Fsb3f9JkndP8RcvFZAH1SkKECXOajM8esZCQ1FYTl7PkUqioyqbq5wMFFY5bK2qKXkwxe2QVZCRCHZC17YtTpi3IAjUbs1LGzxjErY0lgflXmTvQLVOkh7wcaLuvV6lk9BzXsu59PHSJxwBtKbARBFho363aAZATbp8uXFk9y9ZBy1TxsMHsVzj5u2t7Ev8g6Tykv4gw7dE6ZBpOrdZAoN0hOS89K0JqBrZBE4mdpmhnvwWRZAYQZDZD"
META_PHONE_NUMBER_ID=965717463292105
META_VERIFY_TOKEN="college_chatbot_verify"


GRAPH_URL = "https://graph.facebook.com/v22.0"

def send_whatsapp_message(to: str, text: str):
    url = f"{GRAPH_URL}/{META_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }

    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
