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
    "https://xhamster3.com/channels/naughty-america",
    "https://xhamster3.com/creators/msbreewc",
    "https://xhamster3.com/creators/comatozze",
    "https://xhamster3.com/channels/raptor-llc",
    "https://xhamster3.com/channels/school-girls-hd-channel",
    "https://xhamster3.com/categories/russian",
    "https://xhamster3.com/categories/japanese",
    "https://xhamster3.com/channels/av-stockings",
    "https://xhamster3.com/channels/jav-hd",
    "https://xhamster3.com/channels/jav-hd/best",
    "https://xhamster3.com/creators/pornforce",
    "https://xhamster3.com/channels/av-tits",
    "https://xhamster3.com/creators/elina-lizz",
    "https://xhamster3.com/creators/bootyfrutti",
    "https://xhamster3.com/creators/hot-pearl"
]

VIDEOS_PER_ROUND = 10

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
    selected_sources = random.sample(CATEGORY_URLS, k=5)
    print(f"🌐 Selected sources ({len(selected_sources)}):")
    for s in selected_sources:
        print(f"  - {s}")

    all_videos = []
    for source in selected_sources:
        vids = fetch_from_url(source, max_videos=2)
        all_videos.extend(vids)
        time.sleep(1)
    random.shuffle(all_videos)
    return all_videos[:VIDEOS_PER_ROUND]

# === Telegram 發送函式 ===
def send_photo(bot_token, chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": "HTML"}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f"⚠️ sendPhoto failed: {r.text}")

# === 主發送流程 ===
def send_videos():
    print(f"\n🚀 Sending videos at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    videos = fetch_videos()

    if not videos:
        print("⚠️ No videos found.")
        return

    for v in videos:
        caption = (
            f"💦 <a href=\"{v['url']}\">Watch full video now</a> \n\n"
            f"💎 LIMITED TIME BONUS 💎 \n"
            f"🔥 For <a href=\"https://telegram.me/tpaaustralia\">TPA Telegram Members</a> Only! \n\n"
            f"▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
            f"|🇦🇺 Officially Recommended by TPA 🇦🇺| \n"
            f"🚀 Join Now, Win Now 🚀"
        )

        if v["thumbnail"]:
            send_photo(VIDEO_BOT_TOKEN, CHANNEL_ID, v["thumbnail"], caption)
        else:
            url = f"https://api.telegram.org/bot{VIDEO_BOT_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHANNEL_ID, "text": caption, "parse_mode": "HTML"})
        time.sleep(3)

    print(f"✅ Sent {len(videos)} videos successfully.\n")

# === Main loop ===
if __name__ == "__main__":
    print("🤖 Auto Video Poster Bot started")
    while True:
        try:
            send_videos()
            print(f"🕒 Waiting {INTERVAL_HOURS} hours before next round...\n")
            time.sleep(INTERVAL_HOURS * 3600)
        except Exception as e:
            print(f"❗ Unexpected error: {e}")
            print("🔁 Restarting in 1 minute...")
            time.sleep(60)
