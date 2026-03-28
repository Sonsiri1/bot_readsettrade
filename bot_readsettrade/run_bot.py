# import os
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
    def run_if_market_open():
        now = datetime.now()
        
        # # ข้ามวันหยุดสุดสัปดาห์
        if now.weekday() >= 5:
            print("วันหยุด ไม่รัน")
            return
        
        t = now.time()
        morning   = datetime.strptime("10:00", "%H:%M").time() <= t <= datetime.strptime("12:30", "%H:%M").time()
        afternoon = datetime.strptime("14:30", "%H:%M").time() <= t <= datetime.strptime("16:30", "%H:%M").time()
        
        if morning or afternoon:
            print(f"{now.strftime('%H:%M')} ตลาดเปิด รันบอท")
            start_bot()
        else:
            print(f"{now.strftime('%H:%M')} ตลาดปิด ข้าม")

def job():
    run_if_market_open()
# รันตอนเปิด/ปิดตลาด
schedule.every().day.at("10:00").do(job)  # เช้า
schedule.every().day.at("12:30").do(job)  # เที่ยง
schedule.every().day.at("14:30").do(job)  # บ่าย
schedule.every().day.at("16:30").do(job)  # ปิด

print("บอททำงานแล้วนะ")

while True:
    schedule.run_pending()
    time.sleep(1)