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

# === NEW: 多樣化的文案模板 ===
CAPTION_TEMPLATES = [
    {
        "intro": "💦 <a href=\"{url}\">Watch full video now</a>",
        "bonus": "⏳ LIMITED TIME BONUS ⏳",
        "cta": "🔥 For <a href=\"https://telegram.me/tpaaustralia\">TPA Telegram Members</a> Only❗",
        "footer": "🇦🇺 Officially Recommended by TPA\n🚀 Join Now, Win Now"
    },
    {
        "intro": "🔥 <a href=\"{url}\">Click to watch exclusive content</a>",
        "bonus": "🎁 MEMBERS EXCLUSIVE OFFER 🎁",
        "cta": "💎 Only for <a href=\"https://telegram.me/tpaaustralia\">TPA VIP Members</a>",
        "footer": "🇦🇺 Trusted by Australian Players\n⚡ Don't miss out!"
    },
    {
        "intro": "💎 <a href=\"{url}\">Premium video available now</a>",
        "bonus": "⭐ SPECIAL ACCESS UNLOCKED ⭐",
        "cta": "🎯 <a href=\"https://telegram.me/tpaaustralia\">TPA Members</a> get instant access",
        "footer": "🇦🇺 Australia's #1 Community\n🎰 Play Now, Win Big"
    },
    {
        "intro": "🌟 <a href=\"{url}\">Stream this hot content now</a>",
        "bonus": "🚨 EXCLUSIVE DROP 🚨",
        "cta": "🔞 <a href=\"https://telegram.me/tpaaustralia\">Join TPA</a> for more premium content",
        "footer": "🇦🇺 Verified by TPA Authority\n💰 Claim Your Bonus Today"
    },
    {
        "intro": "⚡ <a href=\"{url}\">New video just dropped</a>",
        "bonus": "🎊 MEMBER PERK ALERT 🎊",
        "cta": "💥 <a href=\"https://telegram.me/tpaaustralia\">TPA Community</a> exclusive access",
        "footer": "🇦🇺 Australia's Most Trusted Platform\n🎁 Limited Time Offer"
    }
]

DIVIDER_STYLES = [
    "━━━━━━━━━━━━━━━━━",
]

# === 抓取影片 ===
def fetch_from_url(url, max_videos=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
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
                    thumbnail = (
                        img_tag.get("data-src")
                        or img_tag.get("data-thumb")
                        or img_tag.get("src")
                    )
                videos.append({"url": video_url, "thumbnail": thumbnail})
            if len(videos) >= max_videos:
                break

        random.shuffle(videos)
        return videos[:max_videos]

    except Exception as e:
        print(f"⚠️ Error fetching from {url}: {e}")
        return []

def fetch_videos():
    # NEW: 隨機選擇 3-7 個來源，增加變化性
    num_sources = random.randint(3, 7)
    selected_sources = random.sample(CATEGORY_URLS, k=min(num_sources, len(CATEGORY_URLS)))
    
    print(f"🌐 Selected {num_sources} sources:")
    for s in selected_sources:
        print(f"  - {s}")

    all_videos = []
    for source in selected_sources:
        vids = fetch_from_url(source, max_videos=2)
        all_videos.extend(vids)
        time.sleep(random.uniform(0.5, 2))  # NEW: 隨機延遲
        
    random.shuffle(all_videos)
    return all_videos[:VIDEOS_PER_ROUND]

# === NEW: 生成隨機文案 ===
def generate_caption(video_url):
    template = random.choice(CAPTION_TEMPLATES)
    divider = random.choice(DIVIDER_STYLES)
    
    caption = (
        f"{template['intro'].format(url=video_url)} \n\n"
        f"{template['bonus']} \n"
        f"{template['cta']} \n\n"
        f"{divider}\n"
        f"{template['footer']}"
    )
    
    return caption

# === Telegram 發送函式 ===
def send_photo(bot_token, chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": "HTML"}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f"⚠️ sendPhoto failed: {r.text}")
    return r.status_code == 200

def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, data=data)
    return r.status_code == 200

# === 主發送流程 ===
def send_videos():
    print(f"\n🚀 Sending videos at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    videos = fetch_videos()

    if not videos:
        print("⚠️ No videos found.")
        return

    sent_count = 0
    for v in videos:
        caption = generate_caption(v['url'])  # NEW: 使用隨機文案
        
        success = False
        if v["thumbnail"]:
            success = send_photo(VIDEO_BOT_TOKEN, CHANNEL_ID, v["thumbnail"], caption)
        else:
            success = send_message(VIDEO_BOT_TOKEN, CHANNEL_ID, caption)
        
        if success:
            sent_count += 1
        
        # NEW: 隨機發送間隔 (2-5秒)，更自然
        time.sleep(random.uniform(2, 5))

    print(f"✅ Successfully sent {sent_count}/{len(videos)} videos.\n")

# === Main loop ===
if __name__ == "__main__":
    print("🤖 Auto Video Poster Bot started")
    while True:
        try:
            send_videos()
            
            # NEW: 隨機調整間隔時間 (±30分鐘)，避免固定發送模式
            jitter = random.randint(-30, 30)
            actual_interval = INTERVAL_HOURS * 3600 + (jitter * 60)
            hours = actual_interval / 3600
            
            print(f"🕒 Waiting {hours:.1f} hours before next round...\n")
            time.sleep(actual_interval)
            
        except Exception as e:
            print(f"❗ Unexpected error: {e}")
            print("🔁 Restarting in 1 minute...")
            time.sleep(60)