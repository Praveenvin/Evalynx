import requests

try:
    response = requests.get("http://localhost:8000/api/mock-interview/history?page=1&page_size=10")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
except Exception as e:
    print("ERROR:", e)
