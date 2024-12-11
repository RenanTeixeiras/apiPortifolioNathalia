from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel


class TrajetoriaFotos(Base):
    __tablename__ = "trajetoria_fotos"

    id = Column(Integer, primary_key=True, index=True)
    foto = Column(String, nullable=False)

# Esquema para entrada e saída de dados (Pydantic)
class TrajetoriaFotosCreate(BaseModel):
    foto: str

class TrajetoriaFotosSchema(TrajetoriaFotosCreate):
    id: int

    class Config:
        orm_mode = True

