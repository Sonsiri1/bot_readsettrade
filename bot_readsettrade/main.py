import threading

from fastapi import FastAPI
from api.analysts_api import router as analysts_router
from api.auth_api import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysts_router, prefix="/api", tags=["Analysts"])
app.include_router(auth_router, prefix="/api", tags=["Auth"])


from run_bot import run_bot
# BOT
def start_scheduler():
    import schedule
    import time

    print("บอทพร้อมทำงานแล้ว")

    # ตั้งเวลา
    schedule.every().day.at("19:00").do(run_bot)
    schedule.every().day.at("23:00").do(run_bot)

    # loop ตลอด
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Scheduler error: {e}")
        time.sleep(1)


# RUN BOT ตอน START SERVER
@app.on_event("startup")
def start_bot():
    thread = threading.Thread(target=start_scheduler, daemon=True)
    thread.start()