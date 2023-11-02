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

set `RK_SHARED_AUTHENTICATION_CONFIG` in settings