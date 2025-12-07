# Flask + Azure SQL (SQL Server)


### 1) Requisitos del sistema
- Python 3.10+
- Driver **ODBC Driver 18 for SQL Server** instalado en el sistema (Windows / Linux / Mac via Homebrew para ARM con Rosetta + unixODBC)
- Acceso a Azure SQL (puerto 1433 habilitado y firewall permitido para tu IP o red)


### 2) Instalación
```bash
python -m venv .venv
source .venv/bin/activate # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus credenciales de Azure SQL
```


### 3) Ejecutar en desarrollo
```bash
python app.py
# Servirá en http://localhost:8000
```


### 4) Endpoints
- `GET /health` → estado de la app y conexión
- `GET /beneficios` | `POST /beneficios`
- `GET /periodos`
- `GET /entregas` filtros: `rut, periodo, beneficio, estado, desde, hasta, page, size`
- `GET /entregas/<id>`
- `POST /entregas` (body JSON: `rut, nombre, apellido, beneficio_cod, periodo_cod, firma_base64?`)
- `PATCH /entregas/<id>` (body JSON: `estado?, firma_base64?`)
- `POST /entregas/importar` (multipart/form-data con `file` en .csv o .xlsx; columnas soportadas: `rut`, `beneficio_cod`, `periodo`, `cod_sucursal`, `tipo_contrato`, `estado`, `fecha_entrega`, `usuario_creador`)
- `GET /reportes/entregas-por-beneficio?periodo=2025-10`


### 5) Notas
- **Firmas en Base64**: guardadas tal cual en `FirmaBase64`. Si prefieres almacenar solo el payload, limpia el prefijo `data:*;base64,` en la app.
- **RUT**: validación simple por regex (puedes reemplazar por una validación con dígito verificador si lo necesitas).
- **Migraciones**: como ya creaste las tablas en SQL Server, los modelos solo mapean; no hace falta ejecutar `Base.metadata.create_all`. Si cambias columnas, usa scripts T-SQL y actualiza los modelos.
- **Prod**: usa un servidor WSGI (gunicorn + gevent/uvicorn workers) o Azure App Service con `startup command`. Configura `DEBUG=False` y variables de entorno seguras.
