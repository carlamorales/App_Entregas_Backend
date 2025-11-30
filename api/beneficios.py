from flask import Blueprint, jsonify, request
from database import SessionLocal
from sqlalchemy import select
from flask import abort
from datetime import datetime

def create_beneficios_blueprint(require_perm):
    bp = Blueprint('beneficios', __name__, url_prefix='/beneficios')

    @bp.get('/')
    @require_perm('beneficios.read')
    def list_beneficios():
        db = SessionLocal()
        try:
            from models import Beneficio
            rows = db.execute(select(Beneficio)).scalars().all()
            items = []
            for r in rows:
                items.append({
                    'codigo': getattr(r, 'codigo', None),
                    'nombre_beneficio': getattr(r, 'nombre_beneficio', None),
                })
            return jsonify(items)
        finally:
            db.close()

    

    @bp.get('/<string:codigo>')
    @require_perm('beneficios.read')
    def get_beneficio(codigo):
        db = SessionLocal()
        try:
            from models import Beneficio
            obj = db.execute(select(Beneficio).where(Beneficio.codigo == codigo)).scalar_one_or_none()
            if not obj:
                return abort(404)
            return jsonify({
                'codigo': obj.codigo,
                'nombre_beneficio': obj.nombre_beneficio,
                'descripcion': getattr(obj, 'descripcion', None),
                'activo': bool(obj.activo)
            })
        finally:
            db.close()

    @bp.post('/')
    @require_perm('beneficios.create')
    def create_beneficio():
        data = request.get_json(force=True)
        codigo = data.get('codigo')
        nombre = data.get('nombre_beneficio')
        descripcion = data.get('descripcion')
        activo = data.get('activo', True)
        if not codigo or not nombre:
            return jsonify({'error': 'codigo y nombre_beneficio requeridos'}), 400
        db = SessionLocal()
        try:
            from models import Beneficio
            b = Beneficio(codigo=codigo, nombre_beneficio=nombre, descripcion=descripcion, activo=bool(activo))
            db.add(b)
            db.commit()
            return jsonify({'ok': True, 'codigo': b.codigo}), 201
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    @bp.put('/<string:codigo>')
    @require_perm('beneficios.update')
    def update_beneficio(codigo):
        data = request.get_json(force=True)
        db = SessionLocal()
        try:
            from models import Beneficio
            b = db.execute(select(Beneficio).where(Beneficio.codigo == codigo)).scalar_one_or_none()
            if not b:
                return abort(404)
            if 'nombre_beneficio' in data:
                b.nombre_beneficio = data.get('nombre_beneficio')
            if 'descripcion' in data:
                b.descripcion = data.get('descripcion')
            if 'activo' in data:
                b.activo = bool(data.get('activo'))
            db.commit()
            return jsonify({'ok': True, 'codigo': b.codigo}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
    return bp
