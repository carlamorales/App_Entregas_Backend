from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Date, DateTime, BigInteger, Text, ForeignKey, CheckConstraint
from datetime import datetime


Base = declarative_base()


class Periodo(Base):
    __tablename__ = "Periodos"
    Codigo = Column(String(20), primary_key=True)
    FechaInicio = Column(Date, nullable=False)
    FechaFinal = Column(Date, nullable=False)
    __table_args__ = (
        CheckConstraint('FechaInicio <= FechaFinal', name='CHK_PeriodoRango'),
)


class Beneficio(Base):
    __tablename__ = "Beneficios"
    Codigo = Column(String(20), primary_key=True)
    NombreBeneficio = Column(String(120), nullable=False)


class Entrega(Base):
    __tablename__ = "Entregas"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Rut = Column(String(12), nullable=False)
    Nombre = Column(String(80), nullable=False)
    Apellido = Column(String(80), nullable=False)
    Correo = Column(String(120), nullable=False)
    FechaEntrega = Column(DateTime, nullable=True)
    Beneficio_cod = Column(String(20), ForeignKey('Beneficios.Codigo'), nullable=False)
    FirmaBase64 = Column(Text)
    Estado = Column(String(20), nullable=False, default='pendiente')
    Periodo_cod = Column(String(20), ForeignKey('Periodos.Codigo'), nullable=False)


class Usuario(Base):
    __tablename__ = "Usuarios"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Rol = Column(String(50), nullable=False)
    Usuario = Column(String(100), nullable=False, unique=True)
    ContrasenaHash = Column(String(256), nullable=False)