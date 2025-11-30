import os
import sys
import json
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

SERVER = os.getenv('TEST_SERVER', 'http://127.0.0.1:8000')
USER = os.getenv('TEST_USER', 'test_admin')
PASS = os.getenv('TEST_PASS', 'Test1234!')

def post_json(path, payload, token=None):
    url = SERVER + path
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.getcode(), r.read().decode('utf-8')

def get_with_token(path, token=None):
    url = SERVER + path
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.getcode(), r.read().decode('utf-8')

def try_call(func, *args, **kwargs):
    try:
        code, body = func(*args, **kwargs)
        print(f'OK {code}:', args[0] if args else '')
        print(body)
    except urllib.error.HTTPError as he:
        try:
            body = he.read().decode('utf-8')
        except Exception:
            body = '<no body>'
        print(f'HTTPError {he.code} for {args[0] if args else ""}:', body)
    except Exception as e:
        print('Error calling', args[0] if args else '', repr(e))

def main():
    print('Logging in as', USER)
    try:
        code, resp = post_json('/auth/login', {'usuario': USER, 'contrasena': PASS})
        data = json.loads(resp)
        access = data.get('access_token')
        refresh = data.get('refresh_token')
        print('Login returned', code)
    except Exception as e:
        print('Login failed:', e)
        return

    # Public and protected GETs
    endpoints = [
        '/',
        '/health',
        '/beneficios/',
        '/periodos/',
        '/trabajadores/',
        '/sucursales/',
        '/usuarios/',
        '/entregas/',
        '/reportes/entregas-por-beneficio?periodo=2025Q4',
    ]

    for ep in endpoints:
        print('\nGET', ep)
        try_call(get_with_token, ep, access)

    # Test creating a new usuario (POST /usuarios/) — do not create if exists
    new_user = f'temp_user_{os.getpid()}'
    print('\nPOST /usuarios/ -> creating', new_user)
    payload = {'usuario': new_user, 'contrasena': 'TempPass123!', 'rol': 'operador'}
    try_call(post_json, '/usuarios/', payload, access)

    # Test refresh token rotation
    print('\nTesting /auth/refresh with refresh token')
    try:
        req = urllib.request.Request(SERVER + '/auth/refresh', data=b'', headers={'Authorization': f'Bearer {refresh}'})
        with urllib.request.urlopen(req, timeout=15) as r:
            print('/auth/refresh ->', r.getcode())
            print(r.read().decode('utf-8'))
    except urllib.error.HTTPError as he:
        try:
            body = he.read().decode('utf-8')
        except Exception:
            body = '<no body>'
        print('HTTPError', he.code, body)
    except Exception as e:
        print('Error calling /auth/refresh:', repr(e))

    # Test logout (use the refresh token again to logout)
    print('\nTesting /auth/logout with refresh token')
    try:
        req = urllib.request.Request(SERVER + '/auth/logout', data=b'', headers={'Authorization': f'Bearer {refresh}'})
        with urllib.request.urlopen(req, timeout=15) as r:
            print('/auth/logout ->', r.getcode())
            print(r.read().decode('utf-8'))
    except urllib.error.HTTPError as he:
        try:
            body = he.read().decode('utf-8')
        except Exception:
            body = '<no body>'
        print('HTTPError', he.code, body)
    except Exception as e:
        print('Error calling /auth/logout:', repr(e))

if __name__ == '__main__':
    main()
