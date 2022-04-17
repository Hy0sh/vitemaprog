import os
from fastapi import FastAPI
from vitemaprog.routers import api_router
from vitemaprog.env import load_env
from vitemaprog import __version__, __description__, __name__

# Chargement des variables d'environnement
load_env()

# Création de l'application
app=FastAPI(debug=os.getenv("MODE")=="development", title=__name__, description=__description__, version=__version__)

# Ajout des routes
app.include_router(api_router, prefix="/api")
