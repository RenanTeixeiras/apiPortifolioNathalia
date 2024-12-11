from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sobre import Sobre as SobreModel, SobreCreate, SobreSchema
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[SobreSchema])
async def listar_sobre(db: Session = Depends(get_db)):
    return db.query(SobreModel).all()

@router.post("/", response_model=SobreSchema)
async def adicionar_sobre(sobre: SobreCreate, db: Session = Depends(get_db)):
    if not sobre.foto or not sobre.titulo or not sobre.descricao:
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
    novo_sobre = SobreModel(**sobre.dict())
    db.add(novo_sobre)
    db.commit()
    db.refresh(novo_sobre)
    return novo_sobre

@router.put("/{sobre_id}", response_model=SobreSchema)
async def atualizar_sobre(
    sobre_id: int, 
    sobre: SobreCreate, 
    db: Session = Depends(get_db)
):
    # Verifica se o registro existe
    sobre_existente = db.query(SobreModel).filter(SobreModel.id == sobre_id).first()
    if not sobre_existente:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    
    # Atualiza os campos
    for key, value in sobre.dict().items():
        if not value:
            raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
        setattr(sobre_existente, key, value)
    
    db.commit()
    db.refresh(sobre_existente)  # Atualiza o estado do objeto com os valores do banco
    return sobre_existente


@router.delete("/{sobre_id}")
async def deletar_sobre(sobre_id: int, db: Session = Depends(get_db)):
    sobre = db.query(SobreModel).filter(SobreModel.id == sobre_id).first()
    if not sobre:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    db.delete(sobre)
    db.commit()
    return {"detail": "Informação removida com sucesso"}