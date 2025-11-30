from flask import Blueprint, jsonify, request
from database import SessionLocal
from sqlalchemy import select
from flask import abort

def create_sucursales_blueprint(require_perm):
    bp = Blueprint('sucursales', __name__, url_prefix='/sucursales')

    @bp.get('/')
    @require_perm('sucursales.read')
    def list_sucursales():
        db = SessionLocal()
        try:
            from models import Sucursal
            rows = db.execute(select(Sucursal)).scalars().all()
            items = []
            for r in rows:
                items.append({
                    'codigo': getattr(r, 'codigo', None),
                    'nombre_sucursal': getattr(r, 'nombre_sucursal', None),
                })
            return jsonify(items)
        finally:
            db.close()

    

    @bp.get('/<string:codigo>')
    @require_perm('sucursales.read')
    def get_sucursal(codigo):
        db = SessionLocal()
        try:
            from models import Sucursal
            s = db.execute(select(Sucursal).where(Sucursal.codigo == codigo)).scalar_one_or_none()
            if not s:
                return abort(404)
            return jsonify({
                'codigo': s.codigo,
                'nombre_sucursal': s.nombre_sucursal,
                'direccion': s.direccion,
                'telefono': s.telefono
            })
        finally:
            db.close()

    @bp.post('/')
    @require_perm('sucursales.create')
    def create_sucursal():
        data = request.get_json(force=True)
        codigo = data.get('codigo')
        nombre = data.get('nombre_sucursal')
        if not codigo or not nombre:
            return jsonify({'error': 'codigo y nombre_sucursal requeridos'}), 400
        db = SessionLocal()
        try:
            from models import Sucursal
            s = Sucursal(codigo=codigo, nombre_sucursal=nombre, direccion=data.get('direccion'), telefono=data.get('telefono'))
            db.add(s)
            db.commit()
            return jsonify({'ok': True, 'codigo': s.codigo}), 201
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    @bp.put('/<string:codigo>')
    @require_perm('sucursales.update')
    def update_sucursal(codigo):
        data = request.get_json(force=True)
        db = SessionLocal()
        try:
            from models import Sucursal
            s = db.execute(select(Sucursal).where(Sucursal.codigo == codigo)).scalar_one_or_none()
            if not s:
                return abort(404)
            for fld in ('nombre_sucursal','direccion','telefono'):
                if fld in data:
                    setattr(s, fld, data.get(fld))
            db.commit()
            return jsonify({'ok': True, 'codigo': s.codigo}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    return bp
