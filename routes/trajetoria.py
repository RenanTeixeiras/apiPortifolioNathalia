from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trajetoria import Trajetoria as TrajetoriaModel, TrajetoriaCreate, TrajetoriaSchema
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[TrajetoriaSchema])
async def listar_trajetoria(db: Session = Depends(get_db)):
    return db.query(TrajetoriaModel).all()

@router.get("/{trajetoria_id}", response_model=TrajetoriaSchema)
async def obter_trajetoria(trajetoria_id: int, db: Session = Depends(get_db)):
    trajetoria = db.query(TrajetoriaModel).filter(TrajetoriaModel.id == trajetoria_id).first()
    if not trajetoria:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    return trajetoria

@router.post("/", response_model=TrajetoriaSchema)
async def adicionar_trajetoria(trajetoria: TrajetoriaCreate, db: Session = Depends(get_db)):
    if not trajetoria.data or not trajetoria.titulo or not trajetoria.descricao:
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
    novo_trajetoria = TrajetoriaModel(**trajetoria.dict())
    db.add(novo_trajetoria)
    db.commit()
    db.refresh(novo_trajetoria)
    return novo_trajetoria

@router.put("/{trajetoria_id}", response_model=TrajetoriaSchema)
async def atualizar_trajetoria(
    trajetoria_id: int, 
    trajetoria: TrajetoriaCreate, 
    db: Session = Depends(get_db)
):
    # Verifica se o registro existe
    trajetoria_existente = db.query(TrajetoriaModel).filter(TrajetoriaModel.id == trajetoria_id).first()
    if not trajetoria_existente:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    
    # Atualiza os campos
    for key, value in trajetoria.dict().items():
        if not value:
            raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
        setattr(trajetoria_existente, key, value)
    
    db.commit()
    db.refresh(trajetoria_existente)  # Atualiza o estado do objeto com os valores do banco
    return trajetoria_existente


@router.delete("/{trajetoria_id}")
async def deletar_trajetoria(trajetoria_id: int, db: Session = Depends(get_db)):
    trajetoria = db.query(TrajetoriaModel).filter(TrajetoriaModel.id == trajetoria_id).first()
    if not trajetoria:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    db.delete(trajetoria)
    db.commit()
    return {"detail": "Informação removida com sucesso"}