"""
🎯 VIEWS - EXERCICES PRATIQUES

CONSIGNES :
-----------
Pour chaque modèle, créer un ViewSet complet avec toutes les opérations CRUD :
- List (GET /api/model/)
- Create (POST /api/model/)
- Retrieve (GET /api/model/{id}/)
- Update (PUT/PATCH /api/model/{id}/)
- Destroy (DELETE /api/model/{id}/)

RÈGLES OBLIGATOIRES :
--------------------
✅ Utiliser ModelViewSet pour le CRUD complet
✅ Utiliser le bon serializer selon l'action (get_serializer_class)
✅ Ajouter des filtres (filter_backends)
✅ Ajouter la pagination
✅ Ajouter des actions personnalisées quand nécessaire
✅ Gérer les permissions

MÉTHODES À CONNAÎTRE :
---------------------
- get_serializer_class() : Choisir le serializer selon l'action
- get_queryset() : Optimiser les requêtes avec select_related/prefetch_related
- perform_create() : Logique supplémentaire à la création
- @action : Créer des endpoints personnalisés
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Sum

from .models import Category, Product, Order, OrderItem, Review, Client, Supplier
# TODO: Importer vos serializers depuis serializers_EXERCICES.py


# ============================================================================
# 📁 CATEGORY VIEWSET (EXEMPLE COMPLET - ÉTUDIEZ-LE)
# ============================================================================

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet complet pour gérer les catégories
    
    Endpoints générés automatiquement :
    - GET    /api/categories/          -> list()
    - POST   /api/categories/          -> create()
    - GET    /api/categories/{id}/     -> retrieve()
    - PUT    /api/categories/{id}/     -> update()
    - PATCH  /api/categories/{id}/     -> partial_update()
    - DELETE /api/categories/{id}/     -> destroy()
    
    Endpoints personnalisés :
    - GET /api/categories/{id}/products/  -> Liste des produits de la catégorie
    """
    
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, modification authentifiée
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']  # Recherche sur ces champs
    ordering_fields = ['name', 'created_at']  # Tri possible sur ces champs
    ordering = ['name']  # Tri par défaut
    
    def get_serializer_class(self):
        """
        Retourne le bon serializer selon l'action
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            # Pour créer/modifier : utiliser le CreateSerializer
            from .serializers_EXERCICES import CategoryCreateSerializer
            return CategoryCreateSerializer
        elif self.action == 'list':
            # Pour lister : utiliser le ListSerializer (léger)
            from .serializers_EXERCICES import CategoryListSerializer
            return CategoryListSerializer
        else:
            # Pour retrieve : utiliser le DetailSerializer (complet)
            from .serializers_EXERCICES import CategoryDetailSerializer
            return CategoryDetailSerializer
    
    def get_queryset(self):
        """
        Optimise les requêtes en préchargeant les relations
        """
        queryset = Category.objects.all()
        
        # Optimisation : précharger les produits pour éviter le N+1 query problem
        if self.action == 'list':
            queryset = queryset.annotate(products_count=Count('products'))
        elif self.action == 'retrieve':
            queryset = queryset.prefetch_related('products')
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        Endpoint personnalisé : GET /api/categories/{id}/products/
        Retourne tous les produits d'une catégorie
        """
        category = self.get_object()
        products = category.products.all()
        
        # TODO: Utiliser ProductListSerializer pour sérialiser les produits
        data = [
            {'id': p.id, 'name': p.name, 'price': str(p.price)}
            for p in products
        ]
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Endpoint personnalisé : GET /api/categories/popular/
        Retourne les catégories avec le plus de produits
        """
        categories = Category.objects.annotate(
            products_count=Count('products')
        ).order_by('-products_count')[:5]
        
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


# ============================================================================
# 📁 SUPPLIER VIEWSET
# ============================================================================

# TODO 1: Créer SupplierViewSet
# CONSIGNES :
# - Hériter de ModelViewSet
# - Utiliser les 3 serializers selon l'action
# - Ajouter la recherche sur 'name', 'contact_name', 'email'
# - Ajouter le tri sur 'name', 'created_at'
# - Permissions : IsAuthenticatedOrReadOnly

class SupplierViewSet(viewsets.ModelViewSet):
    """
    📦 TODO : ViewSet pour gérer les fournisseurs
    """
    queryset = Supplier.objects.all()
    # TODO: permission_classes
    # TODO: filter_backends
    # TODO: search_fields
    # TODO: ordering_fields
    # TODO: ordering
    
    def get_serializer_class(self):
        """TODO : Retourner le bon serializer selon l'action"""
        pass
    
    def get_queryset(self):
        """TODO : Optimiser les requêtes"""
        queryset = super().get_queryset()
        # TODO: Ajouter des annotations si nécessaire
        return queryset
    
    # TODO: Action personnalisée 'products' - Liste des produits d'un fournisseur
    # @action(detail=True, methods=['get'])
    # def products(self, request, pk=None):
    #     pass


