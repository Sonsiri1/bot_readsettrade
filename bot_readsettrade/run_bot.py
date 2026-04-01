import os
from arrow import now
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from jobs.bot import start_bot

def run_bot():
    now = datetime.now()
    
    # ข้ามวันหยุดสุดสัปดาห์
    if now.weekday() >= 5:
        print("วันหยุด ไม่รัน")
        return
    
    print(f"\nเริ่มรันบอท: {now.strftime('%H:%M:%S')}")
    
    start = datetime.now()

    try:
        start_bot()
    except Exception as e:
        print(f"บอทพัง: {e}")

    # จบการจับเวลา
    duration = datetime.now() - start
    print(f"ใช้เวลาไป: {duration}")


if __name__ == "__main__":
    print("โหลด .env สำเร็จ")
    
    # ลองว่าได้ไหม
    # print(f"APP_ID ที่อ่านได้คือ: {os.getenv('STT-OPENAPI-AUTH-BROKER-ID')}") 
    # start_bot()
    # รันหลัง 1 ทุ่ม
    schedule.every().day.at("19:00").do(run_bot)
    schedule.every().day.at("23:20").do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(1)

# from arrow import now
# from datetime import datetime
# from dotenv import load_dotenv

# load_dotenv()

# from jobs.bot import start_bot


# def run_bot():
#     now_time = datetime.now()

#     # ข้ามวันหยุด
#     if now_time.weekday() >= 5:
#         print("วันหยุด ไม่รัน")
#         return

#     print(f"\nเริ่มรันบอท: {now_time.strftime('%H:%M:%S')}")

#     start = datetime.now()

#     try:
#         start_bot()
#     except Exception as e:
#         print(f"บอทพัง: {e}")

#     duration = datetime.now() - start
#     print(f"ใช้เวลาไป: {duration}")