import os
import sys
import json
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

SERVER = os.getenv('TEST_SERVER', 'http://127.0.0.1:8000')

def post_json(path, payload):
    url = SERVER + path
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as he:
        try:
            body = he.read().decode('utf-8')
        except Exception:
            body = '<no body>'
        raise RuntimeError(f'HTTP {he.code}: {body}')

def get_with_token(path, token):
    url = SERVER + path
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.getcode(), r.read().decode('utf-8')

def main():
    username = os.getenv('TEST_USER', 'test_admin')
    password = os.getenv('TEST_PASS', 'Test1234!')
    print('Logging in as', username)
    try:
        resp = post_json('/auth/login', {'usuario': username, 'contrasena': password})
        print('Login response:', resp)
        access = resp.get('access_token')
        if not access:
            print('No access token returned')
            return
        code, body = get_with_token('/beneficios/', access)
        print('GET /beneficios/ ->', code)
        print(body)
    except Exception as e:
        print('Error during test calls:', e)
        raise

if __name__ == '__main__':
    main()
