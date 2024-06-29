import ulid
from django.db import models

class ULIDField(models.CharField):
    def __init__(self, *args, primary_key:bool=False, db_collation=None, **kwargs):
        kwargs['max_length'] = 26
        kwargs.setdefault('unique', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', ulid.ULID())
        super().__init__(*args, db_collation=db_collation, primary_key=primary_key, **kwargs)
        
    def deconstruct(self):
        # ensures the field can be properly serialized by Django's migration framework.
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        
        if 'default' in kwargs:
            del kwargs['default']
            
        return name, path, args, kwargs
    
    def get_prep_value(self, value):
        # prepares the value for saving to the database, converting it to a string if it's a ULID instance.
        if isinstance(value, ulid.ULID):
            return str(value)
        return value
    
    def from_db_value(self, value, expression, connection):
        # converts the value from the database to a ulid.ULID instance
        if value is None:
            return value
        
        return ulid.ULID(value)
    
    def to_python(self, value):
        # ensures the value is always a ulid.ULID instance when working with it in Python code.
        if value is None or isinstance(value, ulid.ULID):
            return value
        
        return ulid.ULID(value)

