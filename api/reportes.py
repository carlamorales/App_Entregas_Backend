from flask import Blueprint, jsonify, request
from database import SessionLocal
from sqlalchemy import select, func

def create_reportes_blueprint(require_perm):
    bp = Blueprint('reportes', __name__, url_prefix='/reportes')

    @bp.get('/entregas-por-beneficio')
    @require_perm('reportes.read')
    def reporte_entregas_por_beneficio():
        db = SessionLocal()
        periodo = request.args.get('periodo')
        if not periodo:
            return jsonify({"error": "Debe indicar ?periodo=CODIGO"}), 400

        try:
            from models import Entrega
            q = db.execute(
                select(
                    Entrega.Periodo_cod.label('periodo'),
                    Entrega.Beneficio_cod.label('beneficio'),
                    func.count().label('total'),
                    func.sum(func.iif(Entrega.Estado == 'ENTREGADO', 1, 0)).label('entregados'),
                    func.sum(func.iif(Entrega.Estado == 'PENDIENTE', 1, 0)).label('pendientes'),
                    func.sum(func.iif(Entrega.Estado == 'CANCELADO', 1, 0)).label('rechazados')
                ).where(Entrega.Periodo_cod == periodo)
                .group_by(Entrega.Periodo_cod, Entrega.Beneficio_cod)
                .order_by(Entrega.Beneficio_cod)
            )

            items = []
            for row in q.all():
                items.append({
                    "periodo": row.periodo,
                    "beneficio_cod": row.beneficio,
                    "total": int(row.total or 0),
                    "entregados": int(row.entregados or 0),
                    "pendientes": int(row.pendientes or 0),
                    "rechazados": int(row.rechazados or 0)
                })
            return jsonify(items)
        finally:
            db.close()

    return bp
