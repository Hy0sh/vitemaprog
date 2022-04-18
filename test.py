#!/usr/bin/env python3
import sys
from pathlib import Path

# On récupère le chemin du dossier parent pour pouvoir ajouter le dossier vitemaprog au path
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from vitemaprog.models.auth.user_model import UserModel

user_model = UserModel.query().first()

print(user_model.to_json())
