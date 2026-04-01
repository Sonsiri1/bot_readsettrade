# import os
# import time
# from datetime import datetime

# from selenium import webdriver
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from core.database import SessionLocal
# from sqlalchemy import text
# from dotenv import load_dotenv

# load_dotenv()

# # DRIVER
# def get_driver():
#     options = Options()
#     options.add_argument("--headless=new")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")

#     driver = webdriver.Edge(options=options)
#     driver.set_page_load_timeout(15)
#     return driver

# # WAIT TABLE (สำคัญมาก)
# def wait_for_table(driver, symbol):
#     for attempt in range(3):
#         try:
#             table = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, "tableAnalystConcensus"))
#             )
#             print(f"{symbol}: เจอ table")
#             return table

#         except:
#             print(f"{symbol}: retry {attempt+1}")

#             # scroll เผื่อ lazy load
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)

#     return None

# # บันทึก database
# def save_to_db(records):
#     db = SessionLocal()
#     try:
#         for r in records:
#             db.execute(text("""
#                 INSERT INTO analyst_consensus (
#                     symbol, broker, analyst,
#                     eps_2569, eps_2570,
#                     profit_2569, profit_2570,
#                     pe_2569, pe_2570,
#                     pbv_2569, pbv_2570,
#                     dividend_2569, dividend_2570,
#                     target_price, upside_downside,
#                     recommendation, report_date, scraped_at
#                 )
#                 VALUES (
#                     :symbol, :broker, :analyst,
#                     :eps_2569, :eps_2570,
#                     :profit_2569, :profit_2570,
#                     :pe_2569, :pe_2570,
#                     :pbv_2569, :pbv_2570,
#                     :dividend_2569, :dividend_2570,
#                     :target_price, :upside_downside,
#                     :recommendation, :report_date, :scraped_at
#                 )
#                 ON CONFLICT (symbol, broker, analyst, report_date)
#                 DO UPDATE SET
#                     target_price = EXCLUDED.target_price,
#                     recommendation = EXCLUDED.recommendation,
#                     scraped_at = EXCLUDED.scraped_at
#             """), {**r, "scraped_at": datetime.now()})

#         db.commit()
#         print(f"บันทึก {len(records)} records")

#     except Exception as e:
#         db.rollback()
#         print("DB ERROR:", e)

#     finally:
#         db.close()

# # SCRAPE
# def scrape_symbol(driver, symbol):
#     url = f"https://www.settrade.com/th/equities/quote/{symbol.lower()}/analyst-consensus"
#     print(f"\nดึง {symbol}")

#     driver.get(url)

#     try:
#         # รอ body
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.TAG_NAME, "body"))
#         )

#         # scroll ครั้งแรก
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(1)

#         # ใช้ function retry จริง
#         table = wait_for_table(driver, symbol)

#         if not table:
#             print(f"{symbol}: ไม่เจอ table จริง ๆ")
#             return []

#     except Exception as e:
#         print(f"{symbol}: error -> {e}")
#         return []

#     rows = table.find_elements(By.TAG_NAME, "tr")

#     records = []
    
#     # กันข้อมูลบางอย่างสงมาแปลกๆ
#     def clean_text(val):
#         if not val:
#             return None

#         val = val.strip()

#         if val in ["-", "N/A", ""]:
#             return None

#          # ลบ - ทุกอย่าง
#         if val.startswith("-"):
#             val = val.lstrip("-").strip()

#         return val

#     for row in rows:
#         cols = row.find_elements(By.TAG_NAME, "td")
#         values = [c.text.strip() for c in cols]

#         if not values:
#             continue

#         # filter analyst
#         if len(values) >= 20 and values[1].isupper():
#             record = {
#                 "symbol": symbol,
#                 "broker": clean_text(values[1]),
#                 "analyst": clean_text(values[2]),
#                 "eps_2569": clean_text(values[4]),
#                 "eps_2570": clean_text(values[5]),
#                 "profit_2569": clean_text(values[7]),
#                 "profit_2570": clean_text(values[8]),
#                 "pe_2569": clean_text(values[10]),
#                 "pe_2570": clean_text(values[11]),
#                 "pbv_2569": clean_text(values[13]),
#                 "pbv_2570": clean_text(values[14]),
#                 "dividend_2569": clean_text(values[16]),
#                 "dividend_2570": clean_text(values[17]),
#                 "target_price": clean_text(values[19]),
#                 "upside_downside": clean_text(values[20]) if len(values) > 20 else None,
#                 "recommendation": clean_text(values[21]) if len(values) > 21 else None,
#                 "report_date": clean_text(values[22]) if len(values) > 22 else None,
#             }

#             records.append(record)

#     print(f"{symbol}: ได้ {len(records)} records")
#     return records

# def start_bot():
#     stocks_file = os.getenv("STOCKS_FILE", "stocks.txt")

#     with open(stocks_file, "r") as f:
#         symbols = [line.strip().upper() for line in f if line.strip()]

#     driver = get_driver()

#     try:
#         for symbol in symbols:
#             records = scrape_symbol(driver, symbol)

