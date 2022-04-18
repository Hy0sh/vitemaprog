
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from vitemaprog.exeptions import ModelNotFoundException, ConfigurationException
from vitemaprog.database.db import SessionLocal
from sqlalchemy.orm import declarative_base

class BaseModel(declarative_base()):
    __abstract__ = True

    __session__ = None

    # Sérialise l'objet en JSON
    def to_json(self) -> dict:
        if(self.__model_out__ is None):
            raise ConfigurationException(f'Model output is not set for {self.__class__.__name__}')

        self.refresh()

        return self.__class__.__model_out__(**self.__dict__)

    # Rafraichissement des données au prêt de la base de données
    def refresh(self) -> None:
        session = self.__class__.get_session()
        session.refresh(self)

    # Supprime l'objet de la base de données
    def delete(self) -> None:
        session = self.__class__.get_session()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # Met à jour l'objet dans la base de données
    def update(self, obj: PydanticBaseModel) -> None:
        self.fill(obj)
        self.save()

    # Sauvegarde l'objet dans la base de données
    def save(self) -> None:
        self.updated_at = datetime.utcnow()
        session = self.__class__.get_session()
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    # Assigne les valeurs de l'objet pydantic à l'instance
    def fill(self, obj: PydanticBaseModel) -> None:
        # Fill only the fields that are not None or required
        for model_field in obj.__fields__.values():
            value = getattr(obj, model_field.name)
            if(model_field.required or value is not None):
                setattr(self, model_field.name, value)

    # Retourne la session de la base de données
    @classmethod
    def get_session(cls) -> SessionLocal:
        if(cls.__session__ is None):
            cls.__session__ = SessionLocal()
        return cls.__session__

    # Retourne la query de l'instance
    @classmethod
    def query(cls):
        return cls.get_session().query(cls)

    # Renvoie tous les enregistrements de la base de données
    @classmethod
    def all(cls, serialize=True) -> list:
        return [ item_bdd.to_json() if serialize else item_bdd for item_bdd in cls.query().all()]

    # Renvoie l'enregistrement de la base de données correspondant à l'uuid
    @classmethod
    def find(cls, uuid, serialize=True, raise_exception=False) -> 'BaseModel':
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

    # Créé un nouvel enregistrement dans la base de données
    @classmethod
    def create(cls, obj: PydanticBaseModel) -> 'BaseModel':
        session = cls.get_session()

        # Création de l'instance
        instance = cls(**obj.__dict__)

        # persistance de l'instance
        try:
            session.add(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return instance
