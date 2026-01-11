from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import analyzer

# Crear instancia de FastAPI
app = FastAPI(
    title="CV Analyzer API",
    description="API para analizar compatibilidad entre CVs y ofertas de trabajo",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(analyzer.router, prefix="/api", tags=["analyzer"])

# Ruta de bienvenida
@app.get("/")
async def root():
    return {
        "message": "CV Analyzer API",
        "status": "running",
        "version": "1.0.0"
    }