install `django-rest-knox`
add `knox` to installed path
add the following to settings 
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    ...
}
```
add `shared.apps.authentication` to installed apps
(optional) extend `shared.apps.authentication.models.ExtensibleUser`
add `path("auth/", include("shared.apps.authentication.urls"))` to urlpatterns
setup static:
```
# settings.py

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Add your Vite build directory to STATICFILES_DIRS
]

STATIC_URL = "/static/"
```

set `SHARED` in settings
    add `AUTHENTICATION_CONFIG` in `SHARED`
    and create an instance of `shared.apps.authentication.settings.AuthenticationConfiguration`

like so 
```
SHARED = {
    "AUTHENTICATION_CONFIG": AuthenticationConfiguration(
        application_name="MyShare",
        application_url="https://www.google.com",
        application_icon_url="https://cdn-icons-png.flaticon.com/512/2839/2839021.png",
        callback_url="",
    )
}

```

the backend will redirect to your frontend with a token/code once done