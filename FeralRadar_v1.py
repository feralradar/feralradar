import requests
import feedparser
import time

# --- 설정값 ---
bot_token = '8031064296:AAHBxvIyaBDWsmqbloajGUQz8LUdcn-XPzA'
chat_id = 7807708839

# --- 감시 키워드 (글로벌 기준) ---
keywords = ["xrp", "crypto regulation", "SEC", "halving", "ethereum", "solana", "kaia"]

# --- 구글 글로벌 뉴스 (영어권) ---
rss_url = "https://news.google.com/rss/search?q=bitcoin+OR+cryptocurrency&hl=en&gl=US&ceid=US:en"

# --- 이미 본 뉴스 저장용 세트 ---
seen_titles = set()

# --- 루프 시작 ---
print("Feral Radar 트리거 감시 시작... (Ctrl+C로 중단)")

while True:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        title = entry.title
        link = entry.link

        # 중복 확인
        if title in seen_titles:
            continue

        # 키워드 감지
        for keyword in keywords:
            if keyword.lower() in title.lower():
                message = f"🚨 트리거 감지 (글로벌)\n\n📰 {title}\n🔗 {link}\n🔑 키워드: {keyword}"
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {'chat_id': chat_id, 'text': message}
                requests.post(url, data=payload)
                print(f"[ALERT] {title}")
                break

        seen_titles.add(title)

    # 60초 대기 후 반복
    time.sleep(60)
