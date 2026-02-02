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


from rest_framework import generics, filters, status,viewsets
from rest_framework.response import Response
from .models import Category, Product, Order, OrderItem, Review, Client, Supplier
from .serializers import ( CategorySerializer,CategoryListSerializer,CategoryDetailSerializer,
                          OrderCreateSerializer,OrderDetailSerializer,OrderListSerializer,
                          OrderItemCreateSerializer ,OrderItemListSerializer,OrderItemDetailSerializer)
from django.db.models import Count
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers as rf_serializers



# Create your views here.
# ============================================================================
# 📁 CATEGORY VIEWSET (EXEMPLE COMPLET - ÉTUDIEZ-LE)
# ============================================================================

class CategoryCreateView(generics.CreateAPIView):
    """
    📁 CategoryCreateView
    """
    serializer_class = CategorySerializer
    queryset=Category.objects.all()

class CategoryListView(generics.ListAPIView):
    """
    📁 CategoryListView
    """
    serializer_class =CategoryListSerializer
    queryset=Category.objects.all()   
  
    
    # def get_queryset(self):
    #     queryset = Category.objects.all().annotate(products_count=Count('products'))
        
    #     return queryset
class CategoryDetailView(generics.RetrieveAPIView):
    """
    📁 CategoryDetailView
    """
    serializer_class =CategoryDetailSerializer
    queryset=Category.objects.all()   
    
    # def get_queryset(self):
    #     queryset = Category.objects.all().prefetch_related('products')
    #     return queryset
    # lookup_field = 'id'  # 👈 On dit à la vue d’utiliser "id" au lieu de "pk"

    
    
