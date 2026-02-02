"""
⚙️ CONFIGURATION DJANGO REST FRAMEWORK

CONSIGNES :
-----------
Ajouter cette configuration à votre fichier settings.py

Cette configuration définit :
- Pagination
- Permissions par défaut
- Filtrage
- Authentification
- Format de rendu
"""

# ============================================================================
# À AJOUTER DANS settings.py
# ============================================================================

REST_FRAMEWORK = {
    # Pagination par défaut
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 10 résultats par page
    
    # Permissions par défaut
    # TODO: Choisir la permission appropriée
    # Options :
    # - 'rest_framework.permissions.AllowAny'  # Accès public
    # - 'rest_framework.permissions.IsAuthenticated'  # Authentification requise
    # - 'rest_framework.permissions.IsAuthenticatedOrReadOnly'  # Lecture publique, écriture authentifiée
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    # Authentification
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # Pour DRF browsable API
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',  # Si vous utilisez des tokens
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # Si vous utilisez JWT
    ],
    
    # Filtrage
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Format de rendu
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Interface web de DRF
    ],
    
    # Parsing
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',  # Pour les uploads de fichiers
    ],
    
    # Gestion des erreurs
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    # Format de date/heure
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    
    # Throttling (limitation de taux) - optionnel
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '1000/day'
    # }
}

# ============================================================================
# CONFIGURATION SWAGGER (drf-yasg)
# ============================================================================

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
}

# ============================================================================
# CONFIGURATION CORS (si vous avez un frontend séparé)
# ============================================================================

# Ajouter 'corsheaders' dans INSTALLED_APPS
INSTALLED_APPS = [
    # ... autres apps
    'corsheaders',
]

# Ajouter le middleware CORS
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # En haut de la liste
    # ... autres middlewares
]

# Configuration CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React/Vue/Angular en développement
    "http://127.0.0.1:3000",
]

# OU pour le développement uniquement (ATTENTION : pas en production !)
CORS_ALLOW_ALL_ORIGINS = True

# ============================================================================
# INSTALLED_APPS COMPLET
# ============================================================================

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'corsheaders',
    
    # Votre app
    'app',
]

# ============================================================================
# 📋 CHECKLIST DE CONFIGURATION
# ============================================================================
"""
✅ INSTALLATION DES DÉPENDANCES :
- [ ] pip install -r requirements_API.txt

✅ CONFIGURATION SETTINGS.PY :
- [ ] Ajouter REST_FRAMEWORK dans settings.py
- [ ] Ajouter SWAGGER_SETTINGS dans settings.py
- [ ] Ajouter 'rest_framework' dans INSTALLED_APPS
- [ ] Ajouter 'django_filters' dans INSTALLED_APPS
- [ ] Ajouter 'drf_yasg' dans INSTALLED_APPS
- [ ] Ajouter 'corsheaders' dans INSTALLED_APPS (si frontend séparé)
- [ ] Configurer CORS si nécessaire

✅ MIGRATIONS :
- [ ] python manage.py makemigrations
- [ ] python manage.py migrate

✅ CRÉER UN SUPERUSER :
- [ ] python manage.py createsuperuser

✅ LANCER LE SERVEUR :
- [ ] python manage.py runserver

✅ TESTER :
- [ ] http://localhost:8000/api/
- [ ] http://localhost:8000/swagger/
- [ ] http://localhost:8000/admin/
"""
