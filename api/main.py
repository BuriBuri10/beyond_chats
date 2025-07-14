from fastapi import FastAPI
from api.routes import persona

app = FastAPI()
app.include_router(persona.router, prefix="/api", tags=["Persona"])
