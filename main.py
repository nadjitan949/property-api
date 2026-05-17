from fastapi import FastAPI
from app.database.database import Base, engine
from app.model.users import User
from app.model.properties import Property
from app.api.users import router as user_router
from app.api.auth import router as auth_router
from app.api.properties import router as property_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mon API Immobilière",
    description="Gestion des utilisateurs et des biens",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(property_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Immobilière ! Accédez à /docs pour voir la documentation."}