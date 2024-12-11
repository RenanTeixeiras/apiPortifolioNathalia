from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel


class Trajetoria(Base):
    __tablename__ = "trajetoria"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)

# Esquema para entrada e saída de dados (Pydantic)
class TrajetoriaCreate(BaseModel):
    data: str
    titulo: str
    descricao: str

class TrajetoriaSchema(TrajetoriaCreate):
    id: int

    class Config:
        orm_mode = True

