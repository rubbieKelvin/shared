## Introduction

Setting up new Django projects often involves repetitive tasks and boilerplate code, which can slow down development and lead to inconsistencies across projects. This shared library was created to address these challenges and enhance the developer experience (DX).

> NOTE
> This library is unstable, everything works fine but changes are inevitable, so watch out for changes

### Key Objectives

- **Consistency**: Maintain consistent practices and structures across different Django projects.
- **Productivity**: Eliminate redundant tasks and boilerplate code to accelerate project development.
- **Best Practices**: Incorporate best practices and proven solutions for common development tasks.
- **Flexibility**: Offer configurable components to adapt to project-specific requirements.
- **Sustainability**: Keep the library evolving to embrace changes in Django and emerging development trends.

By utilizing this library, you can streamline your workflow, reduce repetitive work, and ensure that your Django projects adhere to best practices, all while maintaining flexibility and adaptability for your specific project needs.

## Features

### 1. Seamless API Views

Create API views effortlessly with built-in exception handling and straightforward request body validation. This feature simplifies the process of setting up API endpoints while ensuring robust error handling and validation.

### 2. Extended Model Features

Enhance your Django models with extended functionalities, including easy serialization without the need for specifying custom classes. This feature streamlines the serialization process, reducing the need for repetitive code.

### 3. Postman Documentation Generation

Automatically generate Postman documentation from your API views and seamlessly import it into your Postman workspace. This simplifies the task of creating API documentation and keeps it in sync with your codebase.

### 4. Request Body Validation with Pydantic

Effortlessly validate request bodies using Pydantic, a powerful data validation and parsing library. This feature ensures that incoming data meets the expected format, enhancing the security and reliability of your Django applications.

## Installation

To integrate this library into your project, follow these steps:

### 1. Clone the Repository

Clone this repository into your project directory:

```shell
git clone https://github.com/rubbieKelvin/shared
```

This method is suitable when you want to keep your library up-to-date by pulling changes from the remote repository.

### 2. Add as a Git Submodule (Optional)

If you have a fork of this library and want to keep it linked to your project while also receiving updates, you can add it as a Git submodule. Use the following command within your project directory:

```shell
git submodule add https://github.com/rubbieKelvin/shared shared-library
```

This submodule is a convenient way to manage an external codebase within your project.

### 3. Download from GitHub

If you prefer a one-time download, you can grab the library as a ZIP file from GitHub. After downloading, extract the contents and place them in your project folder.

> Please note that this library is not yet available on the Python Package Index (PyPI) but may become accessible once it reaches a stable version and undergoes extensive testing in development environments.

## Getting Started

### Creating API Endpoints with the `Api` Class

The `Api` class simplifies the process of defining API endpoints for your Django project. By utilizing this class, you can create endpoints with custom configurations, including route prefixes, permissions, and tags. This guide will walk you through the steps to create and configure API endpoints.

#### Prerequisites

Before creating endpoints, ensure that you have the necessary dependencies and your Django project is set up correctly.

#### Step 1: Import the `Api` Class

Start by importing the `Api` class from your library:

```python
from shared.view_tools.paths import Api
```

#### Step 2: Instantiate the `Api` Class

Next, create an instance of the `Api` class by providing optional configurations like a route prefix, tags, and a name. The route prefix is added to all endpoint paths.

```python
api = Api(
    prefix='/api/v1/',
    tags=["Tag1", "Tag2"],
    name="API Name",
    description="A description for this api"
)
```

- `prefix` (optional): A prefix to be added to all endpoint paths. If specified, it should end with a slash.
- `tags` (optional): A list of tags to classify this API. Use tags to categorize your endpoints.
- `name` (optional): A name for the API.
- `description` (optional): A description for this api

#### Step 3: Define Endpoints

You can create endpoints using the `endpoint` and `endpoint_class` decorators. The `endpoint` decorator is used for defining functions as endpoints, while the `endpoint_class` decorator is used for wrapping classes to handle various HTTP methods. Both decorators allow you to specify the HTTP method, path, name, and permission.

#### Using the `endpoint` Decorator

```python
@api.endpoint(path="example/", method="GET", name="Get Example Data")
def example_view(request):
    # Your view logic here
```

