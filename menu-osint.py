import requests
import re
import os
import json
import time
from datetime import datetime

def clear_screen():
    os.system("clear")

def pause():
    input("\nPress ENTER to continue...")

# --------------------
# UTIL
# --------------------

def banner():
    print("""
╔══════════════════════════════╗
║        OSINT DASHBOARD       ║
╚══════════════════════════════╝
""")

def menu():
    while True:
        clear_screen()
        banner()

        print("[1] TikTok OSINT")
        print("[2] Instagram OSINT")
        print("[3] Exit")

        op = input("\nChoice: ")

        if op == "1":
            tiktok_osint()

        elif op == "2":
            instagram_osint()

        elif op == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option")
            time.sleep(1)

# --------------------
# TIKTOK OSINT
# --------------------
def tiktok_osint():
    clear_screen()

    print("\033[1;36m")
    os.system('toilet -f future "TikTok"')

    print("""
╔══════════════════════════════╗
║       TIKTOK OSINT TOOL      ║
╚══════════════════════════════╝
""")

    user = input("\nEnter username: ").strip().replace("@", "")

    if not user:
        print("Empty username.")
        pause()
        return

    print("\nSearching profile...")
    time.sleep(1)

    url = f"https://www.tiktok.com/@{user}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
    except:
        print("\nConnection error.")
        pause()
        return

    if r.status_code != 200:
        print("\nUser not found or blocked.")
        pause()
        return

    text = r.text

    def extract(regex):
        match = re.search(regex, text)
        return match.group(1) if match else "Not found"

    def safe_int(v):
        try:
            return int(v)
        except:
            return v

    nickname = extract(r'"nickname":"(.*?)"')
    bio = extract(r'"signature":"(.*?)"').replace("\\n", "\n")

    followers = safe_int(extract(r'"followerCount":(.*?),'))
    following = safe_int(extract(r'"followingCount":(.*?),'))
    likes = safe_int(extract(r'"heartCount":(.*?),'))
    videos = safe_int(extract(r'"videoCount":(.*?),'))
    verified = extract(r'"verified":(true|false)')

    data = {
        "user": user,
        "url": url,
        "nickname": nickname,
        "bio": bio,
        "followers": followers,
        "following": following,
        "likes": likes,
        "videos": videos,
        "verified": verified,
        "timestamp": str(datetime.now())
    }

    print("\n━━━━━━━━━━━━━━━━━━━━━━")
    print("📌 PROFILE FOUND")
    print("━━━━━━━━━━━━━━━━━━━━━━")

    print(f"\nURL: {url}")
    print(f"Nickname: {nickname}")
    print(f"Bio: {bio}")

    if bio and "insta" in bio.lower():
        print("\n📸 Possible Instagram found in bio!")

    print(f"\nFollowers: {followers}")
    print(f"Following: {following}")
    print(f"Likes: {likes}")
    print(f"Videos: {videos}")
    print(f"Verified: {verified}")

    print("\n━━━━━━━━━━━━━━━━━━━━━━")
    print("📦 JSON EXPORT")
    
    input("\nPress ENTER to return to menu...")
    return

def instagram_osint():
    clear_screen()

    print("\033[1;35m")
    os.system('toilet -f future "Instagram"')

    print("""
╔══════════════════════════════╗
║     INSTAGRAM OSINT TOOL     ║
╚══════════════════════════════╝
""")

    user = input("\nEnter username: ").strip().replace("@", "")

    if not user:
        print("Empty username.")
        input("\nPress ENTER to go back...")
        return

    url = f"https://www.instagram.com/{user}/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print("\n🔎 Searching profile...")
    time.sleep(0.5)
    print("📡 Querying Instagram...")
    time.sleep(0.8)

    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("\n❌ Connection error:", e)
        input("\nPress ENTER to go back...")
        return

    html = r.text

    title = re.search(r'<title>(.*?)</title>', html)
    title = title.group(1) if title else "Not found"

    bio = re.search(r'og:description" content="(.*?)"', html)
    bio = bio.group(1) if bio else "Not found"

    if "Sorry, this page isn't available" in html:
        status = "❌ profile does not exist"
    elif "Login" in html and bio == "Not found":
        status = "🚫 blocked or restricted"
    else:
        status = "✅ profile detected"

    data = {
        "user": user,
        "url": url,
        "title": title,
        "bio": bio,
        "status": status,
        "timestamp": str(datetime.now())
    }

    print("\033[1;35m")
    print("\n━━━━━━━━━━━━━━━━━━━━━━")
    print("📌 PROFILE FOUND")
    print("━━━━━━━━━━━━━━━━━━━━━━")

    print("\033[0m")
    print(f"User: {user}")
    print(f"Status: {status}")
    print(f"Title: {title}")
    print(f"Bio: {bio}")

    print("\n\033[1;35m━━━━━━━━━━━━━━━━━━━━━━")
    print("📦 JSON")
    print("━━━━━━━━━━━━━━━━━━━━━━\033[0m")

    print(json.dumps(data, indent=4, ensure_ascii=False))

    with open("instagram_osint.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    input("\nPress ENTER to go back...")

if __name__ == "__main__":
    menu()