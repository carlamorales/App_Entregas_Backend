from flask import Blueprint, jsonify, request
from database import SessionLocal
from sqlalchemy import select
from flask import abort

def create_trabajadores_blueprint(require_perm):
    bp = Blueprint('trabajadores', __name__, url_prefix='/trabajadores')

    @bp.get('/')
    @require_perm('trabajadores.read')
    def list_trabajadores():
        db = SessionLocal()
        try:
            from models import Trabajador
            rows = db.execute(select(Trabajador)).scalars().all()
            items = []
            for r in rows:
                items.append({
                    'rut': getattr(r, 'rut', None),
                    'primer_nombre': getattr(r, 'primer_nombre', None),
                    'primer_apellido': getattr(r, 'primer_apellido', None),
                })
            return jsonify(items)
        finally:
            db.close()

    

    @bp.get('/<string:rut>')
    @require_perm('trabajadores.read')
    def get_trabajador(rut):
        db = SessionLocal()
        try:
            from models import Trabajador
            t = db.execute(select(Trabajador).where(Trabajador.rut == rut)).scalar_one_or_none()
            if not t:
                return abort(404)
            return jsonify({
                'rut': t.rut,
                'primer_nombre': t.primer_nombre,
                'segundo_nombre': t.segundo_nombre,
                'primer_apellido': t.primer_apellido,
                'segundo_apellido': t.segundo_apellido,
                'email': t.email,
                'cargo': t.cargo,
                'activo': bool(t.activo)
            })
        finally:
            db.close()

    @bp.post('/')
    @require_perm('trabajadores.create')
    def create_trabajador():
        data = request.get_json(force=True)
        rut = data.get('rut')
        primer = data.get('primer_nombre')
        primer_ap = data.get('primer_apellido')
        if not rut or not primer or not primer_ap:
            return jsonify({'error': 'rut, primer_nombre y primer_apellido son requeridos'}), 400
        db = SessionLocal()
        try:
            from models import Trabajador
            t = Trabajador(rut=rut, primer_nombre=primer, segundo_nombre=data.get('segundo_nombre'), primer_apellido=primer_ap, segundo_apellido=data.get('segundo_apellido'), email=data.get('email'), cargo=data.get('cargo'), activo=data.get('activo', True))
            db.add(t)
            db.commit()
            return jsonify({'ok': True, 'rut': t.rut}), 201
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    @bp.put('/<string:rut>')
    @require_perm('trabajadores.update')
    def update_trabajador(rut):
        data = request.get_json(force=True)
        db = SessionLocal()
        try:
            from models import Trabajador
            t = db.execute(select(Trabajador).where(Trabajador.rut == rut)).scalar_one_or_none()
            if not t:
                return abort(404)
            for fld in ('primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','email','cargo'):
                if fld in data:
                    setattr(t, fld, data.get(fld))
            if 'activo' in data:
                t.activo = bool(data.get('activo'))
            db.commit()
            return jsonify({'ok': True, 'rut': t.rut}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    return bp
