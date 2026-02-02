"""
🎯 URLS - EXERCICES PRATIQUES

CONSIGNES :
-----------
Créer une structure d'URLs propre et RESTful pour votre API.

RÈGLES OBLIGATOIRES :
--------------------
✅ Utiliser DefaultRouter pour les ViewSets
✅ Structure cohérente /api/<ressource>/
✅ Noms de routes explicites (basename)
✅ Versionning de l'API (optionnel mais recommandé)
✅ Documentation automatique (swagger/redoc)

ARCHITECTURE :
-------------
/api/
  /categories/                  # Liste et création
  /categories/{id}/             # Détail, modification, suppression
  /categories/{id}/products/    # Action personnalisée
  /products/
  /products/{id}/
  /products/low_stock/          # Action personnalisée
  ... etc
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# TODO: Importer vos ViewSets depuis views_EXERCICES.py
# from app.views_EXERCICES import (
#     CategoryViewSet,
#     SupplierViewSet,
#     ClientViewSet,
#     ProductViewSet,
#     ReviewViewSet,
#     OrderViewSet,
#     OrderItemViewSet
# )


# ============================================================================
# 📚 CONFIGURATION DE LA DOCUMENTATION API (SWAGGER)
# ============================================================================

# Configuration de Swagger pour générer la documentation automatique
schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="""
        API REST complète pour une boutique en ligne
        
        ## Fonctionnalités :
        - Gestion des catégories
        - Gestion des produits
        - Gestion des commandes
        - Gestion des avis
        - Gestion des clients
        - Gestion des fournisseurs
        
        ## Authentification :
        Certains endpoints nécessitent une authentification.
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@shop.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# ============================================================================
# 📡 CONFIGURATION DU ROUTER
# ============================================================================

# Créer le router principal
router = DefaultRouter()

# TODO 1: Enregistrer CategoryViewSet
# CONSIGNE : 
# - URL : 'categories'
# - basename : 'category'
# router.register(r'categories', CategoryViewSet, basename='category')

# TODO 2: Enregistrer SupplierViewSet
# CONSIGNE :
# - URL : 'suppliers'
# - basename : 'supplier'
# router.register(r'suppliers', SupplierViewSet, basename='supplier')

# TODO 3: Enregistrer ClientViewSet
# router.register(r'clients', ClientViewSet, basename='client')

# TODO 4: Enregistrer ProductViewSet
# router.register(r'products', ProductViewSet, basename='product')

# TODO 5: Enregistrer ReviewViewSet
# router.register(r'reviews', ReviewViewSet, basename='review')

# TODO 6: Enregistrer OrderViewSet
# router.register(r'orders', OrderViewSet, basename='order')

# TODO 7: Enregistrer OrderItemViewSet
# router.register(r'order-items', OrderItemViewSet, basename='orderitem')


# ============================================================================
# 📍 CONFIGURATION DES URLS
# ============================================================================

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # API REST
    path('api/', include(router.urls)),
    
    # Authentification (pour DRF browsable API)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Documentation Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]


