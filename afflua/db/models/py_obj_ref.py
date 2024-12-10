from bson import ObjectId # type: ignore

class PyObjectId(ObjectId):
    """Custom class to use ObjectId as a Pydantic field"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    