import json
import os
import sys
import time
import urllib.error
import urllib.request

URL = "http://localhost:5678/webhook/review"
KEY = os.environ.get("KEY")
if not KEY:
    sys.exit("Переменная KEY не задана")

path = sys.argv[1] if len(sys.argv) > 1 else "data/test_reviews.json"
with open(path, encoding="utf-8") as f:
    reviews = json.load(f)

for i, review in enumerate(reviews, 1):
    body = {"article": review.get("article"), "rating": review.get("rating"), "text": review.get("text")}
    request = urllib.request.Request(
        URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-API-Key": KEY},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            code = response.status
            answer = json.loads(response.read())
    except urllib.error.HTTPError as error:
        code = error.code
        answer = json.loads(error.read() or b"{}")
    print(i, code, answer.get("sentiment"), answer.get("category"), answer.get("provider"), answer.get("error"))
    time.sleep(1)