- `path`: The URL path for the endpoint.
- `method`: The HTTP method supported by the endpoint.
- `name` (optional): The name of the endpoint.

#### Using the `endpoint_class` Decorator

```python
@api.endpoint_class("example/<var>/", name="Dynamic Endpoint", permission=YourPermissionClass)
class MultiMethodEndpoint:
    def get(self, request, var):
        # GET method logic

    def post(self, request, var):
        # POST method logic
```

- `path`: The URL path for the endpoint.
- `name` (optional): The name of the endpoint.
- `permission` (optional): The permission class that protects this view.

#### Step 4: Handle Endpoints

In your view functions or methods, handle the logic specific to the endpoint's functionality. You can access request data, validate request bodies, and send responses. Additionally, you can use request path variables as needed.

#### Step 5: Include API Endpoints in URL Patterns

To include the defined API endpoints in your Django project's URL patterns, use the `paths` property of your `Api` instance:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    # ...
    *api.paths,
]
```

By following these steps, you can define and configure API endpoints easily and efficiently for your Django project. The `Api` class streamlines the process and allows you to focus on implementing the specific functionality of your endpoints.

Let's demonstrate how the defined endpoints can be used by clients or testing software to interact with your API. You can use tools like `curl`, Postman, or Python libraries like `requests` for testing.

Here are examples using `curl` and `requests`:

#### Using `curl`

`curl` is a command-line tool for making HTTP requests. You can use it to interact with your API endpoints.

1. **GET Request**

To make a GET request to your API endpoint, use the following command:

```bash
curl -X GET http://localhost:8000/api/v1/example/
```

2. **POST Request**

To make a POST request to your API endpoint with data, use the following command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://localhost:8000/api/v1/example/hello/
```

#### Using Python `requests` Library

The `requests` library in Python provides a simple and flexible way to send HTTP requests to your API endpoints.

Install `requests` if you haven't already:

```bash
pip install requests
```

Here are examples of how to use `requests`:

```python
import requests

# Base URL of your API
base_url = "http://localhost:8000/api/v1/"

# GET Request
response = requests.get(base_url + "example/")
print(response.status_code)
print(response.json())

# POST Request
var = "hello"
data = {"key": "value"}
headers = {"Content-Type": "application/json"}

response = requests.post(
    base_url + f"example/{var}/",
    json=data,
    headers=headers
)

print(response.status_code)
print(response.json())
```

These examples demonstrate how to use `curl` and the Python `requests` library to interact with your API endpoints. You can test various HTTP methods and verify the responses for your endpoints using these tools.

By following these steps, you can use `curl`, Python `requests`, or Postman to interact with your API endpoints, test functionality, and verify responses. These tools provide efficient ways to test your API during development and after deployment.

### Validating request body

In your Django REST framework project, ensuring that incoming data adheres to the expected format is a crucial aspect of maintaining data integrity and application security. With the validation feature provided by this library, you can easily validate request data against Pydantic schemas.

#### Using the @validate Decorator

The `@validate` decorator simplifies request body validation. It takes a Pydantic schema as an argument, allowing you to define the expected data structure for a particular API endpoint. If the incoming data doesn't conform to the schema, the decorator automatically returns an error response.

Here's how to use the `@validate` decorator:

```python
from shared.view_tools import body_tools

# Define a Pydantic schema for the request body
class MyPydanticSchema(pydantic.BaseModel):
    name: str
    age: int
    email: pydantic.EmailStr
    phone: str | None = None

# Apply the @validate decorator to your view function
@api1.endpoint(path="user/profile/update/", method="PATCH")
@body_tools.validate(MyPydanticSchema)
def my_validated_view(request: Request) -> Response:
    # Your view logic here
```

With this decorator in place, the incoming request data is automatically validated against the defined schema. If validation fails, an error response with a detailed error message is returned.

#### Getting the Validated Body

After using the `@validate` decorator, you can retrieve the validated request body in your view function using the `body_tools.get_validated_body(request)` method. This method returns a Pydantic BaseModel instance, allowing you to work with the validated data seamlessly.

Here's how to use the `body_tools.get_validated_body(request)` method:

