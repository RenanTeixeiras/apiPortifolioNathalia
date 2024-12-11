from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel



class Habilidades(Base):
    __tablename__ = "habilidades"

    id = Column(Integer, primary_key=True, index=True)
    foto = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    nivel = Column(String, nullable=False)

# Esquema para entrada e saída de dados (Pydantic)
class HabilidadesCreate(BaseModel):
    foto: str
    titulo: str
    nivel: str

class HabilidadesSchema(HabilidadesCreate):
    id: int

    class Config:
        orm_mode = True

