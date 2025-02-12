install `django-rest-knox`<br>
add `knox` to installed path<br>
add the following to settings

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    ...
}
```

add `shared.apps.authentication` to installed apps

<!-- TODO: Say why this is optional -->

(optional) extend `shared.apps.authentication.models.ExtensibleUser`<br>
add `path("auth/", include("shared.apps.authentication.urls"))` to urlpatterns<br>
add whichever model you use, you set the [model in your settings](https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#substituting-a-custom-user-model)

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
and create an instance of `shared.apps.authentication.settings.AuthConf`

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

the backend will redirect to your frontend with a token/code once done.