```python
@api1.endpoint(path="user/profile/update/", method="PATCH")
@body_tools.validate(MyPydanticSchema)
def my_validated_view(request: Request) -> Response:
    # Get the validated request body
    body: MyPydanticSchema = body_tools.get_validated_body(request)

    # Now you can work with the validated data
    return Response({"message": f"Your name is {body.name}"})
```

By following this approach, you can ensure that your API endpoints receive valid and structured data, enhancing data quality and application security.

#### Error Handling

In case validation fails, the library automatically generates an error response with detailed information about the validation error. This includes the specific validation errors for each field, making it easy to diagnose and address issues with incoming data.

The error response includes:

- An "error" message: Indicates that the request data is invalid.
- An "error code" ("INPUT_ERROR" by default): Identifies the type of error.
- Additional "meta" data: Provides a detailed description of the validation errors for each field.

This error response ensures that clients receive clear and informative feedback when submitting invalid data to your API endpoints.

This feature simplifies the process of validating incoming data against Pydantic schemas. By using the `@validate` decorator and the `body_tools.get_validated_body(request)` method, you can ensure that your Django REST framework project receives valid and structured data, promoting data integrity and application security.

### Defining Models

In your Django application, data models are the backbone of your database structure. They define the structure and relationships between various data entities. This library provides a foundation for creating these data models with the `AbstractModel` class and simplifies the process of model serialization.

#### AbstractModel: The Base for All Models

The `AbstractModel` class serves as the base for all data models in your application. It includes common fields, such as `id`, `date_created`, and `date_updated`, which are shared across all your models.

Here's how to define a model using `AbstractModel`:

```python
from shared.abstractmodel import AbstractModel
from django.db import models

class YourModel(AbstractModel):
    # Define your model fields here
```

By inheriting from `AbstractModel`, your model automatically inherits common fields like `id`, which provides a unique identifier for each instance. The `date_created` and `date_updated` fields automatically manage the creation and update timestamps for each instance.

#### Customizing Serialization

This library also simplifies the process of customizing how your models are serialized. You can define specific serialization structures for each model. A serialization structure specifies which attributes to include in the serialized data.

To customize serialization, override the `default_serialization_structure` property in your concrete model class. This property should return a custom serialization structure for your model.

Here's an example of how to define a custom serialization structure for a model:

```python
class YourModel(AbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    @property
    def default_serialization_structure(self):
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
    def default_serialization_structure(self):
        return serialization.struct('name', 'description')
```

By customizing the serialization structure for your model, you have full control over which attributes are included in the serialized data. This allows you to adapt your data output to your application's specific requirements.

#### Handling Related Models

In a Django application, you often define relationships between different data models. These relationships can be one-to-one, one-to-many, or many-to-many, and they are an essential part of building a comprehensive database structure. This library simplifies how related models are handled during serialization, giving you the flexibility to choose how related models are included in the serialized data.

#### Serialization Modes for Related Models

When dealing with related models, this library provides serialization modes to customize how the related models are serialized. You can specify the serialization mode for a related model using the following modes:

- **"SERIALIZE_AS_PK"**: Serialize the related model as its primary key.
- **"SERIALIZE_AS_STRING"**: Serialize the related model as its string representation.
- **Custom Structure**: You can specify a custom structure for each related model.

##### 1. Serialize as Primary Key ("SERIALIZE_AS_PK")

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
    def default_serialization_structure(self):
        return serialization.struct(
            'title',
            author="SERIALIZE_AS_PK",  # Serialize the Author model as its primary key
        )
```

In this example, the `author` field in the `Book` model is serialized as the primary key of the related `Author` model.

##### 2. Serialize as String ("SERIALIZE_AS_STRING")

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
    def default_serialization_structure(self):
        return serialization.struct(
            'title',
            author="SERIALIZE_AS_STRING",  # Serialize the Author model as its string representation
        )
```

In this example, the `author` field in the `Book` model is serialized as the string representation of the related `Author` model, which is defined by the `__str__` method in the `Author` model.

##### 3. Custom Structure

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
    def default_serialization_structure(self):
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

### Serializing the model

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
    def default_serialization_structure(self):
        return {
            'title': True,
            'author': {
                'name': True,  # Include the 'name' attribute of the Author model
            },
        }
