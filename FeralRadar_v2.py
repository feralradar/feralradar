# feral_radar_updated.py
import feedparser
import json
import time
import requests

# 텔레그램 정보
TELEGRAM_BOT_TOKEN = "8031064296:AAHBxvIyaBDWsmqbloajGUQz8LUdcn-XPzA"
TELEGRAM_CHAT_ID = "7807708839"

# 키워드 불러오기
with open("trigger_keywords.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)

# RSS 피드 목록 (세계 주요 뉴스)
rss_feeds = [
    "https://news.google.com/rss?hl=en&gl=US&ceid=US:en",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

# 중복 메시지 방지용
sent_messages = set()

# 메시지 전송 함수
def send_telegram_message(message):
    if message in sent_messages:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        sent_messages.add(message)

# 키워드 검사 함수
def keyword_match(text):
    for category in keywords:
        for kw in keywords[category]:
            if kw.lower() in text.lower():
                return True
    return False

# 뉴스 감시 루프
def check_news():
    for rss_url in rss_feeds:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary if 'summary' in entry else ""
            link = entry.link
            content = f"{title}\n{summary}"
            if keyword_match(content):
                send_telegram_message(f"🔔 트리거 감지됨!\n{title}\n{link}")

if __name__ == "__main__":
    while True:
        try:
            check_news()
        except Exception as e:
            print(f"에러 발생: {e}")
        time.sleep(300)  # 5분마다 감시
