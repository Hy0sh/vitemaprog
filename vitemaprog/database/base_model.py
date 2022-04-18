
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from vitemaprog.exeptions import ModelNotFoundException, ConfigurationException
from vitemaprog.database.db import DB
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from vitemaprog.exeptions.model_already_exists_exception import ModelAlreadyExistsException

class BaseModel(declarative_base()):
    __abstract__ = True

    # Sérialise l'objet en JSON
    def to_json(self) -> dict:
        if(not hasattr(self,'__model_out__') or self.__model_out__ is None or not issubclass(self.__model_out__, PydanticBaseModel)):
            raise ConfigurationException(f'Model output is not set for {self.__class__.__name__}')

        dict_from_model_out = {}
        for field in self.__model_out__.__fields__.values():
            if(field.type_ == list):
                dict_from_model_out[field.name] = [ item.to_json() if(isinstance(item, BaseModel)) else item for item in getattr(self, field.name)]
            elif(issubclass(field.type_, PydanticBaseModel)):
                dict_from_model_out[field.name] = getattr(self, field.name).to_json()
            else:
                dict_from_model_out[field.name] = str(getattr(self, field.name))

        return self.__class__.__model_out__(**dict_from_model_out)

    # Rafraichissement des données au prêt de la base de données
    def refresh(self) -> None:
        session = self.__class__.get_db()
        session.refresh(self)

    # Supprime l'objet de la base de données
    def delete(self) -> None:
        session = self.__class__.get_db()
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
        session = self.__class__.get_db()
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def save_relations(self) -> None:
        session = self.__class__.get_db()
        try:
            session.add(self)
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
    def get_db(cls) -> sessionmaker:
        return DB().db

    # Retourne la query de l'instance
    @classmethod
    def query(cls):
        return cls.get_db().query(cls)

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
    @classmethod
    def exists(cls, uuid) -> bool:
        return cls.query().filter(cls.uuid == uuid).first() is not None

    # Créé un nouvel enregistrement dans la base de données
    @classmethod
    def create(cls, obj: PydanticBaseModel) -> 'BaseModel':
        session = cls.get_db()

        # Création de l'instance
        instance = cls(**obj.__dict__)

        # persistance de l'instance
        try:
            session.add(instance)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            message = e.args[0]
            if "psycopg2.errors.UniqueViolation" in message:
                raise ModelAlreadyExistsException(f'{cls.__name__} already exists')
        except Exception as e:
            session.rollback()
            raise e

        return instance
