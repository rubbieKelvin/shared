# Validating request body

In your Django REST framework project, ensuring that incoming data adheres to the expected format is a crucial aspect of maintaining data integrity and application security. With the validation feature provided by this library, you can easily validate request data against Pydantic schemas.

## Using the @validate Decorator

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

## Getting the Validated Body

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

## Error Handling

In case validation fails, the library automatically generates an error response with detailed information about the validation error. This includes the specific validation errors for each field, making it easy to diagnose and address issues with incoming data.

The error response includes:

- An "error" message: Indicates that the request data is invalid.
- An "error code" ("INPUT_ERROR" by default): Identifies the type of error.
- Additional "meta" data: Provides a detailed description of the validation errors for each field.

This error response ensures that clients receive clear and informative feedback when submitting invalid data to your API endpoints.

This feature simplifies the process of validating incoming data against Pydantic schemas. By using the `@validate` decorator and the `body_tools.get_validated_body(request)` method, you can ensure that your Django REST framework project receives valid and structured data, promoting data integrity and application security.
