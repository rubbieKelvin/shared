# Creating API Endpoints with the `Api` Class

The `Api` class simplifies the process of defining API endpoints for your Django project. By utilizing this class, you can create endpoints with custom configurations, including route prefixes, permissions, and tags. This guide will walk you through the steps to create and configure API endpoints.

## Prerequisites

Before creating endpoints, ensure that you have the necessary dependencies and your Django project is set up correctly.

## Step 1: Import the `Api` Class

Start by importing the `Api` class from your library:

```python
from shared.view_tools.paths import Api
```

## Step 2: Instantiate the `Api` Class

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

## Step 3: Define Endpoints

You can create endpoints using the `endpoint` and `endpoint_class` decorators. The `endpoint` decorator is used for defining functions as endpoints, while the `endpoint_class` decorator is used for wrapping classes to handle various HTTP methods. Both decorators allow you to specify the HTTP method, path, name, and permission.

## Using the `endpoint` Decorator

```python
@api.endpoint(path="example/", method="GET", name="Get Example Data")
def example_view(request):
    # Your view logic here
```

- `path`: The URL path for the endpoint.
- `method`: The HTTP method supported by the endpoint.
- `name` (optional): The name of the endpoint.

## Using the `endpoint_class` Decorator

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

## Step 4: Handle Endpoints

In your view functions or methods, handle the logic specific to the endpoint's functionality. You can access request data, validate request bodies, and send responses. Additionally, you can use request path variables as needed.

## Step 5: Include API Endpoints in URL Patterns

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

## Using `curl`

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

## Using Python `requests` Library

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