class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class =CategoryDetailSerializer
    queryset=Category.objects.all()   
    



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
    search_fields = ['name', 'address']  # Recherche sur ces champs
    ordering_fields = ['name']  # Tri possible sur ces champs
    ordering = ['name']  # Tri par défaut
    # TODO: permission_classes
    # TODO: filter_backends
    # TODO: search_fields
    # TODO: ordering_fields
    # TODO: ordering
    
    def get_serializer_class(self):
        """TODO : Retourner le bon serializer selon l'action"""
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            from .serializers import SupplierCreateSerializer
            return SupplierCreateSerializer
        elif self.action == 'list':
            from .serializers import SupplierListSerializer
            return SupplierListSerializer
        else:
            from .serializers import SupplierDetailSerializer
            return SupplierDetailSerializer
    
    def get_queryset(self):
        """TODO : Optimiser les requêtes"""
        queryset = Supplier.objects.all()
        # TODO: Ajouter des annotations si nécessaire
        # Optimisation : précharger les produits pour éviter le N+1 query problem
        if self.action == 'list':
            queryset = queryset.annotate(products_count=Count('products'))
        elif self.action == 'retrieve':
            queryset = queryset.prefetch_related('products')
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
    queryset = Client.objects.all()
    search_fields=['first_name','email','address','last_name','phone_number']
    ordering_fields=['first_name','email','address','last_name']
    ordering=['first_name']
    
    def get_serializer_class(self):
        
        
        # if self.action in ['create', 'update', 'partial_update']:
        if self.action == 'create' or self.action == 'update' or self.action =='partial_update':
            from .serializers import ClientCreateSerializer
            return ClientCreateSerializer
        elif self.action =='list':
            from .serializers import ClientListSerializer
            return ClientListSerializer
        else:
            from .serializers import ClientDetailSerializer
            return ClientDetailSerializer
        
    def get_queryset(self):
        queryset=Client.objects.all()
        if self.action=='list':
            queryset=queryset.annotate(orders_count=Count('orders'))
        elif self.action =='retrieve':
                        # Précharger les commandes pour éviter les requêtes multiples
            queryset = queryset.prefetch_related('orders__items', 'orders__items__product','orders__user')

            
        return queryset   
    
    

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
class ProductViewApi(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    
    def get_serializer_class(self):
        if self.action  in ['create', 'update', 'partial_update']:
            from .serializers import ProductCreateSerializer
            return ProductCreateSerializer
        elif self.action =='list':
            from .serializers import ProductListSerializer
            return ProductListSerializer

        else:
            from .serializers import ProductDetailSerializer
            return ProductDetailSerializer
        
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
    queryset = Review.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            from .serializers import ReviewCreateSerializer
            return ReviewCreateSerializer
        elif self.action == 'list':
            from .serializers import ReviewListSerializer
            return ReviewListSerializer
        else:
            from .serializers import ReviewDetailSerializer

            return ReviewDetailSerializer
    # def perform_create(self, serializer):
    #     """
    #     TODO : Lors de la création, associer automatiquement l'utilisateur connecté
    #     """
    #     # serializer.save(user=self.request.user)
    #     pass
    
    # TODO: Action 'top_rated' - GET /api/reviews/top_rated/
    # Retourner les avis avec rating >= 4
    





from rest_framework.decorators import action

# ============================================================================
# 📁 ORDER VIEWSET (NIVEAU AVANCÉ)
# ============================================================================


class OrderViewSet(viewsets.ModelViewSet):
    """
    🛒 ViewSet pour gérer les commandes
    """
    queryset = Order.objects.all()
    # permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['user', 'client', 'status']
    # ordering_fields = ['created_at', 'status']
    # ordering = ['-created_at']

    def get_serializer_class(self):
        """Retourne le serializer selon l'action"""
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateSerializer
        elif self.action == 'list':
            return OrderListSerializer
        else:
            return OrderDetailSerializer

    def get_queryset(self):
        """
        Optimisations :
        - select_related pour user et client
        - prefetch_related pour items__product
        """
        queryset = super().get_queryset().select_related('user', 'client').prefetch_related('items__product')
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Crée une commande + ses items"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        # Retourne les détails complets après création
        detail_serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        """Associer l'utilisateur connecté à la commande"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if getattr(order, 'status', None) == Order.StatusChoices.PENDING:
            order.status = Order.StatusChoices.CONFIRMED
            order.save()
            return Response({'status': 'Commande confirmée'})
        return Response({'error': "La commande ne peut pas être confirmée"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if getattr(order, 'status', None) not in [Order.StatusChoices.CANCELLED, Order.StatusChoices.DELIVERED]:
            order.status = Order.StatusChoices.CANCELLED
            order.save()
            return Response({'status': 'Commande annulée'})
        return Response({'error': "La commande ne peut pas être annulée"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """
        Ajouter un produit à la commande.
        Attendu en body: product_id, quantity
        """
        order = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({'error': 'product_id et quantity requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({'error': 'quantity doit être un entier'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Produit introuvable'}, status=status.HTTP_404_NOT_FOUND)

        if product.stock < quantity:
            return Response({'error': 'Stock insuffisant'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer l'OrderItem
        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
        # Décrémenter le stock
        product.stock = product.stock - quantity
        product.save()

        serializer = OrderItemDetailSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Retourner toutes les commandes de l'utilisateur connecté"""
        qs = self.filter_queryset(self.get_queryset().filter(user=request.user))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


# ============================================================================
# 📁 ORDERITEM VIEWSET
# ============================================================================

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    📦 ViewSet pour gérer les articles de commande
    """
    queryset = OrderItem.objects.all()
    # permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ['order', 'product']
    # ordering_fields = ['created_at']
    # ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderItemCreateSerializer
        elif self.action == 'list':
            return OrderItemListSerializer
        else:
            return OrderItemDetailSerializer

    def get_queryset(self):
        """Optimisations avec select_related"""
        queryset = super().get_queryset().select_related('order', 'product')
        return queryset

    def perform_create(self, serializer):
        """
        Avant de créer, vérifier le stock
        """
        product = serializer.validated_data.get('product')
        quantity = serializer.validated_data.get('quantity', 0)
        if product.stock < quantity:
            raise rf_serializers.ValidationError("Stock insuffisant")
        # Décrémenter le stock et sauvegarder
        product.stock = product.stock - quantity
        product.save()
        serializer.save()
