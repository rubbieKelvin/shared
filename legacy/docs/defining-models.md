# Defining Models

In your Django application, data models are the backbone of your database structure. They define the structure and relationships between various data entities. This library provides a foundation for creating these data models with the `AbstractModel` class and simplifies the process of model serialization.

## AbstractModel: The Base for All Models

The `AbstractModel` class serves as the base for all data models in your application. It includes common fields, such as `id`, `date_created`, and `date_updated`, which are shared across all your models.

Here's how to define a model using `AbstractModel`:

```python
from shared.abstractmodel import AbstractModel
from django.db import models

class YourModel(AbstractModel):
    # Define your model fields here
```

By inheriting from `AbstractModel`, your model automatically inherits common fields like `id`, which provides a unique identifier for each instance. The `date_created` and `date_updated` fields automatically manage the creation and update timestamps for each instance.

## Customizing Serialization

This library also simplifies the process of customizing how your models are serialized. You can define specific serialization structures for each model. A serialization structure specifies which attributes to include in the serialized data.

To customize serialization, override the `serializers` property in your concrete model class. This property should return a custom serialization structure for your model.

Here's an example of how to define a custom serialization structure for a model:

```python
class YourModel(AbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    @property
    def serializers(self):
        return {
            'name': True,
            'description': True,
        }
```

Alternatively, you can use the `serialization.struct` method to define the serialization structure. This method simplifies the process of specifying which fields should be included in the serialized data.

```python
from shared.abstractmodel import serialization

class YourModel(AbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    @property
    def serializers(self):
        return serialization.struct('name', 'description')
```

By customizing the serialization structure for your model, you have full control over which attributes are included in the serialized data. This allows you to adapt your data output to your application's specific requirements.

## Handling Related Models

In a Django application, you often define relationships between different data models. These relationships can be one-to-one, one-to-many, or many-to-many, and they are an essential part of building a comprehensive database structure. This library simplifies how related models are handled during serialization, giving you the flexibility to choose how related models are included in the serialized data.

## Serialization Modes for Related Models

When dealing with related models, this library provides serialization modes to customize how the related models are serialized. You can specify the serialization mode for a related model using the following modes:

- **"SERIALIZE_AS_PK"**: Serialize the related model as its primary key.
- **"SERIALIZE_AS_STRING"**: Serialize the related model as its string representation.
- **Custom Structure**: You can specify a custom structure for each related model.

### 1. Serialize as Primary Key ("SERIALIZE_AS_PK")

This mode serializes the related model as its primary key. This is a straightforward way to include related model data without the need to serialize all its attributes. It's useful when you only need a reference to the related model in your serialized data.

Here's an example of how to use the "SERIALIZE_AS_PK" mode:

```python
from shared.abstractmodel import AbstractModel, serialization
from django.db import models

class Author(AbstractModel):
    name = models.CharField(max_length=100)

class Book(AbstractModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    @property
    def serializers(self):
        return serialization.struct(
            'title',
            author="SERIALIZE_AS_PK",  # Serialize the Author model as its primary key
        )
```

In this example, the `author` field in the `Book` model is serialized as the primary key of the related `Author` model.

### 2. Serialize as String ("SERIALIZE_AS_STRING")

The "SERIALIZE_AS_STRING" mode serializes the related model as its string representation. This is useful when you want to include a human-readable representation of the related model in your serialized data.

Here's an example of how to use the "SERIALIZE_AS_STRING" mode:

```python
from shared.abstractmodel import AbstractModel, serialization
from django.db import models

class Author(AbstractModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(AbstractModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    @property
    def serializers(self):
        return serialization.struct(
            'title',
            author="SERIALIZE_AS_STRING",  # Serialize the Author model as its string representation
        )
```

In this example, the `author` field in the `Book` model is serialized as the string representation of the related `Author` model, which is defined by the `__str__` method in the `Author` model.

### 3. Custom Structure

You can specify a custom structure for each related model, allowing you to define exactly which attributes of the related model are included in the serialized data. This gives you full control over how related models are serialized.

Here's an example of how to specify a custom structure for a related model:

```python
from shared.abstractmodel import AbstractModel, serialization
from django.db import models

class Author(AbstractModel):
    name = models.CharField(max_length=100)

class Book(AbstractModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    @property
    def serializers(self):
        return serialization.struct(
            'title',
            author=serialization.struct(
                'id',
                'name',  # Include the 'name' attribute of the Author model
            ),
        )
```

In this example, the `author` field in the `Book` model is serialized with a custom structure that includes only the `name` attribute of the related `Author` model.

You can easily control how related models are included in the serialized data with these modes, adapting the serialization output to your specific requirements. This flexibility ensures that your data is structured in a way that best serves your application's needs.
