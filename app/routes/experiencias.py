from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.experiencias import Experiencias as ExperienciasModel, ExperienciasCreate, ExperienciasSchema
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[ExperienciasSchema])
async def listar_experiencias(db: Session = Depends(get_db)):
    return db.query(ExperienciasModel).all()

@router.get("/{experiencias_id}", response_model=ExperienciasSchema)
async def obter_experiencias(experiencias_id: int, db: Session = Depends(get_db)):
    experiencias = db.query(ExperienciasModel).filter(ExperienciasModel.id == experiencias_id).first()
    if not experiencias:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    return experiencias

@router.post("/", response_model=ExperienciasSchema)
async def adicionar_experiencias(experiencias: ExperienciasCreate, db: Session = Depends(get_db)):
  
    if not experiencias.foto or not experiencias.titulo or not experiencias.data_entrada:
        raise HTTPException(status_code=400, detail=f"Todos os campos, exceto data_saida são obrigatórios.")
    novo_experiencias = ExperienciasModel(**experiencias.dict())
    db.add(novo_experiencias)
    db.commit()
    db.refresh(novo_experiencias)
    return novo_experiencias

@router.put("/{experiencias_id}", response_model=ExperienciasSchema)
async def atualizar_experiencias(
    experiencias_id: int, 
    experiencias: ExperienciasCreate, 
    db: Session = Depends(get_db)
):
    # Verifica se o registro existe
    experiencias_existente = db.query(ExperienciasModel).filter(ExperienciasModel.id == experiencias_id).first()
    if not experiencias_existente:
        raise HTTPException(status_code=404, detail="Informação não encontrada")

    # Atualiza os campos
    for key, value in experiencias.dict().items():
        if not value:
            raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
        setattr(experiencias_existente, key, value)
    
    db.commit()
    db.refresh(experiencias_existente)  # Atualiza o estado do objeto com os valores do banco
    return experiencias_existente


@router.delete("/{experiencias_id}")
async def deletar_experiencias(experiencias_id: int, db: Session = Depends(get_db)):
    experiencias = db.query(ExperienciasModel).filter(ExperienciasModel.id == experiencias_id).first()
    if not experiencias:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    db.delete(experiencias)
    db.commit()
    return {"detail": "Informação removida com sucesso"}