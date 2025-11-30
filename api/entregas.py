from flask import Blueprint, jsonify, request
from database import SessionLocal
from sqlalchemy import select
from flask import abort
from datetime import datetime

def create_entregas_blueprint(require_perm):
    bp = Blueprint('entregas', __name__, url_prefix='/entregas')

    @bp.get('/')
    @require_perm('entregas.read')
    def list_entregas():
        db = SessionLocal()
        try:
            from models import Entrega
            rows = db.execute(select(Entrega)).scalars().all()
            items = []
            for r in rows:
                items.append({
                    'ID': getattr(r, 'ID', None),
                    'Trabajador_Rut': getattr(r, 'Rut', None),
                    'Beneficio_cod': getattr(r, 'Beneficio_cod', None),
                    'Estado': getattr(r, 'Estado', None),
                })
            return jsonify(items)
        finally:
            db.close()

    

    @bp.get('/<int:id>')
    @require_perm('entregas.read')
    def get_entrega(id):
        db = SessionLocal()
        try:
            from models import Entrega
            e = db.execute(select(Entrega).where(Entrega.ID == id)).scalar_one_or_none()
            if not e:
                return abort(404)
            return jsonify({
                'ID': e.ID,
                'Trabajador_Rut': getattr(e, 'Rut', None),
                'Beneficio_cod': getattr(e, 'Beneficio_cod', None),
                'Estado': getattr(e, 'Estado', None),
                'Periodo_cod': getattr(e, 'Periodo_cod', None),
                'CodSucursal': getattr(e, 'CodSucursal', None),
                'TipoContrato': getattr(e, 'TipoContrato', None),
            })
        finally:
            db.close()

    @bp.post('/')
    @require_perm('entregas.create')
    def create_entrega():
        data = request.get_json(force=True)
        rut = data.get('Rut') or data.get('trabajador_rut') or data.get('Trabajador_Rut')
        beneficio = data.get('Beneficio_cod') or data.get('beneficio_cod')
        estado = data.get('Estado', 'PENDIENTE')
        periodo = data.get('Periodo_cod') or data.get('periodo')
        sucursal = data.get('CodSucursal') or data.get('cod_sucursal')
        tipo = data.get('TipoContrato') or data.get('tipo_contrato')
        usuario_creador = data.get('Usuario_creador')
        fecha_entrega = data.get('FechaEntrega')
        if not rut or not beneficio:
            return jsonify({'error': 'Rut y Beneficio_cod son requeridos'}), 400
        if fecha_entrega:
            try:
                fecha = datetime.fromisoformat(fecha_entrega)
            except Exception:
                return jsonify({'error': 'FechaEntrega en formato ISO requerido'}), 400
        else:
            fecha = datetime.utcnow()
        db = SessionLocal()
        try:
            from models import Entrega
            e = Entrega(Rut=rut, FechaEntrega=fecha, Beneficio_cod=beneficio, Estado=estado, Periodo_cod=periodo, CodSucursal=sucursal, TipoContrato=tipo, Usuario_creador=usuario_creador)
            db.add(e)
            db.commit()
            return jsonify({'ok': True, 'ID': e.ID}), 201
        except Exception as ex:
            db.rollback()
            return jsonify({'error': str(ex)}), 500
        finally:
            db.close()

    @bp.put('/<int:id>')
    @require_perm('entregas.update')
    def update_entrega(id):
        data = request.get_json(force=True)
        db = SessionLocal()
        try:
            from models import Entrega
            e = db.execute(select(Entrega).where(Entrega.ID == id)).scalar_one_or_none()
            if not e:
                return abort(404)
            for field, attr in (('Estado','Estado'), ('Periodo_cod','Periodo_cod'), ('CodSucursal','CodSucursal'), ('TipoContrato','TipoContrato')):
                if field in data:
                    setattr(e, attr, data.get(field))
            db.commit()
            return jsonify({'ok': True, 'ID': e.ID}), 200
        except Exception as ex:
            db.rollback()
            return jsonify({'error': str(ex)}), 500
        finally:
            db.close()

    return bp
