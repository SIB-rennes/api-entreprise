import marshmallow
import marshmallow_dataclass as ma


class _BaseSchemaExcludingUnknown(marshmallow.Schema):
    """Schema marshmallow avec l'option d'exclure les champs unknown lors du load par défaut"""

    class Meta:
        unknown = marshmallow.EXCLUDE


class _AddMarshmallowSchema(type):
    """Metaclass qui génère le schema marshmallow pour une dataclass."""

    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        ma_schema_class = ma.class_schema(cls, base_schema=_BaseSchemaExcludingUnknown)

        cls.ma_schema_class = ma_schema_class
        cls.ma_schema = ma_schema_class()
        cls.ma_schema_many = ma_schema_class(many=True)
