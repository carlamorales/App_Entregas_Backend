import urllib.request
import json

URLS = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/health',
    'http://127.0.0.1:8000/beneficios/',
    'http://127.0.0.1:8000/reportes/entregas-por-beneficio?periodo=2025Q4',
]

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read().decode('utf-8')
            print('URL:', url)
            print('STATUS:', r.status)
            print('BODY:', body)
    except urllib.error.HTTPError as he:
        print('URL:', url)
        try:
            body = he.read().decode('utf-8')
        except Exception:
            body = '<no body>'
        print('HTTPError:', he.code, he.reason)
        print('BODY:', body)
    except Exception as e:
        print('URL:', url)
        print('ERROR:', repr(e))

def main():
    for u in URLS:
        fetch(u)

if __name__ == '__main__':
    main()
