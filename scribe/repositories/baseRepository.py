from scribe.model.base import BaseModel
from abc import ABCMeta, abstractmethod
from scribe import db

class BaseRepository(metaclass=ABCMeta):
    def __init__(self, model_class: BaseModel):
        self.model_class = model_class

    # Get an entity by its primary key
    def find(self, id):
        entity = self.model_class.query.get(id)
        return entity

    # Add an entity if it doesn't exist, or update an existing entity
    # For example, a new or existing user
    def add_or_update(self, entity):
        #result = self.validate(entity)
        #if result.success():
        db.session.add(entity)
        #return result

    # **kwargs is any sort of sql filter argument
    def get(self, **kwargs):
        entities = self.model_class.query.filter_by(**kwargs).all()
        return entities

    def delete(self, id):
        self.model_class.query.filter_by(id=id).delete()

    # used to offset some problems with sql alchemy
    # probably won't be used
    def expunge(self, entity):
        db.session.expunge(entity)

    #@abstractmethod #can be implemented later on repository by repository basis
    #def validate(self, entity):
    #    pass

    # commits everything to the db
    # MUST run this function to confirm any of the prior functions
    def save_changes(self):
        db.session.commit()