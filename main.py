import asyncio
import os
import socket
import google.generativeai as genai
from pyrogram import Client, filters, idle, enums
from datetime import datetime
import pytz

# --- [ Configuration ] ---
# Koyeb/Render ရဲ့ Environment Variables ထဲမှာ ဒီအမည်တွေအတိုင်း ထည့်ပေးပါ
API_KEY = os.environ.get("GEMINI_API_KEY") 
SESSION_STRING = os.environ.get("SESSION_STRING")
API_ID = int(os.environ.get("API_ID", 32642557))
API_HASH = os.environ.get("API_HASH", "2790877135ea0991a392fe6a0d285c27")

# Gemini Setup
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram Client Setup
app = Client(
    "blitz_twin",
    session_string=SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH
)

# Target Usernames
TARGET_FRIEND = "Goozxak12"
GIRLFRIEND = "thwe014"

last_message_time = {}

# Cloud Hosting အိပ်မသွားအောင် Port တစ်ခု ဖွင့်ထားခြင်း
def start_port_listener():
    try:
        port = int(os.environ.get("PORT", 8080))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"⚓ Port {port} is active for Cloud Hosting.")
    except: pass

@app.on_message(filters.private & ~filters.me)
async def blitz_ai_handler(client, message):
    if not message.text: return
    
    chat_id = message.chat.id
    user = message.from_user
    text = message.text

    # ၂ မိနစ် စောင့်ဆိုင်းခြင်း (လူကိုယ်တိုင် စာရိုက်သလို ခံစားရစေရန်)
    arrival_time = datetime.now()
    last_message_time[chat_id] = arrival_time
    await asyncio.sleep(120) 

    # နောက်ထပ် စာဝင်မလာတော့မှသာ AI က ပြန်ဖြေမည်
    if last_message_time.get(chat_id) == arrival_time:
        # Typing အရင်ပြမည်
        await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
        
        # Myanmar Time Logic
        tz = pytz.timezone('Asia/Yangon')
        now_mm = datetime.now(tz)
        h = now_mm.hour

        if 6 <= h < 18:
            status = "ကုမ္ပဏီမှာ အလုပ်လုပ်နေတာမို့ လိုရင်းပဲ ပြောမယ်။"
        elif 18 <= h < 22:
            status = "အခု ဂိမ်း Stream နေတာ။ ပွဲကြားအားတုန်း ခဏပြန်ဖြေတာ။"
        else:
            status = "အခု အနားယူရင်း ဖုန်းကြည့်နေတာ။"

        # Persona Prompt
        identity = f"မင်းက Blitz (တိုးဝေအောင်) ပါ။ ရန်ကုန်သား၊ မြဝတီမှာနေတယ်။ စရိုက်က ဟာသနှောတယ်၊ လိုရင်းပဲပြောတယ်။ လက်ရှိအခြေအနေ: {status}"

        if user.username == TARGET_FRIEND:
            prompt = f"{identity} အခု စကားပြောနေတာက သူငယ်ချင်း 'ယဖ'။ သူ့ကို 'ငါ/မင်း' သုံး၊ ဆဲရင်ပြန်ဆဲ၊ အရင်းနှီးဆုံးပုံစံနဲ့ ဖြေပါ။ User: {text}"
        elif user.username == GIRLFRIEND:
            prompt = f"{identity} အခုပြောနေတာက မိန်းမ (Baby) @thwe014။ 'ကိုကို' လို့သုံး၊ သူ့ကို 'Baby' လို့ခေါ်ပါ။ User: {text}"
        else:
            prompt = f"{identity} တခြားလူတွေကို 'အစ်ကို/အစ်မ' သုံးပြီး ယဉ်ကျေးစွာ လိုရင်းပဲ ဖြေပါ။ User: {text}"

        try:
            response = model.generate_content(prompt)
            await message.reply_text(response.text)
        except Exception as e:
            print(f"AI Error: {e}")

async def main():
    start_port_listener()
    print("🛰️ BLITZ DIGITAL TWIN IS STARTING...")
    await app.start()
    print("✅ ONLINE AND READY TO REPLY!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
