from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel


class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)

# Esquema para entrada e saída de dados (Pydantic)
class UsuariosCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuariosLoginCreate(BaseModel):
    email: str
    senha: str

class UsuariosLoginSchema(UsuariosLoginCreate):
    id: int

    class Config:
        orm_mode = True


class UsuariosSchema(UsuariosCreate):
    id: int

    class Config:
        orm_mode = True