#             if records:
#                 save_to_db(records)
#             else:
#                 print(f"{symbol}: ไม่มีข้อมูล")

#             time.sleep(1)

#     finally:
#         driver.quit()
#         print("\nปิด browser")

import os
import time
import re
from datetime import datetime

# ใช้ Selenium สำหรับเปิดเว็บ
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlalchemy import text
from core.database import SessionLocal

from dotenv import load_dotenv

load_dotenv()


# เปิด Web (ไม่เปิดหน้าจอ) option ทำให้ไม่ต้องเปิดจอ
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(20)
    return driver

# จากข้อความแปลงเป็นทศนิยมเรียกว่า PARSE (แปลงข้อมูล) 
def parse_number(val):
    if not val:
        return None

    val = val.replace(",", "").strip()
    match = re.search(r"-?\d+(\.\d+)?", val)
    return float(match.group()) if match else None

# ดึงค่า % จากข้อความ เช่น "15.00 (+10.25%)" → 10.25
def parse_upside(val):
    if not val:
        return None

    match = re.search(r"\((-?\d+(\.\d+)?)%\)", val)
    return float(match.group(1)) if match else None

# แปลง ข้อความให้เป็นเวลา
def parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val.strip(), "%d/%m/%Y").date()
    except:
        return None


# กันเวลามีข้อความแปลกๆ เช่น "-" หรือ ไม่มีไรเลย
def clean_text(val):
    if not val:
        return None

    val = val.strip()

    if val in ["-", "N/A", ""]:
        return None

    return val


 # รอโหลดเสร็จ
def wait_for_table(driver, symbol):
    for attempt in range(3):
        try:
            # รอ tbody tr ของตาราง ไม่ใช่แค่รอหน้าโหลด
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#tableAnalystConcensus tbody tr")
                )
            )
            print(f"{symbol}: ✅ table loaded")
            return driver.find_element(By.ID, "tableAnalystConcensus")

        except:
            print(f"{symbol}: retry {attempt+1}")

            # scroll เพื่อให้เว็บโหลดข้อมูลเพิ่ม
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

    return None

# เอาเข้าดาต้าเบส
def save_to_db(records):
    db = SessionLocal()
    now = datetime.now()

    try:
        # เอา symbol ที่ไม่ซ้ำ
        symbols = list(set(r["symbol"] for r in records))

        for symbol in symbols:

            # ดึงข้อมูลเดิมของ symbol นี้
            old_rows = db.execute(text("""
                SELECT * FROM analyst_consensus
                WHERE symbol = :symbol
            """), {"symbol": symbol}).mappings().all()

            # map broker → row
            old_map = {row["broker"]: row for row in old_rows}

            # ข้อมูลใหม่ของ symbol นี้
            new_rows = [r for r in records if r["symbol"] == symbol]

            changed = False  # flag ว่ามีการเปลี่ยนไหม

            for r in new_rows:
                broker = r["broker"]

                if broker not in old_map:
                    # มี broker ใหม่
                    changed = True
                else:
                    old = old_map[broker]

                    # เช็คว่าข้อมูลเปลี่ยนไหม
                    if (
                        old["report_date"] != r["report_date"] or
                        old["target_price"] != r["target_price"] or
                        old["recommendation"] != r["recommendation"]
                    ):
                        changed = True

                # insert หรือ update ข้อมูลใหม่
                db.execute(text("""
                    INSERT INTO analyst_consensus (
                        symbol, broker, analyst,
                        eps_2569, eps_2570,
                        profit_2569, profit_2570,
                        pe_2569, pe_2570,
                        pbv_2569, pbv_2570,
                        dividend_2569, dividend_2570,
                        target_price, upside_value, upside_text,
                        recommendation, report_date, scraped_at
                    )
                    VALUES (
                        :symbol, :broker, :analyst,
                        :eps_2569, :eps_2570,
                        :profit_2569, :profit_2570,
                        :pe_2569, :pe_2570,
                        :pbv_2569, :pbv_2570,
                        :dividend_2569, :dividend_2570,
                        :target_price, :upside_value, :upside_text,
                        :recommendation, :report_date, :scraped_at
                    )
                    ON CONFLICT (symbol, broker)
                    DO UPDATE SET
                        analyst = EXCLUDED.analyst,
                        eps_2569 = EXCLUDED.eps_2569,
                        eps_2570 = EXCLUDED.eps_2570,
                        profit_2569 = EXCLUDED.profit_2569,
                        profit_2570 = EXCLUDED.profit_2570,
                        pe_2569 = EXCLUDED.pe_2569,
                        pe_2570 = EXCLUDED.pe_2570,
                        pbv_2569 = EXCLUDED.pbv_2569,
                        pbv_2570 = EXCLUDED.pbv_2570,
                        dividend_2569 = EXCLUDED.dividend_2569,
                        dividend_2570 = EXCLUDED.dividend_2570,
                        target_price = EXCLUDED.target_price,
                        upside_value = EXCLUDED.upside_value,
                        upside_text = EXCLUDED.upside_text,
                        recommendation = EXCLUDED.recommendation,
                        report_date = EXCLUDED.report_date,
                        scraped_at = EXCLUDED.scraped_at
                """), {**r, "scraped_at": now})

            # ถ้ามีการเปลี่ยน บันทึก history
            if changed:
                latest_rows = db.execute(text("""
                    SELECT * FROM analyst_consensus
                    WHERE symbol = :symbol
                """), {"symbol": symbol}).mappings().all()

                for row in latest_rows:
                    db.execute(text("""
                        INSERT INTO analyst_consensus_history (
                            symbol, broker, analyst,
                            eps_2569, eps_2570,
                            profit_2569, profit_2570,
                            pe_2569, pe_2570,
                            pbv_2569, pbv_2570,
                            dividend_2569, dividend_2570,
                            target_price, upside_value, upside_text,
                            recommendation, report_date,
                            scraped_at, batch_time
                        )
                        VALUES (
                            :symbol, :broker, :analyst,
                            :eps_2569, :eps_2570,
                            :profit_2569, :profit_2570,
                            :pe_2569, :pe_2570,
                            :pbv_2569, :pbv_2570,
                            :dividend_2569, :dividend_2570,
                            :target_price, :upside_value, :upside_text,
                            :recommendation, :report_date,
                            :scraped_at, :batch_time
                        )
                    """), {**row, "scraped_at": now, "batch_time": now})

                print(f"บันทึก history ของ {symbol}")

        db.commit()
        print(f"บันทึก {len(records)} รายการ")

    except Exception as e:
        db.rollback()
        print("ดาต้าเบสมีปัญหา:", e)

    finally:
        db.close()

