import requests
# import pywhatkit as kit
import time
# import pyautogui
from news_agent.core.config import TELEGRAM_TOKEN, CHAT_ID, PHONE_NO

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    return response.status_code

# def send_whatsapp(msg):
#     # send instantly (must keep WhatsApp Web logged in)
#     print("📲 Sending WhatsApp...")
#     try:
#         kit.sendwhatmsg_instantly(
#             phone_no=PHONE_NO,
#             message=msg,
#             wait_time=15,
#             tab_close=True
#         )

#         time.sleep(10)   #avoid blocking

#     except Exception as e:
#         print(f"Error: {e}")
#     print("WhatsApp Sent")

# def send_whatsapp_group(message):
#     try:
#         print("📲 Opening WhatsApp Web...")

#         # open any chat first
#         kit.sendwhatmsg_instantly(
#             phone_no="+91XXXXXXXXX",  # your own number
#             message="temp",
#             wait_time=35,
#             tab_close=False
#         )

#         time.sleep(10)

#         # search group manually via typing
#         grp_name="Mazza the group"
#         pyautogui.write("grp_name")
#         pyautogui.press("enter")

#         time.sleep(2)

#         pyautogui.write(message)
#         pyautogui.press("enter")

#         print("✅ Group message sent")

#     except Exception as e:
#         print("❌ Failed:", e)

def send_all(message):
    try:
        res=send_telegram(message)
        print(f"Telegram sent status: {res}")
    except:
        print("Telegram failed")
        
    # try:
    #     send_whatsapp(message) # will not work for prod
    #     # send_whatsapp_group(message)
    # except:
    #     print("WhatsApp failed")
