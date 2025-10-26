import os
import asyncio
import random
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import subprocess
from dotenv import load_dotenv

# === 载入环境变量 ===
load_dotenv()

BOT_TOKEN = os.getenv("VIDEO_BOT_TOKEN", "7961665345:AAFtGJsNNqNRRntKXQCFxuCLwqGzln6hbhM")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@hottxvideos18plus")
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))

# === 视频来源 ===
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
    "https://xhamster3.com/creators/hot-pearl",
]

VIDEOS_PER_ROUND = 10


# === 抓取单个网页视频 ===
async def fetch_from_url(session, url, max_videos=3):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        )
    }

    try:
        async with session.get(url, headers=headers, timeout=15) as res:
            text = await res.text()
            soup = BeautifulSoup(text, "html.parser")

            videos = []
            for a in soup.select("a.thumb-image-container, a.video-thumb__image-container"):
                href = a.get("href")
                img_tag = a.find("img")
                if not href:
                    continue
                video_url = "https://xhamster3.com" + href if href.startswith("/") else href
                thumbnail = img_tag.get("data-src") or img_tag.get("src") if img_tag else None
                videos.append({"url": video_url, "thumbnail": thumbnail})

            random.shuffle(videos)
            return videos[:max_videos]
    except Exception as e:
        print(f"⚠️ Error fetching from {url}: {e}")
        return []


# === 抓取多个来源 ===
async def fetch_videos():
    selected_sources = random.sample(CATEGORY_URLS, k=5)
    print(f"🌐 Selected sources ({len(selected_sources)}):")
    for s in selected_sources:
        print(f"  - {s}")

    videos = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_from_url(session, src, max_videos=2) for src in selected_sources]
        results = await asyncio.gather(*tasks)
        for r in results:
            videos.extend(r)

    random.shuffle(videos)
    return videos[:VIDEOS_PER_ROUND]


# === Telegram 发送函数 ===
async def send_photo(session, chat_id, photo_url, caption, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": parse_mode}
    async with session.post(url, data=data) as response:
        if response.status == 200:
            return True
        else:
            print(f"⚠️ sendPhoto failed: {response.status}")
            return False


async def send_message(session, chat_id, text, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    async with session.post(url, data=data) as response:
        if response.status == 200:
            return True
        else:
            print(f"⚠️ sendMessage failed: {response.status}")
            return False


# === 发送视频到频道 ===
async def send_to_channel():
    print(f"\n🚀 Sending videos at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        videos = await fetch_videos()
        print(f"✅ Total collected: {len(videos)} videos\n")

        if not videos:
            print("⚠️ No videos found — check page structure or network.")
            return False

        success_count = 0
        async with aiohttp.ClientSession() as session:
            for v in videos:
                caption = (
                    f"💦 <a href=\"{v['url']}\">Click here to unlock full videos 🔗</a>\n"
                    f"🔞 <a href=\"https://tinyurl.com/3zh5zvrf\">Tap here for more hot videos 🔥</a>"
                )
                if v["thumbnail"]:
                    ok = await send_photo(session, CHANNEL_ID, v["thumbnail"], caption)
                else:
                    ok = await send_message(session, CHANNEL_ID, caption)
                if ok:
                    success_count += 1
                await asyncio.sleep(3)

        print(f"✅ Sent {success_count}/{len(videos)} videos successfully.")
        return success_count == len(videos)
    except Exception as e:
        print(f"❗ Error sending videos: {e}")
        return False


# === 主循环 ===
async def main_loop():
    print("✅ Auto Multi-Source Video Poster Started (async mode, every 6 hours).")

    while True:
        all_ok = await send_to_channel()

        if all_ok:
            print("🎯 All videos sent successfully. Running forward script...")
            try:
                script_path = os.path.join(os.path.dirname(__file__), "..", "forward_bot", "forward_group_to_channel.py")
                script_path = os.path.abspath(script_path)
                subprocess.run(["python3", script_path], check=True)
            except Exception as e:
                print(f"⚠️ Forward script failed: {e}")
        else:
            print("⚠️ Some videos failed, skipping forwarding this round.")

        print(f"🕒 Waiting {INTERVAL_HOURS} hours before next video batch...\n")
        await asyncio.sleep(INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    asyncio.run(main_loop())
