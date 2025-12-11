แก้ตรงไหน
"import requests
import datetime
import json
import os  # <--- เพิ่มตัวนี้ เพื่อดึง Key จาก GitHub Secret

# --- ดึง Key จาก Environment Variable แทนการใส่ตรงๆ ---
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
KEYWORDS = ['Nvidia', 'Jensen Huang', 'AI Chip', 'Data Center']

# --- ฟังก์ชันส่งเข้า Discord (เหมือนเดิม) ---
def send_discord_notify(title, link, source):
    data = {
        "username": "Nvidia Watcher",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nvidia_logo.svg/1200px-Nvidia_logo.svg.png",
        "embeds": [{
            "title": f"🔥 {title}",
            "description": f"Source: {source}",
            "url": link,
            "color": 7864115,
            "footer": {"text": f"Update: {datetime.datetime.now().strftime('%H:%M:%S')}"}
        }]
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(data), headers=headers)

# --- ฟังก์ชันดึงข่าว (เหมือนเดิม) ---
def check_news():
    if not NEWS_API_KEY or not DISCORD_WEBHOOK_URL:
        print("❌ Error: ไม่พบ API Key หรือ Webhook URL")
        return

    today = datetime.date.today().isoformat()
    url = f'https://newsapi.org/v2/everything?q={"+OR+".join(KEYWORDS)}&from={today}&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
    
    response = requests.get(url)
    data = response.json()
    
    if data.get('status') == 'ok':
        articles = data.get('articles', [])[:3]
        if not articles:
            print("ไม่พบข่าวใหม่")
        for article in articles:
            send_discord_notify(article['title'], article['url'], article['source']['name'])
            print(f"Sent: {article['title']}")
    else:
        print("Error:", data)

if __name__ == "__main__":

    check_news()
"
