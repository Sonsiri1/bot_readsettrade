import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.database import SessionLocal
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# DRIVER
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(15)
    return driver

# WAIT TABLE (สำคัญมาก)
def wait_for_table(driver, symbol):
    for attempt in range(3):
        try:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tableAnalystConcensus"))
            )
            print(f"{symbol}: เจอ table")
            return table

        except:
            print(f"{symbol}: retry {attempt+1}")

            # scroll เผื่อ lazy load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

    return None

# บันทึก database
def save_to_db(records):
    db = SessionLocal()
    try:
        for r in records:
            db.execute(text("""
                INSERT INTO analyst_consensus (
                    symbol, broker, analyst,
                    eps_2569, eps_2570,
                    profit_2569, profit_2570,
                    pe_2569, pe_2570,
                    pbv_2569, pbv_2570,
                    dividend_2569, dividend_2570,
                    target_price, upside_downside,
                    recommendation, report_date, scraped_at
                )
                VALUES (
                    :symbol, :broker, :analyst,
                    :eps_2569, :eps_2570,
                    :profit_2569, :profit_2570,
                    :pe_2569, :pe_2570,
                    :pbv_2569, :pbv_2570,
                    :dividend_2569, :dividend_2570,
                    :target_price, :upside_downside,
                    :recommendation, :report_date, :scraped_at
                )
                ON CONFLICT (symbol, broker, analyst, report_date)
                DO UPDATE SET
                    target_price = EXCLUDED.target_price,
                    recommendation = EXCLUDED.recommendation,
                    scraped_at = EXCLUDED.scraped_at
            """), {**r, "scraped_at": datetime.now()})

        db.commit()
        print(f"บันทึก {len(records)} records")

    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)

    finally:
        db.close()

# SCRAPE
def scrape_symbol(driver, symbol):
    url = f"https://www.settrade.com/th/equities/quote/{symbol.lower()}/analyst-consensus"
    print(f"\nดึง {symbol}")

    driver.get(url)

    try:
        # รอ body
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # scroll ครั้งแรก
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # ใช้ function retry จริง
        table = wait_for_table(driver, symbol)

        if not table:
            print(f"{symbol}: ไม่เจอ table จริง ๆ")
            return []

    except Exception as e:
        print(f"{symbol}: error -> {e}")
        return []

    rows = table.find_elements(By.TAG_NAME, "tr")

    records = []
    
    # กันข้อมูลบางอย่างสงมาแปลกๆ
    def clean_text(val):
        if not val:
            return None

        val = val.strip()

        if val in ["-", "N/A", ""]:
            return None

         # ลบ - ทุกอย่าง
        if val.startswith("-"):
            val = val.lstrip("-").strip()

        return val

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        values = [c.text.strip() for c in cols]

        if not values:
            continue

        # filter analyst
        if len(values) >= 20 and values[1].isupper():
            record = {
                "symbol": symbol,
                "broker": clean_text(values[1]),
                "analyst": clean_text(values[2]),
                "eps_2569": clean_text(values[4]),
                "eps_2570": clean_text(values[5]),
                "profit_2569": clean_text(values[7]),
                "profit_2570": clean_text(values[8]),
                "pe_2569": clean_text(values[10]),
                "pe_2570": clean_text(values[11]),
                "pbv_2569": clean_text(values[13]),
                "pbv_2570": clean_text(values[14]),
                "dividend_2569": clean_text(values[16]),
                "dividend_2570": clean_text(values[17]),
                "target_price": clean_text(values[19]),
                "upside_downside": clean_text(values[20]) if len(values) > 20 else None,
                "recommendation": clean_text(values[21]) if len(values) > 21 else None,
                "report_date": clean_text(values[22]) if len(values) > 22 else None,
            }

            records.append(record)

    print(f"{symbol}: ได้ {len(records)} records")
    return records

def start_bot():
    stocks_file = os.getenv("STOCKS_FILE", "stocks.txt")

    with open(stocks_file, "r") as f:
        symbols = [line.strip().upper() for line in f if line.strip()]

    driver = get_driver()

    try:
        for symbol in symbols:
            records = scrape_symbol(driver, symbol)

            if records:
                save_to_db(records)
            else:
                print(f"{symbol}: ไม่มีข้อมูล")

            time.sleep(1)

    finally:
        driver.quit()
        print("\nปิด browser")