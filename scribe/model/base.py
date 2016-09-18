#base abstract model class, defines a "get dictionary" for objects

from scribe import db

class BaseModel(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
