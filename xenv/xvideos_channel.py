import requests
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os
import subprocess

# === Telegram 設定 ===
BOT_TOKEN = os.getenv("VIDEO_BOT_TOKEN", "7961665345:AAFtGJsNNqNRRntKXQCFxuCLwqGzln6hbhM")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@hottxvideos18plus")
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))  # 每 6 小時發送一次

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


# === 抓取單個頁面影片 ===
def fetch_from_url(url, max_videos=3):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        )
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        # 打印頁面標題以檢查是否被 Cloudflare 攔截
        title_tag = soup.find("title")
        print(f"📄 Page title from {url}: {title_tag.text.strip() if title_tag else 'No title found'}")

        videos = []
        # ✅ 加入多種 CSS Selector 匹配
        for a in soup.select(
            "a.thumb-image-container, a.video-thumb__image-container, a.video-thumb, div.thumb a, div.video-thumb__link"
        ):
            href = a.get("href")
            img_tag = a.find("img")
            if not href:
                continue

            video_url = "https://xhamster3.com" + href if href.startswith("/") else href
            thumbnail = img_tag.get("data-src") or img_tag.get("src") if img_tag else None
            videos.append({"url": video_url, "thumbnail": thumbnail})

        print(f"🎞 Found {len(videos)} videos from {url}")
        random.shuffle(videos)
        return videos[:max_videos]

    except Exception as e:
        print(f"⚠️ Error fetching from {url}: {e}")
        return []


# === 抓取多個來源影片 ===
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
    print(f"📦 Total gathered before filtering: {len(all_videos)} videos")
    return all_videos[:VIDEOS_PER_ROUND]


# === Telegram 發送函式 ===
def send_photo(chat_id, photo_url, caption, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": parse_mode}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return True
    else:
        print(f"⚠️ sendPhoto failed: {response.text}")
        return False


def send_message(chat_id, text, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return True
    else:
        print(f"⚠️ sendMessage failed: {response.text}")
        return False


# === 發送到 Telegram 頻道 ===
def send_to_channel():
    print(f"\n🚀 Sending videos at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        videos = fetch_videos()
        print(f"✅ Total collected: {len(videos)} videos\n")

        if not videos:
            print("⚠️ No videos found — check page structure or network.")
            return False

        success_count = 0
        for v in videos:
            caption = (
                f"💦 <a href=\"{v['url']}\">Click here to unlock full videos: [Link...]</a>\n"
                f"🔞 <a href=\"https://tinyurl.com/3zh5zvrf\">Tap here for more videos: [Link...]</a>"
            )

            if v["thumbnail"]:
                ok = send_photo(CHANNEL_ID, v["thumbnail"], caption)
            else:
                ok = send_message(CHANNEL_ID, caption)

            if ok:
                success_count += 1
            time.sleep(3)

        print(f"✅ Sent {success_count}/{len(videos)} videos successfully.")
        return success_count == len(videos)

    except Exception as e:
        print(f"❗ Error sending videos: {e}")
        return False


# === 主程序循環 ===
if __name__ == "__main__":
    print("✅ Auto Multi-Source Video Poster Started!")

    while True:
        all_ok = send_to_channel()

        if all_ok:
            print("🎯 All videos sent successfully. Now starting message forward script...")

            script_path = os.path.join(os.path.dirname(__file__), "..", "forward_bot", "forward_group_to_channel.py")
            script_path = os.path.abspath(script_path)

            print(f"📂 Running forward script at: {script_path}")
            subprocess.run(["python3", script_path])
        else:
            print("⚠️ Some videos failed, skipping message forwarding this round！")

        # ✅ 加入循环检测输出
        next_run = datetime.now() + timedelta(hours=INTERVAL_HOURS)
        print(f"🔁 Loop check — Next run scheduled at {next_run.strftime('%Y-%m-%d %H:%M:%S')} "
              f"(every {INTERVAL_HOURS} hours)\n")

        time.sleep(INTERVAL_HOURS * 3600)
