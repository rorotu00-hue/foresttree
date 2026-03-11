import os
import csv
from datetime import datetime
import requests

BASE_DIR = r"G:\내 드라이브\Foresttree"
DATA_DIR = os.path.join(BASE_DIR, "data")
PRICE_FILE = os.path.join(DATA_DIR, "garak_price_history.csv")

API_URL = "https://db.garak.co.kr:9443/api/datasources/40f2c32edec68ae89c0994c0f2d8dab6"

CSV_HEADERS = [
    "수집일시", "기준일자", "시장", "품목", "품종", "등급", "단위",
    "최저가", "최고가", "평균가", "거래량", "반입량",
    "전일평균가", "전일대비금액", "전일대비율",
    "전주평균가", "전주대비금액", "전주대비율",
    "전년평균가", "전년대비금액", "전년대비율",
    "알림여부", "알림시간", "원본URL", "비고"
]

def make_payload():
    today = datetime.now().strftime("%Y%m%d")
    return {
        "mrktDiv": "1",
        "startDate": today,
        "endDate": today,
        "handlClssCd": "2",
        "selectedItmCd": "",
        "selectedRptvItmCd": "",
        "selectedItmNm": ""
    }

def safe_number(value):
    if value in [None, "", "-"]:
        return ""
    try:
        if isinstance(value, str):
            value = value.replace(",", "").replace("%", "").strip()
        num = float(value)
        return int(num) if num.is_integer() else num
    except:
        return value

def extract_rate_number(rate_text):
    if not rate_text:
        return ""

    text = str(rate_text).strip()

    if "(" in text and ")" in text:
        inside = text.split("(")[-1].split(")")[0]
        return safe_number(inside)

    return safe_number(text)

def make_unit_value(item):
    unit_qty = str(item.get("UNIT_QTY", "")).strip()
    unit_name = str(item.get("UNIT", "")).strip()

    # UNIT 값에 이미 10kg상자 같은 완성형 값이 들어있는 경우 그대로 사용
    if unit_name and any(ch.isdigit() for ch in unit_name):
        unit_value = unit_name

    # UNIT 값이 상자/망/포대 등만 있을 때만 수량과 결합
    elif unit_qty and unit_name:
        unit_value = f"{unit_qty}{unit_name}"

    # 하나만 있으면 있는 값 사용
    else:
        unit_value = unit_name or unit_qty

    # 혹시 생길 수 있는 중복 패턴 보정
    replacements = {
        "1010kg": "10kg",
        "2020kg": "20kg",
        "3030kg": "30kg",
        "4040kg": "40kg",
        "5050kg": "50kg",
        "kgkg": "kg",
    }

    for old, new in replacements.items():
        unit_value = unit_value.replace(old, new)

    return unit_value

def fetch_garak_data():
    payload = make_payload()

    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://db.garak.co.kr:9443",
        "Referer": "https://db.garak.co.kr:9443",
        "User-Agent": "Mozilla/5.0",
        "dashboard-token": "9D4EBB9B3B9AF6176EF913F22BBDACB0F545DB9D569B1499244944825CF0540E68532E26C6991DC0C5C28242479B53244A5E9893BB8CFB159984EB6E5DE2D519",
        "Cookie": "JSESSIONID=BLxvmdDfZQ6bsbk4Sflupn2JbLs5ccxzorSEbzuM1TUTafYdtyswWAO8w7Pdj2PA.amV1c19kb21haW4veW91dG9uZw==; JSESSIONID=B51FD656ADA9B1AA685B189384E5A8D9"
    }

    res = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    res.raise_for_status()

    data = res.json()
    dataset = data.get("dataset", [])

    if not dataset:
        print("가져온 데이터가 없습니다.")
        return []

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []

    for item in dataset:
        invest_dt = str(item.get("INVEST_DT", "")).strip()
        base_date = invest_dt.replace(".", "-") if invest_dt else datetime.now().strftime("%Y-%m-%d")
        unit_value = make_unit_value(item)

        row = {
            "수집일시": now,
            "기준일자": base_date,
            "시장": "가락시장",
            "품목": item.get("ITM_NM", ""),
            "품종": item.get("RPTV_ITM_NM", ""),
            "등급": item.get("G_NAME", ""),
            "단위": unit_value,
            "최저가": safe_number(item.get("MI_P")),
            "최고가": safe_number(item.get("MA_P")),
            "평균가": safe_number(item.get("AV_P")),
            "거래량": "",
            "반입량": "",
            "전일평균가": "",
            "전일대비금액": safe_number(item.get("FLT_P")),
            "전일대비율": extract_rate_number(item.get("PAV_RATE")),
            "전주평균가": "",
            "전주대비금액": "",
            "전주대비율": extract_rate_number(item.get("J_7_RATE")),
            "전년평균가": "",
            "전년대비금액": "",
            "전년대비율": extract_rate_number(item.get("J_365_RATE")),
            "알림여부": "N",
            "알림시간": "",
            "원본URL": API_URL,
            "비고": ""
        }

        rows.append(row)

    return rows

def save_data(rows):
    if not rows:
        print("저장할 데이터가 없습니다.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(PRICE_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)}건 저장 완료")

def main():
    rows = fetch_garak_data()
    save_data(rows)
    print("garak_api 실행 완료")

if __name__ == "__main__":
    main()