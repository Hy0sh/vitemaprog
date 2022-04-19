import os
from fastapi import FastAPI, Request
from vitemaprog.database.db import DB
from vitemaprog.routers import api_router
from vitemaprog.env import load_env
from vitemaprog import __version__, __description__, __name__

# Chargement des variables d'environnement
load_env()

# Création de l'application
app=FastAPI(debug=os.getenv("MODE")=="development", title=__name__, description=__description__, version=__version__)

# Renouvellement de la session à chaque requête
@app.middleware("http")
async def close_and_renew_session(request: Request, call_next):
    response = await call_next(request)
    DB().db.close_all()
    DB().renew_session()
    return response

# Ajout des routes
app.include_router(api_router, prefix="/api")
