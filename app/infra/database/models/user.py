import datetime
from mongoengine import Document, StringField, DateTimeField, BooleanField


class User(Document):
    username = StringField(required=True, unique=True)
    fullname = StringField(required=False)
    role = StringField(required=True)
    hashed_password = StringField()
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    @classmethod
    def from_mongo(cls, data: dict, id_str=False):
        """We must convert _id into "id". """
        if not data:
            return data
        id = data.pop("_id", None) if not id_str else str(data.pop("_id", None))
        if "_cls" in data:
            data.pop("_cls", None)
        return cls(**dict(data, id=id))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super(User, self).save(*args, **kwargs)

    meta = {
        "collection": "Users",
        "indexes": ["role"],
        "allow_inheritance": True,
        "index_cls": False,
    }