```

In this example, we have two models: `Author` and `Book`. The `Book` model has a foreign key relationship with the `Author` model. To customize the serialization structure, we define the `default_serialization_structure` property for the `Book` model.

Within the `default_serialization_structure`, we specify how we want the `Book` model to be serialized:

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

### Generating postman documentation

Postman is a popular tool for testing and documenting APIs. With your Django project's API endpoints defined using the `Api` class, you can generate Postman documentation automatically. This documentation helps you test your APIs and share them with your team or API consumers.

#### Generating Postman Documentation

To generate Postman documentation, follow these steps:

1. **Review Your API Endpoints**: Ensure that you have defined your API endpoints using the `Api` class in your Django project. The endpoints should be decorated with the necessary metadata such as HTTP methods, paths, and descriptions.

2. **Create a PostmanV2Collection Object**: To generate Postman documentation, you need to create a `PostmanV2Collection` object. This object will represent the Postman collection. Here's how you can do it:

   ```python
   from shared.view_tools.postman import PostmanV2Collection

   # Define the base URL of your API
   base_url = "https://example.com/api/v1"

   # Create an Info object to provide collection information
   collection_info = PostmanV2Collection.Info(
       name="My API Collection",
       description="Documentation for my API endpoints",
   )

   # Create the Postman collection object
   postman_collection = PostmanV2Collection(url=base_url, info=collection_info)
   ```

   In this example, replace `"https://example.com/api/v1"` with the base URL of your API.

3. **Define Variables**: You can define variables for your collection that can be reused in requests. For example, you can define a variable for the base URL. To define a variable, use the `var` method:

   ```python
   postman_collection.var("VAR", "<value>")
   ```

   This variable can be referenced in your requests as `{{VAR}}`.

4. **Add the View to URLs**: Finally, add your Postman view to your Django project's URLs so that it can be accessed. Here's an example of how to do it in your `urls.py`:

   ```python
   from django.urls import path

   urlpatterns = [
       # ... Your other URL patterns ...

       # Add the Postman view URL
       path("postman-v2-collection/", postman_collection.view),
   ]
   ```

#### Usage

Once you have completed the steps above, you can access the Postman documentation for your Django API by visiting the URL you defined for the Postman view. This documentation can be imported into Postman for testing your APIs or shared with others who need to consume your API.

## Contributions

I welcome contributions from the open-source community to enhance and improve this library. Whether you want to fix a bug, add a feature, or suggest improvements, your contributions are highly valued. Here's how you can get involved:

### Reporting Issues

If you encounter a bug or have a suggestion, please [create an issue](https://github.com/rubbieKelvin/shared/issues/new) on my issue tracker. When creating an issue, provide as much detail as possible, including a clear description, steps to reproduce, and any relevant error messages.

### Pull Requests

If you'd like to contribute code changes, please follow these steps:

1. **Fork the Repository**: Start by forking my repository on GitHub.

2. **Create a Branch**: Create a new branch for your changes. Use a descriptive branch name that relates to the issue or feature you're working on.

3. **Make Changes**: Implement your changes, ensuring that your code adheres to my coding standards.

4. **Tests**: If applicable, write tests to verify your changes.

5. **Documentation**: Update the documentation to reflect your changes, including code comments, README updates, or any other relevant documentation files.

6. **Commit Changes**: Commit your changes with clear and concise commit messages.

7. **Push Changes**: Push your branch to your forked repository on GitHub.

8. **Pull Request**: Open a pull request from your branch to the main repository. In the pull request description, explain the purpose of your changes and reference any related issues.

### Coding Guidelines

To maintain code consistency, follow best practices, including code style, naming conventions, and code structure.

### Review Process

After you submit a pull request, it will undergo a review process. I'll provide feedback and work with you to ensure your contributions align with the project's goals.

I'm excited to collaborate with you, and I appreciate your contributions to make this library even better!

Thank you for being a part of the open-source community. Your efforts are valuable, and they help us improve this library for everyone.

## Acknowledgments

This library would not have been possible without the fantastic work of the open-source community and the following projects:

- [Django](https://www.djangoproject.com/): A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- [Django REST framework](https://www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs on top of Django.
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and parsing using Python type hints.
- [pytest](https://docs.pytest.org/en/latest/): A testing framework that makes it easy to write simple and scalable test cases.

I express my gratitude to the developers and contributors of these projects for providing invaluable tools and resources that have greatly facilitated the development of this library.
