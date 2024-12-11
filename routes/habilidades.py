from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.habilidades import Habilidades as HabilidadesModel, HabilidadesCreate, HabilidadesSchema
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[HabilidadesSchema])
async def listar_habilidades(db: Session = Depends(get_db)):
    return db.query(HabilidadesModel).all()

@router.get("/{habilidades_id}", response_model=HabilidadesSchema)
async def obter_habilidades(habilidades_id: int, db: Session = Depends(get_db)):
    habilidades = db.query(HabilidadesModel).filter(HabilidadesModel.id == habilidades_id).first()
    if not habilidades:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    return habilidades

@router.post("/", response_model=HabilidadesSchema)
async def adicionar_habilidades(habilidades: HabilidadesCreate, db: Session = Depends(get_db)):
    if habilidades.nivel not in ['Básico', 'Intermediário', 'Avançado', 'Especialista']:
        raise HTTPException(status_code=400, detail="Campo nível deve ser preenchido com 'Básico', 'Intermediário', 'Avançado' ou 'Especialista'.")
    if not habilidades.foto or not habilidades.titulo or not habilidades.nivel:
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
    novo_habilidades = HabilidadesModel(**habilidades.dict())
    db.add(novo_habilidades)
    db.commit()
    db.refresh(novo_habilidades)
    return novo_habilidades

@router.put("/{habilidades_id}", response_model=HabilidadesSchema)
async def atualizar_habilidades(
    habilidades_id: int, 
    habilidades: HabilidadesCreate, 
    db: Session = Depends(get_db)
):
    # Verifica se o registro existe
    habilidades_existente = db.query(HabilidadesModel).filter(HabilidadesModel.id == habilidades_id).first()
    if not habilidades_existente:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    
    if habilidades.nivel not in ['Básico', 'Intermediário', 'Avançado', 'Especialista']:
        raise HTTPException(status_code=400, detail="Campo nível deve ser preenchido com 'Básico', 'Intermediário', 'Avançado' ou 'Especialista'.")

    # Atualiza os campos
    for key, value in habilidades.dict().items():
        if not value:
            raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
        setattr(habilidades_existente, key, value)
    
    db.commit()
    db.refresh(habilidades_existente)  # Atualiza o estado do objeto com os valores do banco
    return habilidades_existente


@router.delete("/{habilidades_id}")
async def deletar_habilidades(habilidades_id: int, db: Session = Depends(get_db)):
    habilidades = db.query(HabilidadesModel).filter(HabilidadesModel.id == habilidades_id).first()
    if not habilidades:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    db.delete(habilidades)
    db.commit()
    return {"detail": "Informação removida com sucesso"}