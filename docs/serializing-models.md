# Serializing the model

Let's provide an example of how the `serialize` method is used in your Django models:

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
        return {
            'title': True,
            'author': {
                'name': True,  # Include the 'name' attribute of the Author model
            },
        }
```

In this example, we have two models: `Author` and `Book`. The `Book` model has a foreign key relationship with the `Author` model. To customize the serialization structure, we define the `serializers` property for the `Book` model.

Within the `serializers`, we specify how we want the `Book` model to be serialized:

- The `'title'` field is set to `True`, which means it will be included in the serialized data.
- The `'author'` field is defined with a custom structure. In this custom structure, we include the `'name'` attribute of the related `Author` model.

Now, when you use the `serialize` method on an instance of the `Book` model, it will serialize the data based on the specified structure. For example:

```python
book_instance = Book.objects.first()  # Get an instance of the Book model

# Serialize the 'book_instance' using the specified structure
serialized_data = book_instance.serialize()

# 'serialized_data' will contain the 'title' and 'author' attributes
# with the 'name' attribute of the related Author model
```

This way, you can control which attributes of the related models are included in the serialized data. This allows you to customize the serialization output to meet the specific needs of your application.
