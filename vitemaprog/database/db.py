
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vitemaprog.env import load_env
from vitemaprog.exeptions import  ConfigurationException

load_env()

__all__ = ["DB"]
class DB:
    # Définition pour le singleton
    __instance = None
    # Optimisation chargement des attributs
    __slots__ = ('_db_driver', '_db_name', '_db_user', '_db_pass',
                 '_db_host', '_db_port', '_db_url', '_db_engine')

    def __new__(cls) -> 'DB':
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    # Intentiation
    def __init__(self) -> None:
        self._db_driver = os.getenv('DB_DRIVER')
        self._db_name = os.getenv('DB_NAME')
        self._db_user = os.getenv('DB_USER')
        self._db_pass = os.getenv('DB_PASS')
        self._db_host = os.getenv('DB_HOST')
        self._db_port = os.getenv('DB_PORT')

        if(self._db_driver is None or self._db_name is None or self._db_user is None or self._db_pass is None or self._db_host is None or self._db_port is None):
            raise ConfigurationException('Database configuration is not set')

        self._db_url = f'{self._db_driver}://{self._db_user}:{self._db_pass}@{self._db_host}:{self._db_port}/{self._db_name}'
        self._db_engine = create_engine(self.db_url)

    @property
    def db_url(self) -> str:
        return self._db_url

    @property
    def db_engine(self) -> 'create_engine':
        return self._db_engine

# Session local pour la base de données
SessionLocal = sessionmaker(bind=DB().db_engine)

