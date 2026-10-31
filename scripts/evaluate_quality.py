import json
import os
import sys
import urllib.request
import time

URL = "http://localhost:5678/webhook/review"
KEY = os.environ.get("KEY")

if not KEY:
    sys.exit("Переменная KEY не задана. Выполни: export KEY=$(grep '^WEBHOOK_KEY=' .env | cut -d= -f2 | tr -d '\r \" ')")

with open("data/golden_set.json", encoding="utf-8") as f:
    golden = json.load(f)

correct_sent = 0
correct_cat = 0
total = len(golden)

print(f"Запускаю проверку {total} отзывов...\n")

for i, item in enumerate(golden, 1):
    body = {"article": "TEST", "rating": 5, "text": item["text"]}
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-API-Key": KEY},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            
            got_sent = data.get("sentiment")
            got_cat = data.get("category")
            
            match_sent = (got_sent == item["expected_sentiment"])
            match_cat = (got_cat == item["expected_category"])
            
            if match_sent: correct_sent += 1
            if match_cat: correct_cat += 1
            
            print(f"[{i}/{total}] Sent: {'OK' if match_sent else 'FAIL'} | Cat: {'OK' if match_cat else 'FAIL'}")
            if not match_sent:
                print(f"   -> Ожидали: {item['expected_sentiment']}, Получили: {got_sent}")
            if not match_cat:
                print(f"   -> Ожидали: {item['expected_category']}, Получили: {got_cat}")
                
    except Exception as e:
        print(f"[{i}/{total}] Ошибка: {e}")
    
    time.sleep(1)

print("\n" + "="*30)
print(f"ИТОГО:")
print(f"Тональность: {correct_sent}/{total} ({correct_sent/total*100:.1f}%)")
print(f"Категория:   {correct_cat}/{total} ({correct_cat/total*100:.1f}%)")
print("="*30)