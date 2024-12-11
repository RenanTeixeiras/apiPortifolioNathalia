from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel



class Projetos(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    link = Column(String, nullable=False)

# Esquema para entrada e saída de dados (Pydantic)
class ProjetosCreate(BaseModel):
    titulo: str
    descricao: str
    link: str

class ProjetosSchema(ProjetosCreate):
    id: int

    class Config:
        orm_mode = True

