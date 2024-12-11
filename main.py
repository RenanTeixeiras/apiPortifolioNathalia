from fastapi import FastAPI
from app.routes.sobre import router as sobre_router
from app.routes.trajetoria import router as trajetoria_router
from app.routes.habilidades import router as habilidades_router
from app.routes.projetos import router as projetos_router
from app.routes.trajetoria_fotos import router as trajetoria_fotos_router
from app.routes.usuarios import router as usuarios_router
from app.database import engine
from app.models.sobre import Sobre

app = FastAPI()

# Criar as tabelas no banco de dados
Sobre.metadata.create_all(bind=engine)

# Registrar as rotas
app.include_router(sobre_router, prefix="/sobre", tags=["Sobre"])
app.include_router(trajetoria_router, prefix="/trajetoria", tags=["Trajetoria"])
app.include_router(habilidades_router, prefix="/habilidades", tags=["Habilidades"])
app.include_router(projetos_router, prefix="/projetos", tags=["projetos"])
app.include_router(trajetoria_fotos_router, prefix="/trajetoria_fotos", tags=["TrajetoriaFotos"])
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Portfólio!"}
