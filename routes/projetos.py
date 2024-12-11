from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.projetos import Projetos as ProjetosModel, ProjetosCreate, ProjetosSchema
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[ProjetosSchema])
async def listar_projetos(db: Session = Depends(get_db)):
    return db.query(ProjetosModel).all()

@router.get("/{projetos_id}", response_model=ProjetosSchema)
async def obter_projetos(projetos_id: int, db: Session = Depends(get_db)):
    projetos = db.query(ProjetosModel).filter(ProjetosModel.id == projetos_id).first()
    if not projetos:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    return projetos

@router.post("/", response_model=ProjetosSchema)
async def adicionar_projetos(projetos: ProjetosCreate, db: Session = Depends(get_db)):
    if not projetos.titulo or not projetos.descricao or not projetos.link:
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
    novo_projetos = ProjetosModel(**projetos.dict())
    db.add(novo_projetos)
    db.commit()
    db.refresh(novo_projetos)
    return novo_projetos

@router.put("/{projetos_id}", response_model=ProjetosSchema)
async def atualizar_projetos(
    projetos_id: int, 
    projetos: ProjetosCreate, 
    db: Session = Depends(get_db)
):
    # Verifica se o registro existe
    projetos_existente = db.query(ProjetosModel).filter(ProjetosModel.id == projetos_id).first()
    if not projetos_existente:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    
    # Atualiza os campos
    for key, value in projetos.dict().items():
        if not value:
            raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")
        setattr(projetos_existente, key, value)
    
    db.commit()
    db.refresh(projetos_existente)  # Atualiza o estado do objeto com os valores do banco
    return projetos_existente


@router.delete("/{projetos_id}")
async def deletar_projetos(projetos_id: int, db: Session = Depends(get_db)):
    projetos = db.query(ProjetosModel).filter(ProjetosModel.id == projetos_id).first()
    if not projetos:
        raise HTTPException(status_code=404, detail="Informação não encontrada")
    db.delete(projetos)
    db.commit()
    return {"detail": "Informação removida com sucesso"}