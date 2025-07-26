from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=False)

