import os
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

VIDEO_BOT_TOKEN = os.getenv("VIDEO_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))

# === 影片來源連結 ===
CATEGORY_URLS = [
    "https://xhamster3.com/categories/russian",
    "https://xhamster3.com/channels/only-tarts",
    "https://xhamster3.com/channels/21-naturals",
]

VIDEOS_PER_ROUND = 10

# === NEW: 多樣化的文案模板（已優化為 Telegram 內嵌瀏覽）===
CAPTION_TEMPLATES = [
    {
        "intro": "💦 <b>Watch full video</b>\n{url}",
        "bonus": "⏳ LIMITED TIME BONUS ⏳",
        "cta": "🔥 For TPA Telegram Members Only❗",
        "footer": "🇦🇺 Officially Recommended by TPA\n🚀 Join Now, Win Now"
    },
    {
        "intro": "🔥 <b>Exclusive content</b>\n{url}",
        "bonus": "🎁 MEMBERS EXCLUSIVE OFFER 🎁",
        "cta": "💎 Only for TPA VIP Members",
        "footer": "🇦🇺 Trusted by Australian Players\n⚡ Don't miss out!"
    },
    {
        "intro": "💎 <b>Premium video</b>\n{url}",
        "bonus": "⭐ SPECIAL ACCESS UNLOCKED ⭐",
        "cta": "🎯 TPA Members get instant access",
        "footer": "🇦🇺 Australia's #1 Community\n🎰 Play Now, Win Big"
    },
    {
        "intro": "🌟 <b>Hot drop</b>\n{url}",
        "bonus": "🚨 EXCLUSIVE DROP 🚨",
        "cta": "🔞 Join TPA for more premium content",
        "footer": "🇦🇺 Verified by TPA Authority\n💰 Claim Your Bonus Today"
    },
    {
        "intro": "⚡ <b>New video just dropped</b>\n{url}",
        "bonus": "🎊 MEMBER PERK ALERT 🎊",
        "cta": "💥 TPA Community exclusive access",
        "footer": "🇦🇺 Australia's Most Trusted Platform\n🎁 Limited Time Offer"
    }
]

DIVIDER_STYLES = ["━━━━━━━━━━━━━━━━━"]

# === 抓取影片 ===
def fetch_from_url(url, max_videos=3):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        selectors = [
            "a.thumb-image-container",
            "a.video-thumb__image-container",
            "a.video-thumb",
            "div.thumb a",
            "a.video-item__link",
            "a.thumb__link",
        ]

        videos = []
        for selector in selectors:
            for a in soup.select(selector):
                href = a.get("href")
                if not href:
                    continue
                img_tag = a.find("img")
                video_url = "https://xhamster3.com" + href if href.startswith("/") else href
                thumbnail = None
                if img_tag:
                    thumbnail = img_tag.get("data-src") or img_tag.get("src")
                videos.append({"url": video_url, "thumbnail": thumbnail})
            if len(videos) >= max_videos:
                break

        random.shuffle(videos)
        return videos[:max_videos]

    except Exception as e:
        print(f"⚠️ Error fetching from {url}: {e}")
        return []

def fetch_videos():
    num_sources = random.randint(3, 7)
    selected_sources = random.sample(CATEGORY_URLS, k=min(num_sources, len(CATEGORY_URLS)))

    all_videos = []
    for source in selected_sources:
        vids = fetch_from_url(source, max_videos=2)
        all_videos.extend(vids)
        time.sleep(random.uniform(0.5, 2))

    random.shuffle(all_videos)
    return all_videos[:VIDEOS_PER_ROUND]

# === 生成隨機文案 ===
def generate_caption(video_url):
    template = random.choice(CAPTION_TEMPLATES)
    divider = random.choice(DIVIDER_STYLES)

    return (
        f"{template['intro'].format(url=video_url)}\n\n"
        f"{template['bonus']}\n"
        f"{template['cta']}\n\n"
        f"{divider}\n"
        f"{template['footer']}"
    )

# === Telegram 發送函式（已加入內嵌瀏覽設定）===
def send_photo(bot_token, chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(url, data=data)
    return r.status_code == 200

def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(url, data=data)
    return r.status_code == 200

# === 主發送流程 ===
def send_videos():
    print(f"\n🚀 Sending videos at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    videos = fetch_videos()

    sent_count = 0
    for v in videos:
        caption = generate_caption(v['url'])
        success = send_photo(VIDEO_BOT_TOKEN, CHANNEL_ID, v["thumbnail"], caption) if v["thumbnail"] else send_message(VIDEO_BOT_TOKEN, CHANNEL_ID, caption)
        if success:
            sent_count += 1
        time.sleep(random.uniform(2, 5))

    print(f"✅ Successfully sent {sent_count}/{len(videos)} videos.\n")

# === Main loop ===
if __name__ == "__main__":
    print("🤖 Auto Video Poster Bot started")
    while True:
        try:
            send_videos()
            jitter = random.randint(-30, 30)
            actual_interval = INTERVAL_HOURS * 3600 + (jitter * 60)
            time.sleep(actual_interval)
        except Exception as e:
            print(f"❗ Unexpected error: {e}")
            time.sleep(60)
