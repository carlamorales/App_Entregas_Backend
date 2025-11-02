import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import pyodbc

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_ENCRYPT = os.getenv("DB_ENCRYPT", "yes")
DB_TRUST = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes")

if not all([DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD]):
    raise RuntimeError("❌ Faltan datos en .env (DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD)")

# Selección del driver disponible
PREFERRED = ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"]
installed = set(pyodbc.drivers())
driver = next((d for d in PREFERRED if d in installed), None)
if not driver:
    raise RuntimeError(f"❌ No se encontró un driver ODBC SQL Server compatible. Instalados: {sorted(installed)}")

# Construye cadena ODBC sin DSN y codificada
odbc_raw = (
    f"DRIVER={{{driver}}};"
    f"SERVER={DB_SERVER},{DB_PORT};"
    f"DATABASE={DB_DATABASE};"
    f"UID={DB_USERNAME};PWD={DB_PASSWORD};"
    f"Encrypt={DB_ENCRYPT};TrustServerCertificate={DB_TRUST};"
)
conn_str = f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_raw)}"

engine = create_engine(conn_str, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
