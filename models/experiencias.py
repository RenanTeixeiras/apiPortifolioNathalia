from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel

class Experiencias(Base):
    __tablename__ = "experiencias"

    id = Column(Integer, primary_key=True, index=True)
    foto = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    data_entrada = Column(String, nullable=False)
    data_saida = Column(String, nullable=True)

# Esquema para entrada e saída de dados (Pydantic)
class ExperienciasCreate(BaseModel):
    foto: str
    titulo: str
    data_entrada: str
    data_saida: str
    
class ExperienciasSchema(ExperienciasCreate):
    id: int
    class Config:
        orm_mode = True

