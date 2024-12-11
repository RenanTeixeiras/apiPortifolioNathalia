from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuarios import Usuarios, UsuariosCreate, UsuariosSchema, UsuariosLoginCreate, UsuariosLoginSchema
from app.utils.auth import hash_password, verify_password, create_access_token
from app.database import get_db
from app.utils.auth import get_current_user

router = APIRouter()

from fastapi import Depends

@router.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}






@router.post("/cadastro", response_model=UsuariosSchema)
def register_user(user: UsuariosCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está registrado
    if db.query(Usuarios).filter(Usuarios.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso",
        )
    
    # Cria e salva o usuário no banco
    hashed_password = hash_password(user.senha)
    new_user = Usuarios(nome=user.nome, email=user.email, senha=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user: UsuariosLoginCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    db_user = db.query(Usuarios).filter(Usuarios.email == user.email).first()
    if not db_user or not verify_password(user.senha, db_user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Cria o token JWT
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