# ============================================================================
# 📁 CLIENT VIEWSET
# ============================================================================

# TODO 2: Créer ClientViewSet
# CONSIGNES :
# - Recherche sur 'first_name', 'last_name', 'email'
# - Tri sur 'last_name', 'created_at'
# - Permissions : IsAuthenticated (les clients sont privés)
# - Action personnalisée 'orders' : Liste des commandes du client

class ClientViewSet(viewsets.ModelViewSet):
    """
    👤 TODO : ViewSet pour gérer les clients
    """
    queryset = Client.objects.all()
    # TODO: Compléter comme CategoryViewSet
    
    def get_serializer_class(self):
        """TODO"""
        pass
    
    # TODO: Action 'orders' - GET /api/clients/{id}/orders/
    # Retourner toutes les commandes de ce client


# ============================================================================
# 📁 PRODUCT VIEWSET (NIVEAU INTERMÉDIAIRE)
# ============================================================================

# TODO 3: Créer ProductViewSet
# CONSIGNES IMPORTANTES :
# - Recherche sur 'name', 'description'
# - Filtrage sur 'category', 'price'
# - Tri sur 'name', 'price', 'created_at', 'stock'
# - Permissions : IsAuthenticatedOrReadOnly
# - Optimisation : select_related('category') et prefetch_related('suppliers')

class ProductViewSet(viewsets.ModelViewSet):
    """
    🛍️ TODO : ViewSet pour gérer les produits
    """
    queryset = Product.objects.all()
    # TODO: Configuration complète
    
    def get_serializer_class(self):
        """TODO"""
        pass
    
    def get_queryset(self):
        """
        TODO : Optimiser les requêtes
        - select_related pour category (ForeignKey)
        - prefetch_related pour suppliers (ManyToMany)
        """
        queryset = super().get_queryset()
        # TODO: Ajouter les optimisations
        return queryset
    
    # TODO: Action 'low_stock' - GET /api/products/low_stock/
    # Retourner les produits avec stock < 10
    # @action(detail=False, methods=['get'])
    # def low_stock(self, request):
    #     pass
    
    # TODO: Action 'by_category' - GET /api/products/by_category/?category_id=1
    # Filtrer par catégorie via query parameter
    # @action(detail=False, methods=['get'])
    # def by_category(self, request):
    #     pass
    
    # TODO: Action 'reviews' - GET /api/products/{id}/reviews/
    # Retourner tous les avis d'un produit
    # @action(detail=True, methods=['get'])
    # def reviews(self, request, pk=None):
    #     pass


# ============================================================================
# 📁 REVIEW VIEWSET
# ============================================================================

