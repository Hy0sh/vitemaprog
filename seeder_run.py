#!/usr/bin/env python3

"""
    Ce fichier permet de lancer les seeders souhaités.
    ex: ./seeder_run.py RightSeeder RoleSeeder
"""
import sys
from pathlib import Path

# On récupère le chemin du dossier parent pour pouvoir ajouter le dossier vitemaprog au path
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

import vitemaprog.database.seeders as seeders

for arg in sys.argv[1::]:
    try:
        cls = getattr(seeders, arg)
        if(not issubclass(cls, seeders.SeederInterface)):
            raise Exception("La classe {} n'est pas une classe de seeders".format(arg))
        else:
            print("Lancement du seeder {}".format(arg))
            cls.run()
    except AttributeError:
        print("Seeder inconnu: {}".format(arg))
        continue
    except Exception as e:
        print(e)
        continue
