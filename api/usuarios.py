from flask import Blueprint, jsonify, request
from database import SessionLocal
from sqlalchemy import select
from werkzeug.security import generate_password_hash
from flask import abort

def create_usuarios_blueprint(require_perm):
    bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

    @bp.get('/')
    @require_perm('usuarios.read')
    def list_usuarios():
        db = SessionLocal()
        try:
            from models import Usuario
            rows = db.execute(select(Usuario)).scalars().all()
            items = []
            for r in rows:
                items.append({
                    'ID': getattr(r, 'ID', None),
                    'usuario': getattr(r, 'usuario', None),
                    'rol': getattr(r, 'rol', None),
                })
            return jsonify(items)
        finally:
            db.close()

    @bp.post('/')
    @require_perm('usuarios.create')
    def create_usuario():
        data = request.get_json(force=True)
        username = data.get('usuario')
        password = data.get('contrasena')
        rol = data.get('rol', 'operador')
        if not username or not password:
            return jsonify({'error': 'usuario y contrasena requeridos'}), 400
        db = SessionLocal()
        try:
            from models import Usuario
            u = Usuario(usuario=username, contrasenaHash=generate_password_hash(password), rol=rol)
            db.add(u)
            db.commit()
            return jsonify({'ok': True, 'id': getattr(u, 'ID', None)}), 201
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    

    @bp.get('/<int:id>')
    @require_perm('usuarios.read')
    def get_usuario(id):
        db = SessionLocal()
        try:
            from models import Usuario
            u = db.execute(select(Usuario).where(Usuario.ID == id)).scalar_one_or_none()
            if not u:
                return ('', 404)
            return jsonify({
                'ID': u.ID,
                'usuario': u.usuario,
                'rol': u.rol,
                'email': u.email,
                'activo': bool(u.activo)
            })
        finally:
            db.close()

    @bp.put('/<int:id>')
    @require_perm('usuarios.update')
    def update_usuario(id):
        data = request.get_json(force=True)
        db = SessionLocal()
        try:
            from models import Usuario
            u = db.execute(select(Usuario).where(Usuario.ID == id)).scalar_one_or_none()
            if not u:
                return ('', 404)
            if 'usuario' in data:
                u.usuario = data.get('usuario')
            if 'rol' in data:
                u.rol = data.get('rol')
            if 'email' in data:
                u.email = data.get('email')
            if 'activo' in data:
                u.activo = bool(data.get('activo'))
            if 'contrasena' in data:
                u.contrasenaHash = generate_password_hash(data.get('contrasena'))
            db.commit()
            return jsonify({'ok': True, 'ID': u.ID}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    return bp
