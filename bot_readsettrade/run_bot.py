# import os
from arrow import now
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from jobs.bot import start_bot

if __name__ == "__main__":
    print("โหลด .env สำเร็จ")
    
    # ลองว่าได้ไหม
    # print(f"APP_ID ที่อ่านได้คือ: {os.getenv('STT-OPENAPI-AUTH-BROKER-ID')}") 
    # start_bot()
    def run_if_bot_open():
        now = datetime.now()
        
        # # ข้ามวันหยุดสุดสัปดาห์
        if now.weekday() >= 5:
            print("วันหยุด ไม่รัน")
            return
        
        t = now.time()
        morning   = datetime.strptime("10:00", "%H:%M").time() <= t <= datetime.strptime("12:30", "%H:%M").time()
        afternoon = datetime.strptime("14:30", "%H:%M").time() <= t <= datetime.strptime("16:30", "%H:%M").time()
        
        if morning or afternoon:
            # เริ่มจับเวลา
            start = datetime.now()
            print(f"\nเริ่มรันบอท: {start.strftime('%H:%M:%S')} (ตลาดเปิด)")

            try:
                start_bot()
            except Exception as e:
                print(f"บอทพัง: {e}")

            # จบการจับเวลา
            duration = datetime.now() - start
            print(f"ใช้เวลาไป: {duration}")
        else:
            print(f"{now.strftime('%H:%M')} | ตลาดปิด ข้ามการทำงาน")

# รันตอนเปิด/ปิดตลาด
schedule.every().day.at("10:00").do(run_if_bot_open)  # เช้า
schedule.every().day.at("12:30").do(run_if_bot_open)  # เที่ยง
schedule.every().day.at("14:30").do(run_if_bot_open)  # บ่าย
schedule.every().day.at("16:30").do(run_if_bot_open)  # ปิด

print("บอททำงานแล้วนะ")

while True:
    schedule.run_pending()
    time.sleep(1)