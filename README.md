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

### Using `curl`

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

### Using Python `requests` Library

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

- Request body validation
- Creating models
- Serialization
- Generating postman documentation
- Using exceptions
- Limitations

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

Please ensure that you include the appropriate links to the respective projects and adjust the descriptions as needed. This section is a way to give credit to the open-source projects that have contributed to your library and show appreciation for the broader community.
