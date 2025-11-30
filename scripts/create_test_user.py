import os
import sys
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import SessionLocal
from models import Usuario

def main():
    username = os.getenv('TEST_USER', 'test_admin')
    password = os.getenv('TEST_PASS', 'Test1234!')
    role = os.getenv('TEST_ROLE', 'admin')

    db = SessionLocal()
    try:
        user = db.query(Usuario).filter(Usuario.usuario == username).one_or_none()
        if user:
            print(f"Usuario existente '{username}' encontrado. Actualizando password y rol.")
            user.contrasenaHash = generate_password_hash(password)
            user.rol = role
        else:
            print(f"Creando usuario '{username}' con rol '{role}'")
            user = Usuario(usuario=username, contrasenaHash=generate_password_hash(password), rol=role)
            db.add(user)
        db.commit()
        print('Hecho. Credenciales:')
        print('  usuario:', username)
        print('  contrasena:', password)
        print('  rol:', role)
    except Exception as e:
        db.rollback()
        print('Error creando usuario:', e)
    finally:
        db.close()

if __name__ == '__main__':
    main()
