from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trajetoria_fotos import TrajetoriaFotos as TrajetoriaFotosModel, TrajetoriaFotosCreate, TrajetoriaFotosSchema
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[TrajetoriaFotosSchema])
async def listar_trajetoria(db: Session = Depends(get_db)):
    return db.query(TrajetoriaFotosModel).all()


@router.post("/", response_model=TrajetoriaFotosSchema)
async def adicionar_trajetoria(trajetoria: TrajetoriaFotosCreate, db: Session = Depends(get_db)):
    if not trajetoria.foto:
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
    novo_trajetoria = TrajetoriaFotosModel(**trajetoria.dict())
    db.add(novo_trajetoria)
    db.commit()
    db.refresh(novo_trajetoria)
    return novo_trajetoria

@router.put("/{trajetoria_id}", response_model=TrajetoriaFotosSchema)
async def atualizar_trajetoria(
    trajetoria_id: int, 
    trajetoria: TrajetoriaFotosCreate, 
    db: Session = Depends(get_db)
):
    # Verifica se o registro existe
    trajetoria_existente = db.query(TrajetoriaFotosModel).filter(TrajetoriaFotosModel.id == trajetoria_id).first()
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
    trajetoria = db.query(TrajetoriaFotosModel).filter(TrajetoriaFotosModel.id == trajetoria_id).first()
    if not trajetoria:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    db.delete(trajetoria)
    db.commit()
    return {"detail": "Informação removida com sucesso"}