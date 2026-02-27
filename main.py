import asyncio
import os
from threading import Thread
from flask import Flask
from pyrogram import Client, filters, idle, enums
import google.generativeai as genai
from datetime import datetime
import pytz

# --- [ Port Binding for Render ] ---
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Bot is Running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- [ Bot Configuration ] ---
API_KEY = os.environ.get("GEMINI_API_KEY") 
SESSION_STRING = os.environ.get("SESSION_STRING")
API_ID = int(os.environ.get("API_ID", "32642557"))
API_HASH = os.environ.get("API_HASH", "2790877135ea0991a392fe6a0d285c27")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Client(
    "blitz_twin",
    session_string=SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH
)

last_message_time = {}

@app.on_message(filters.private & ~filters.me)
async def blitz_ai_handler(client, message):
    if not message.text: return
    chat_id = message.chat.id
    arrival_time = datetime.now()
    last_message_time[chat_id] = arrival_time
    
    # ၁၅ စက္ကန့် စောင့်မယ်
    await asyncio.sleep(15) 

    if last_message_time.get(chat_id) == arrival_time:
        await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
        tz = pytz.timezone('Asia/Yangon')
        h = datetime.now(tz).hour
        status = "အလုပ်လုပ်နေတယ်" if 6 <= h < 18 else "နားနေတယ်"
        
        prompt = f"မင်းက Blitz ပါ။ User က '{message.text}' လို့ပြောတယ်။ လိုရင်းပဲ မြန်မာလိုဖြေပါ။"
        try:
            response = model.generate_content(prompt)
            await message.reply_text(response.text)
        except: pass

async def start_bot():
    print("🛰️ Bot Starting...")
    async with app:
        print("✅ Bot is Online!")
        await idle()

if __name__ == "__main__":
    # Flask ကို Thread တစ်ခုနဲ့ Run မယ် (Render Port အတွက်)
    Thread(target=run_flask).start()
    
    # Bot ကို Run မယ်
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
