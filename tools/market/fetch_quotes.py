#!/usr/bin/env python3
"""Собирает дневные котировки сырья и валют для экрана «Рынок» (PLD Polymer Sales AI).

Источники (бесплатные, без ключей):
  - Sina Finance — непрерывные главные контракты DCE / ZCE (агрегатор, неофициально)
  - FRED (данные EIA) — Brent spot, задержка ~1 неделя
  - MOEX ISS — CNY/RUB, режим TOM
  - ЦБ РФ — официальные курсы USD и CNY

Запуск:  python3 tools/market/fetch_quotes.py [out_dir]
Результат: <out_dir>/series.json — список документов для коллекции `series`.
"""
import csv
import io
import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone

DAYS = 740  # ~2 года истории
UA = {"User-Agent": "Mozilla/5.0 (PLD Polymer market fetcher)"}

FUTURES = [
    # id, sina symbol, name, venue, mats
    ("lldpe", "L0", "LLDPE", "DCE · фьючерс", "POE, POP, OBC, MLLDPE, XLPE"),
    ("pp", "PP0", "Полипропилен", "DCE · фьючерс", "POP, ориентир рынка полиолефинов"),
    ("propylene", "PL0", "Пропилен", "DCE · фьючерс", "POP, PP-компаунды"),
    ("styrene", "EB0", "Стирол", "DCE · фьючерс", "PC/ABS (компонент ABS)"),
    ("benzene", "BZ0", "Бензол", "DCE · фьючерс", "PC (фенол → бисфенол-А), PA66 (адипиновая кислота)"),
    ("methanol", "MA0", "Метанол", "ZCE · фьючерс", "POM (формальдегид), PMMA (ММА)"),
]


def get(url, headers=None, timeout=30, attempts=3):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    for n in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except OSError:
            if n == attempts - 1:
                raise
            time.sleep(3 * (n + 1))


def since():
    return date.today() - timedelta(days=DAYS)


def sina(symbol):
    url = ("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_x=/"
           f"InnerFuturesNewService.getDailyKLine?symbol={symbol}")
    text = get(url, {"Referer": "https://finance.sina.com.cn"}).decode("utf-8")
    rows = json.loads(text[text.index("(") + 1:text.rindex(")")])
    start = since().isoformat()
    return [[r["d"], float(r["c"])] for r in rows if r["d"] >= start]


def fred(series_id):
    text = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}").decode("utf-8")
    start = since().isoformat()
    out = []
    for row in csv.DictReader(io.StringIO(text)):
        v = row.get(series_id, "")
        d = row.get("observation_date") or row.get("DATE")
        if d >= start and v not in ("", "."):
            out.append([d, float(v)])
    return out


def moex(secid, board="CETS"):
    out, startrow = [], 0
    base = (f"https://iss.moex.com/iss/history/engines/currency/markets/selt/boards/{board}/"
            f"securities/{secid}.json?from={since().isoformat()}&history.columns=TRADEDATE,CLOSE")
    while True:
        data = json.loads(get(f"{base}&start={startrow}"))
        rows = data["history"]["data"]
        out += [[d, c] for d, c in rows if c]
        idx, total, size = data["history.cursor"]["data"][0]
        startrow = idx + size
        if startrow >= total or not rows:
            return out


def cbr(code):
    d1, d2 = since().strftime("%d/%m/%Y"), date.today().strftime("%d/%m/%Y")
    xml = get(f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={d1}&date_req2={d2}&VAL_NM_RQ={code}")
    out = []
    for rec in ET.fromstring(xml).findall("Record"):
        d = datetime.strptime(rec.get("Date"), "%d.%m.%Y").date().isoformat()
        out.append([d, round(float(rec.find("VunitRate").text.replace(",", ".")), 4)])
    return out


def doc(id_, name, venue, unit, source, source_url, mats, points):
    return {"id": id_, "name": name, "venue": venue, "unit": unit, "source": source,
            "sourceUrl": source_url, "mats": mats, "points": points,
            "last": points[-1] if points else None}


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    docs, errors = [], []
    jobs = [(lambda i=i, s=s, n=n, v=v, m=m: doc(i, n, v, "CNY/т", "Sina Finance (главный контракт)",
                                                 "https://finance.sina.com.cn/futuremarket/", m, sina(s)))
            for i, s, n, v, m in FUTURES]
    jobs += [
        lambda: doc("brent", "Brent", "спот · EIA", "$/барр.", "FRED / EIA (DCOILBRENTEU)",
                    "https://fred.stlouisfed.org/series/DCOILBRENTEU",
                    "все материалы (нафта → этилен, пропилен, бензол)", fred("DCOILBRENTEU")),
        lambda: doc("cnyrub", "CNY/RUB", "MOEX · TOM", "₽ за ¥", "Московская биржа (ISS)",
                    "https://www.moex.com/ru/issue.aspx?code=CNYRUB_TOM",
                    "рублёвые цены для клиентов РФ", moex("CNYRUB_TOM")),
    ]
    for job in jobs:
        try:
            docs.append(job())
        except Exception as e:  # один упавший источник не должен ронять остальные
            errors.append(repr(e))

    try:
        usd, cny = cbr("R01235"), cbr("R01375")
        docs.append(doc("usdrub", "USD/RUB", "ЦБ РФ · офиц.", "₽ за $", "Банк России",
                        "https://www.cbr.ru/currency_base/dynamics/", "цены в рублях, пошлины", usd))
        cny_by_date = dict(cny)
        cross = [[d, round(v / cny_by_date[d], 4)] for d, v in usd if d in cny_by_date]
        docs.append(doc("usdcny", "USD/CNY", "кросс-курс ЦБ РФ", "¥ за $", "Банк России (USD/RUB ÷ CNY/RUB)",
                        "https://www.cbr.ru/currency_base/dynamics/", "закупка в юанях, КП в долларах", cross))
    except Exception as e:
        errors.append(repr(e))

    status = {"updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "series": len(docs), "errors": errors}
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "series.json"), "w", encoding="utf-8") as f:
        json.dump({"status": status, "series": docs}, f, ensure_ascii=False)
    # Таблицы для дашборда «Рынок сырья PLD Polymer»: один файл на источник,
    # строки {series, date, close}
    by_id = {d["id"]: d for d in docs}
    groups = {
        "cn_futures": [i for i, *_ in FUTURES],
        "brent": ["brent"],
        "cnyrub_moex": ["cnyrub"],
        "cbr_fx": ["usdrub", "usdcny"],
    }
    for name, ids in groups.items():
        rows = [{"series": i, "date": d, "close": c}
                for i in ids if i in by_id for d, c in by_id[i]["points"]]
        with open(os.path.join(out_dir, f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))

    for d in docs:
        print(f"{d['id']:10} {len(d['points']):4} pts  last {d['last']}")
    if errors:
        print("ERRORS:", *errors, sep="\n  ")


if __name__ == "__main__":
    main()
