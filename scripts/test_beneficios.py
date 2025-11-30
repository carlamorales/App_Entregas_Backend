import os
import sys
import json
import urllib.request
import time

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

def main():
    print('Login as', USER)
    try:
        code, body = post_json('/auth/login', {'usuario': USER, 'contrasena': PASS})
        print('Login', code)
        data = json.loads(body)
        access = data.get('access_token')
        if not access:
            print('No access token returned')
            return
    except Exception as e:
        print('Login failed:', e)
        return

    print('\n1) GET /beneficios/')
    try:
        c, b = get_with_token('/beneficios/', access)
        print(c, b)
    except Exception as e:
        print('Error GET list:', e)

    codigo = f'temp_ben_{int(time.time())}'
    payload = {'codigo': codigo, 'nombre_beneficio': 'Beneficio Temporal', 'descripcion': 'Creado por pruebas', 'activo': True}
    print('\n2) POST /beneficios/ ->', payload)
    try:
        c, b = post_json('/beneficios/', payload, access)
        print(c, b)
    except Exception as e:
        print('Error POST:', e)
        return

    print(f"\n3) GET /beneficios/{codigo}")
    try:
        c, b = get_with_token(f'/beneficios/{codigo}', access)
        print(c, b)
    except Exception as e:
        print('Error GET by id:', e)

    print(f"\n4) PUT /beneficios/{codigo} -> actualizar nombre")
    try:
        c, b = post_json(f'/beneficios/{codigo}', {'nombre_beneficio': 'Beneficio Actualizado'}, access)
        print('Note: script uses POST for update if server expects it; response:')
        print(c, b)
    except Exception as e:
        print('Error PUT (using POST):', e)
        # Try real PUT
        try:
            req = urllib.request.Request(SERVER + f'/beneficios/{codigo}', data=json.dumps({'nombre_beneficio':'Beneficio Actualizado'}).encode('utf-8'), headers={'Content-Type':'application/json','Authorization':f'Bearer {access}'}, method='PUT')
            with urllib.request.urlopen(req, timeout=15) as r:
                print(r.getcode(), r.read().decode('utf-8'))
        except Exception as e2:
            print('Error real PUT:', e2)

    print(f"\n5) GET /beneficios/{codigo} after update")
    try:
        c, b = get_with_token(f'/beneficios/{codigo}', access)
        print(c, b)
    except Exception as e:
        print('Error final GET:', e)

if __name__ == '__main__':
    main()
