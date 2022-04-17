
import os
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from vitemaprog.env import load_env
from vitemaprog.exeptions import ModelNotFoundException, ConfigurationException

load_env()

__all__ = ["DB"]


class DB:
    # Définition pour le singleton
    __instance = None
    # Optimisation chargement des attributs
    __slots__ = ('_db_driver', '_db_name', '_db_user', '_db_pass',
                 '_db_host', '_db_port', '_db_url', '_db_engine')

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    # Intentiation
    def __init__(self):
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
    def db_url(self):
        return self._db_url

    @property
    def db_engine(self):
        return self._db_engine


# Session local pour la base de données
SessionLocal = sessionmaker(bind=DB().db_engine)


class Base(declarative_base()):
    __abstract__ = True

    __session__ = None

    def to_json(self):
        if(self.__model_out__ is None):
            raise ConfigurationException(f'Model output is not set for {self.__class__.__name__}')

        return self.__class__.__model_out__(**self.__dict__)

    def delete(self):
        session = self.__class__.get_session()
        session.delete(self)
        session.commit()
        session.close()

    def update(self, obj):
        session = self.__class__.get_session()
        self.fill(obj)
        session.commit()

    def fill(self, obj):
        # Fill only the fields that are not None or required
        for model_field in obj.__fields__.values():
            value = getattr(obj, model_field.name)
            if(model_field.required or value is not None):
                setattr(self, model_field.name, value)

    @classmethod
    def get_session(cls):
        if(cls.__session__ is None):
            cls.__session__ = SessionLocal()
        return cls.__session__

    @classmethod
    def query(cls):
        return cls.get_session().query(cls)

    @classmethod
    def all(cls, serialize=True):
        return [ item_bdd.to_json() if serialize else item_bdd for item_bdd in cls.query().all()]

    @classmethod
    def find(cls, uuid, serialize=True, raise_exception=False):
        obj = cls.query().filter(cls.uuid == uuid).first()
        if(obj):
            if(serialize):
                return obj.to_json()
            else:
                return obj
        else:
            if(raise_exception):
                raise ModelNotFoundException(f'{cls.__name__} not found')
            else:
                return None

    @classmethod
    def create(cls, obj: BaseModel):
        session = cls.get_session()

        # Création de l'instance
        instance = cls(**obj.__dict__)

        # persistance de l'instance
        session.add(instance)
        session.commit()

        return instance.to_json()
