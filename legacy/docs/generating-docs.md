# Generating postman documentation

Postman is a popular tool for testing and documenting APIs. With your Django project's API endpoints defined using the `Api` class, you can generate Postman documentation automatically. This documentation helps you test your APIs and share them with your team or API consumers.

## Generating Postman Documentation

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

## Usage

Once you have completed the steps above, you can access the Postman documentation for your Django API by visiting the URL you defined for the Postman view. This documentation can be imported into Postman for testing your APIs or shared with others who need to consume your API.
