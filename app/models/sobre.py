from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel

class Sobre(Base):
    __tablename__ = "sobre"

    id = Column(Integer, primary_key=True, index=True)
    foto = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)

# Esquema para entrada e saída de dados (Pydantic)
class SobreCreate(BaseModel):
    foto: str
    titulo: str
    descricao: str

class SobreSchema(SobreCreate):
    id: int

    class Config:
        orm_mode = True

