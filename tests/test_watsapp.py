import requests
import pywhatkit as kit
import time

def send_whatsapp(msg):
    # send instantly (must keep WhatsApp Web logged in)
    print("📲 Sending WhatsApp...")
    kit.sendwhatmsg_instantly(
        phone_no="+919313845079",
        message=msg,
        wait_time=70,
        tab_close=True
    )
    time.sleep(5)
    print("Watsapp Sent")

send_whatsapp("hi ")