# SCRAPE (ดึงข้อมูลหลัก)
def scrape_symbol(driver, symbol):
    url = f"https://www.settrade.com/th/equities/quote/{symbol.lower()}/analyst-consensus"
    print(f"\n📊 {symbol}")

    driver.get(url)

    try:
        # รอหน้าเว็บโหลด
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # scroll เพื่อให้ table โหลด
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        table = wait_for_table(driver, symbol)

        if not table:
            print(f"{symbol}: ไม่เจอ table")
            return []

    except Exception as e:
        print(f"{symbol}: error -> {e}")
        return []

    rows = table.find_elements(By.TAG_NAME, "tr")
    records = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        values = [c.text.strip() for c in cols]

        # ข้ามแถวที่ไม่ใช่ข้อมูล
        if not values or len(values) < 20:
            continue

        broker = clean_text(values[1])
        analyst = clean_text(values[2])

        # กรองแถวสรุป เช่น Average / Median
        if not broker or broker.lower() in ["average", "median", "high", "low"]:
            continue

        # สร้างข้อมูลเป็น dict
        record = {
            "symbol": symbol,
            "broker": broker,
            "analyst": analyst,

            "eps_2569": parse_number(values[4]),
            "eps_2570": parse_number(values[5]),

            "profit_2569": parse_number(values[7]),
            "profit_2570": parse_number(values[8]),

            "pe_2569": parse_number(values[10]),
            "pe_2570": parse_number(values[11]),

            "pbv_2569": parse_number(values[13]),
            "pbv_2570": parse_number(values[14]),

            "dividend_2569": parse_number(values[16]),
            "dividend_2570": parse_number(values[17]),

            "target_price": parse_number(values[19]),

            # แยก value กับ text เพื่อให้ frontend ใช้ง่าย
            "upside_value": parse_upside(values[20]),
            "upside_text": clean_text(values[20]),

            "recommendation": clean_text(values[21]) if len(values) > 21 else None,
            "report_date": parse_date(values[22]) if len(values) > 22 else None,
        }

        records.append(record)

    print(f"{symbol}: ผ่านแล้วเย้ {len(records)} rows")
    return records


# ควบคุมทั้งหมด)
def start_bot():
    # อ่านรายชื่อหุ้น จากไฟล์ แล้ว save
    # db = SessionLocal()
    # result = db.execute(text("SELECT symbol FROM companies WHERE symbol IS NOT NULL"))
    # symbols = [row[0] for row in result.fetchall()]
    stocks_file = os.getenv("STOCKS_FILE", "stocks.txt")

    # อ่าน symbol จากไฟล์
    with open(stocks_file, "r") as f:
        # ข้ามบรรทัดว่าง และทำให้เป็นตัวใหญ่หมด
        symbols = [line.strip().upper() for line in f if line.strip()]

    driver = get_driver()
    success_symbol = 0
    failed_symbol = 0
    total_symbol = len(symbols)

    try:
        for symbol in symbols:
            # ดึงข้อมูลจากเว็บ
            records = scrape_symbol(driver, symbol)

            if records:
                save_to_db(records)
                success_symbol += 1
            else:
                print(f"{symbol}: ไม่มีข้อมูล")
                failed_symbol += 1

            time.sleep(1)

    finally:
        # ปิด browser ทุกครั้งไม่งั้นจะค้าง
        driver.quit()
        print("\nปิด browser")
        # สรุปผล
        print(f"ทั้งหมด: {total_symbol} ตัว")
        print(f"สำเร็จ: {success_symbol} ตัว")
        print(f"ไม่สำเร็จ: {failed_symbol} ตัว")