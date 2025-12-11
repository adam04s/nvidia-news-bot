import requests
import datetime
import json
import os

# --- ดึง Key ที่ซ่อนไว้ใน GitHub Secrets ---
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

# คำค้นหาข่าว
KEYWORDS = ['Nvidia', 'Jensen Huang', 'AI Chip', 'Data Center']

# --- ฟังก์ชันส่งเข้า Discord ---
def send_discord_notify(title, link, source):
    data = {
        "username": "Nvidia Watcher",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nvidia_logo.svg/1200px-Nvidia_logo.svg.png",
        "embeds": [{
            "title": f"🔥 {title}",
            "description": f"Source: {source}",
            "url": link,
            "color": 7864115,  # สีเขียว Nvidia
            "footer": {"text": f"Update: {datetime.datetime.now().strftime('%H:%M:%S')}"}
        }]
    }
    headers = {'Content-Type': 'application/json'}
    try:
        requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(data), headers=headers)
    except Exception as e:
        print(f"Error sending discord: {e}")

# --- ฟังก์ชันดึงข่าวจาก NewsAPI ---
def check_news():
    if not NEWS_API_KEY or not DISCORD_WEBHOOK_URL:
        print("❌ Error: ไม่พบ API Key หรือ Webhook URL (ตรวจสอบ GitHub Secrets)")
        return

    today = datetime.date.today().isoformat()
    # สร้าง URL สำหรับดึงข่าว
    url = f'https://newsapi.org/v2/everything?q={"+OR+".join(KEYWORDS)}&from={today}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&language=en'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = data.get('articles', [])[:3] # เอาแค่ 3 ข่าวล่าสุด
            if not articles:
                print("ไม่พบข่าวใหม่วันนี้")
            
            for article in articles:
                send_discord_notify(article['title'], article['url'], article['source']['name'])
                print(f"Sent: {article['title']}")
        else:
            print(f"NewsAPI Error: {data}")
            
    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    print("🚀 Starting Bot...")
    check_news()
    print("✅ Finished.")