# TODO 4: Créer ReviewViewSet
# CONSIGNES :
# - Filtrage sur 'product', 'user', 'rating'
# - Tri sur 'created_at', 'rating'
# - Permissions : IsAuthenticated
# - perform_create() : Associer automatiquement l'utilisateur connecté

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ⭐ TODO : ViewSet pour gérer les avis
    """
    queryset = Review.objects.all()
    # TODO: Configuration
    
    def get_serializer_class(self):
        """TODO"""
        pass
    
    def perform_create(self, serializer):
        """
        TODO : Lors de la création, associer automatiquement l'utilisateur connecté
        """
        # serializer.save(user=self.request.user)
        pass
    
    # TODO: Action 'top_rated' - GET /api/reviews/top_rated/
    # Retourner les avis avec rating >= 4


# ============================================================================
# 📁 ORDER VIEWSET (NIVEAU AVANCÉ)
# ============================================================================

# TODO 5: Créer OrderViewSet
# CONSIGNES COMPLEXES :
# - Filtrage sur 'user', 'client', 'status'
# - Tri sur 'created_at', 'status'
# - Permissions : IsAuthenticated
# - Optimisation : select_related('user', 'client') et prefetch_related('items__product')
# - perform_create() : Associer l'utilisateur connecté

class OrderViewSet(viewsets.ModelViewSet):
    """
    🛒 TODO : ViewSet pour gérer les commandes
    """
    queryset = Order.objects.all()
    # TODO: Configuration complète
    
    def get_serializer_class(self):
        """TODO"""
        pass
    
    def get_queryset(self):
        """
        TODO : Optimisations importantes
        - select_related pour user et client
        - prefetch_related pour items et products
        """
        queryset = super().get_queryset()
        # TODO: Optimisations
        return queryset
    
    def perform_create(self, serializer):
        """TODO : Associer l'utilisateur connecté"""
        pass
    
    # TODO: Action 'confirm' - POST /api/orders/{id}/confirm/
    # Changer le status de PENDING à CONFIRMED
    # @action(detail=True, methods=['post'])
    # def confirm(self, request, pk=None):
    #     order = self.get_object()
    #     if order.status == Order.StatusChoices.PENDING:
    #         order.status = Order.StatusChoices.CONFIRMED
    #         order.save()
    #         return Response({'status': 'Commande confirmée'})
    #     return Response(
    #         {'error': 'La commande ne peut pas être confirmée'},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
    
    # TODO: Action 'cancel' - POST /api/orders/{id}/cancel/
    # Changer le status à CANCELLED
    
    # TODO: Action 'add_item' - POST /api/orders/{id}/add_item/
    # Ajouter un produit à la commande
    # Paramètres attendus : product_id, quantity
    
    # TODO: Action 'my_orders' - GET /api/orders/my_orders/
    # Retourner toutes les commandes de l'utilisateur connecté


# ============================================================================
# 📁 ORDERITEM VIEWSET
# ============================================================================

# TODO 6: Créer OrderItemViewSet
# CONSIGNES :
# - Filtrage sur 'order', 'product'
# - Tri sur 'created_at'
# - Permissions : IsAuthenticated
# - Optimisation : select_related('order', 'product')
# - perform_create() : Vérifier que le stock est suffisant avant de créer

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    📦 TODO : ViewSet pour gérer les articles de commande
    """
    queryset = OrderItem.objects.all()
    # TODO: Configuration
    
    def get_serializer_class(self):
        """TODO"""
        pass
    
    def get_queryset(self):
        """TODO : Optimisations avec select_related"""
        queryset = super().get_queryset()
        # TODO: Optimisations
        return queryset
    
    def perform_create(self, serializer):
        """
        TODO : Avant de créer, vérifier le stock
        Si stock insuffisant, retourner une erreur
        """
        # product = serializer.validated_data['product']
        # quantity = serializer.validated_data['quantity']
        # if product.stock < quantity:
        #     raise serializers.ValidationError("Stock insuffisant")
        # serializer.save()
        pass


# ============================================================================
# 📊 RÉSUMÉ DES TÂCHES
# ============================================================================
"""
✅ FAIT :
- CategoryViewSet (exemple complet)

❌ À FAIRE :
- [ ] SupplierViewSet
- [ ] ClientViewSet
- [ ] ProductViewSet (avec 3 actions personnalisées)
- [ ] ReviewViewSet (avec 1 action)
- [ ] OrderViewSet (avec 4 actions personnalisées)
- [ ] OrderItemViewSet

TOTAL : 6 ViewSets à créer

ACTIONS PERSONNALISÉES À CRÉER :
- SupplierViewSet : 1 action
- ClientViewSet : 1 action
- ProductViewSet : 3 actions
- ReviewViewSet : 1 action
- OrderViewSet : 4 actions

TOTAL : 10 actions personnalisées

⏱️ TEMPS ESTIMÉ : 4-5 heures
🎯 DIFFICULTÉ : Moyenne à Avancée

💡 ASTUCES :
- Copiez la structure de CategoryViewSet pour commencer
- Testez chaque ViewSet au fur et à mesure
- Utilisez Postman ou curl pour tester vos endpoints
- Consultez la documentation DRF en cas de doute
"""