# ============================================================================
# 📋 ENDPOINTS GÉNÉRÉS AUTOMATIQUEMENT
# ============================================================================
"""
Une fois que vous avez enregistré tous les ViewSets, vous aurez :

CATEGORIES :
------------
GET    /api/categories/                    -> Liste des catégories
POST   /api/categories/                    -> Créer une catégorie
GET    /api/categories/{id}/               -> Détail d'une catégorie
PUT    /api/categories/{id}/               -> Modifier une catégorie (complet)
PATCH  /api/categories/{id}/               -> Modifier une catégorie (partiel)
DELETE /api/categories/{id}/               -> Supprimer une catégorie
GET    /api/categories/{id}/products/      -> Produits de la catégorie
GET    /api/categories/popular/            -> Catégories populaires

SUPPLIERS :
-----------
GET    /api/suppliers/                     -> Liste des fournisseurs
POST   /api/suppliers/                     -> Créer un fournisseur
GET    /api/suppliers/{id}/                -> Détail d'un fournisseur
PUT    /api/suppliers/{id}/                -> Modifier un fournisseur
PATCH  /api/suppliers/{id}/                -> Modifier un fournisseur (partiel)
DELETE /api/suppliers/{id}/                -> Supprimer un fournisseur
GET    /api/suppliers/{id}/products/       -> Produits du fournisseur (TODO)

CLIENTS :
---------
GET    /api/clients/                       -> Liste des clients
POST   /api/clients/                       -> Créer un client
GET    /api/clients/{id}/                  -> Détail d'un client
PUT    /api/clients/{id}/                  -> Modifier un client
PATCH  /api/clients/{id}/                  -> Modifier un client (partiel)
DELETE /api/clients/{id}/                  -> Supprimer un client
GET    /api/clients/{id}/orders/           -> Commandes du client (TODO)

PRODUCTS :
----------
GET    /api/products/                      -> Liste des produits
POST   /api/products/                      -> Créer un produit
GET    /api/products/{id}/                 -> Détail d'un produit
PUT    /api/products/{id}/                 -> Modifier un produit
PATCH  /api/products/{id}/                 -> Modifier un produit (partiel)
DELETE /api/products/{id}/                 -> Supprimer un produit
GET    /api/products/low_stock/            -> Produits en rupture (TODO)
GET    /api/products/by_category/          -> Filtrer par catégorie (TODO)
GET    /api/products/{id}/reviews/         -> Avis du produit (TODO)

REVIEWS :
---------
GET    /api/reviews/                       -> Liste des avis
POST   /api/reviews/                       -> Créer un avis
GET    /api/reviews/{id}/                  -> Détail d'un avis
PUT    /api/reviews/{id}/                  -> Modifier un avis
PATCH  /api/reviews/{id}/                  -> Modifier un avis (partiel)
DELETE /api/reviews/{id}/                  -> Supprimer un avis
GET    /api/reviews/top_rated/             -> Meilleurs avis (TODO)

ORDERS :
--------
GET    /api/orders/                        -> Liste des commandes
POST   /api/orders/                        -> Créer une commande
GET    /api/orders/{id}/                   -> Détail d'une commande
PUT    /api/orders/{id}/                   -> Modifier une commande
PATCH  /api/orders/{id}/                   -> Modifier une commande (partiel)
DELETE /api/orders/{id}/                   -> Supprimer une commande
POST   /api/orders/{id}/confirm/           -> Confirmer la commande (TODO)
POST   /api/orders/{id}/cancel/            -> Annuler la commande (TODO)
POST   /api/orders/{id}/add_item/          -> Ajouter un produit (TODO)
GET    /api/orders/my_orders/              -> Mes commandes (TODO)

ORDER ITEMS :
-------------
GET    /api/order-items/                   -> Liste des articles
POST   /api/order-items/                   -> Créer un article
GET    /api/order-items/{id}/              -> Détail d'un article
PUT    /api/order-items/{id}/              -> Modifier un article
PATCH  /api/order-items/{id}/              -> Modifier un article (partiel)
DELETE /api/order-items/{id}/              -> Supprimer un article

DOCUMENTATION :
---------------
GET    /swagger/                           -> Documentation Swagger UI
GET    /redoc/                             -> Documentation ReDoc
GET    /swagger.json                       -> Schéma OpenAPI JSON

TOTAL : 40+ endpoints !
"""


# ============================================================================
# 🧪 TESTER VOS ENDPOINTS
# ============================================================================
"""
AVEC CURL :
-----------
# Lister les catégories
curl http://localhost:8000/api/categories/

# Créer une catégorie
curl -X POST http://localhost:8000/api/categories/ \\
  -H "Content-Type: application/json" \\
  -d '{"name": "Électronique", "description": "Produits électroniques"}'

# Obtenir une catégorie
curl http://localhost:8000/api/categories/1/

# Modifier une catégorie
curl -X PATCH http://localhost:8000/api/categories/1/ \\
  -H "Content-Type: application/json" \\
  -d '{"description": "Nouvelle description"}'

# Supprimer une catégorie
curl -X DELETE http://localhost:8000/api/categories/1/


AVEC HTTPIE (plus lisible) :
----------------------------
# Installer httpie : pip install httpie

# Lister
http GET http://localhost:8000/api/categories/

# Créer
http POST http://localhost:8000/api/categories/ \\
  name="Électronique" description="Produits électroniques"

# Détail
http GET http://localhost:8000/api/categories/1/


AVEC PYTHON REQUESTS :
----------------------
import requests

# Lister
response = requests.get('http://localhost:8000/api/categories/')
print(response.json())

# Créer
data = {'name': 'Électronique', 'description': 'Produits électroniques'}
response = requests.post('http://localhost:8000/api/categories/', json=data)
print(response.json())


AVEC LE NAVIGABLE API DE DRF :
------------------------------
Ouvrez simplement dans votre navigateur :
http://localhost:8000/api/categories/

Vous aurez une interface graphique pour tester !
"""


# ============================================================================
# 📊 RÉSUMÉ DES TÂCHES
# ============================================================================
"""
✅ FAIT :
- Structure de base des URLs
- Configuration Swagger
- Documentation

❌ À FAIRE :
- [ ] Importer les ViewSets
- [ ] Enregistrer les 7 ViewSets dans le router
- [ ] Tester tous les endpoints
- [ ] Vérifier la documentation Swagger

⏱️ TEMPS ESTIMÉ : 30 minutes
🎯 DIFFICULTÉ : Facile

💡 CONSEIL :
Testez au fur et à mesure en démarrant le serveur :
python manage.py runserver

Puis visitez :
- http://localhost:8000/api/
- http://localhost:8000/swagger/
"""
