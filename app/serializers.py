"""
🎯 SERIALIZERS - EXERCICES PRATIQUES

CONSIGNES :
-----------
Pour chaque modèle, créer 3 serializers :
1. CreateSerializer - Pour créer des objets (accepte les IDs)
2. ListSerializer - Pour lister (léger, sans relations imbriquées)
3. DetailSerializer - Pour afficher les détails complets (avec relations)

RÈGLES OBLIGATOIRES :
--------------------
✅ Utiliser ModelSerializer
✅ Toujours définir 'model' et 'fields' dans Meta
✅ Ajouter des validations personnalisées
✅ Utiliser SerializerMethodField pour les champs calculés
✅ Mettre read_only=True sur les champs calculés

ORDRE D'IMPLÉMENTATION :
-----------------------
1. Category (FAIT comme exemple ✅)
2. Supplier (TODO - À FAIRE)
3. Client (TODO - À FAIRE)
4. Product (TODO - À FAIRE)
5. Review (TODO - À FAIRE)
6. Order (TODO - À FAIRE)
7. OrderItem (TODO - À FAIRE)
"""

from rest_framework import serializers
from .models import Product,Category,Supplier,OrderItem,Order,Client,Review,User
from django.db.models import Avg


# ============================================================================
# 📁 CATEGORY SERIALIZERS (EXEMPLE COMPLET - ÉTUDIEZ-LE)
# ============================================================================

class CategorySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Category
        fields = ['name','description']
        
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Le nom doit contenir au moins 3 caractères.")
                    
        return value.strip().title() 
   

class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name', 'description','products_count','created_at']
    
    def get_products_count(self, obj):
        return obj.products.count()
   
   
    
class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    product_names = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name','description', 'product_names','created_at','url']   
        extra_kwargs={
            'url':{'view_name':'category-detail','lookup_field':'pk'}
        }
        
    def get_product_names(self, obj):
        return [ product.name  for product in obj.products.all()[:5]]
    
    

# ============================================================================
# 📁 SUPPLIER SERIALIZERS
# ============================================================================

# TODO 1: Créer SupplierCreateSerializer
# CONSIGNES :
# - Champs : name, contact_name, email, phone_number, address
# - Validation : email doit être valide (déjà géré par EmailField)
# - Validation : name doit faire au moins 2 caractères

class SupplierCreateSerializer(serializers.ModelSerializer):
    """
    ✍️ TODO : Compléter ce serializer pour créer un fournisseur
    """
    class Meta:
        model = Supplier
        # TODO: Définir les fields
        fields = ['name', 'contact_name', 'email', 'phone_number', 'address']  # ⚠️ REMPLACER par la liste explicite des champs
    
    # TODO: Ajouter une validation sur 'name'
    def validate_name(self, data):
        if len(data) < 3:
            raise serializers.ValidationError('name doit faire au moins 2 caractères')
        return data


# TODO 2: Créer SupplierListSerializer
# CONSIGNES :
# - Champs : id, name, email, products_count
# - products_count : utiliser SerializerMethodField pour compter les produits

class SupplierListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : Serializer pour lister les fournisseurs
    """
    # TODO: Ajouter products_count avec SerializerMethodField
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'products_count']  # TODO: Compléter
    
    # TODO: Implémenter get_products_count
    def get_products_count(self, obj):
        return obj.products.count()


# TODO 3: Créer SupplierDetailSerializer
# CONSIGNES :
# - Tous les champs du modèle
# - Ajouter la liste des produits fournis (nom et prix seulement)

class SupplierDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    🔍 TODO : Serializer pour les détails complets d'un fournisseur
    """
    # TODO: Ajouter un champ 'products' avec SerializerMethodField
    products = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields =  ['id', 'name', 'email','contact_name','address', 'products_count','products','url']  # TODO: Être plus explicite
        extra_kwargs={
            'url':{'view_name':'supplier-detail','lookup_field':'pk'}
        }
        
    # TODO: Implémenter get_products
    
    def get_products(self, obj):
        return [product.name for product in obj.products.all()[:5] ]
    
    def get_products_count(self, obj):
        return obj.products.count()
  

# ============================================================================
# 📁 CLIENT SERIALIZERS
# ============================================================================

# TODO 4: Créer les 3 serializers pour Client
# CONSIGNES :
# - ClientCreateSerializer : first_name, last_name, email, phone_number, address
# - ClientListSerializer : id, first_name, last_name, email, orders_count
# - ClientDetailSerializer : tous les champs + liste des commandes

class ClientCreateSerializer(serializers.ModelSerializer):
    """
    ✍️ TODO : À compléter
    """
    class Meta:
        model = Client
        fields = [ 'first_name', 'last_name', 'email', 'phone_number', 'address']  # TODO
    
    # TODO: Validation sur email (vérifier qu'il est unique)
    # TODO: Validation sur first_name et last_name (min 2 caractères)
    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return value

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return value

    
    


class ClientListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : À compléter
    """
    # TODO: Ajouter orders_count
    orders_count =serializers.SerializerMethodField()
    # TODO: Ajouter full_name (combinaison de first_name et last_name)
    full_name =serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [ 'first_name', 'last_name', 'email', 'phone_number', 'address','orders_count','full_name']   # TODO
        
    def get_orders_count(self, obj):
        
        return obj.orders.count()
    
    def get_full_name(self, obj):
        first_name=obj.first_name or""
        last_name=obj.last_name or ""
        full_name=f"{first_name} {last_name}".strip()
        
        return full_name


class ClientDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : À compléter
    """
    # TODO: Ajouter la liste des commandes
    orders_list =serializers.SerializerMethodField()
    # TODO: Ajouter le montant total dépensé
    total_price =serializers.SerializerMethodField()
     
    class Meta:
        model = Client
        fields = '__all__'
        
        
    def get_orders_list(self, obj):
        return [ {               "id": order.id,                "user": order.user.username if order.user else None,
                "client": f"{order.client.first_name} {order.client.last_name}",
                "status": order.status,
                "created_at": order.created_at.isoformat() if hasattr(order, 'created_at') else None,
                "total": str(order.total) if hasattr(order, 'total') else None
            }
                for order in obj.orders.all()[:5]]
    
        
    def get_total_price(self, obj):    
        
        return obj.orders_subtotal
    

# ============================================================================
# 📁 PRODUCT SERIALIZERS
# ============================================================================

# TODO 5: Créer les 3 serializers pour Product
# CONSIGNES IMPORTANTES :
# - ProductCreateSerializer : 
#   * Accepter category comme ID (pas d'objet complet)
#   * Accepter suppliers comme liste d'IDs
#   * Validation : price > 0
#   * Validation : stock >= 0
#   * Validation : name doit faire au moins 3 caractères

class ProductCreateSerializer(serializers.ModelSerializer):
    """
    ✍️ TODO : Serializer pour créer un produit
    
    ATTENTION : 
    - category doit être un PrimaryKeyRelatedField
    - suppliers doit être un PrimaryKeyRelatedField avec many=True
    """
    # TODO: Définir category correctement
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # TODO: Définir suppliers correctement
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(),many=True)
    
    class Meta:
        model = Product
        fields = ['name','price','description','category','image','stock','supplier']  # TODO
    
    # TODO: validate_price
    def validate_price(self,data):
        if data <= 0:
            raise serializers.ValidationError("Validation : price > 0")
        return data

    # TODO: validate_stock
    def validate_stock(self, attrs):
        if attrs <=0:
            raise serializers.ValidationError(" Validation : stock >= 0")
        return attrs
    # TODO: validate_name
    def validate_name(self, value):
        # Nettoyer le nom
        cleaned_name = " ".join(value.split()).strip()

        # Vérifier si un autre produit du même nom existe
        if Product.objects.filter(name__iexact=cleaned_name).exists():
            raise serializers.ValidationError(f"Un produit nommé '{cleaned_name}' existe déjà.")

        return cleaned_name


class ProductListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : Serializer pour lister les produits
    
    AFFICHER :
    - id, name, price, stock
    - category_name (nom de la catégorie, pas l'ID)
    - in_stock (boolean - True si stock > 0)
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    # TODO: Ajouter in_stock
    in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category_name','in_stock','url']  # TODO: Compléter
        # extra_kwagrs={'url':{'view_name':'','lookup_field':'pk'}}
    def get_in_stock(self,obj):
        
        return obj.in_stock


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : Serializer pour les détails d'un produit
    
    AFFICHER :
    - Tous les champs
    - Détails de la catégorie (objet complet)
    - Liste des fournisseurs (objets complets)
    - Moyenne des notes (reviews)
    - Nombre d'avis
    """
    category = CategoryDetailSerializer(read_only=True)
    # TODO: suppliers (liste complète)
    supplier = SupplierDetailSerializer(read_only=True,many=True)
    # TODO: average_rating
    average_rating=serializers.SerializerMethodField()
    # TODO: reviews_count
    reviews_count =serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        
    def get_average_rating(self, obj):
        """Calcule la moyenne des notes pour ce produit."""
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

    def get_reviews_count(self, obj):
        """Renvoie le nombre d'avis liés à ce produit."""
        return obj.reviews.count()


# ============================================================================
# 📁 REVIEW SERIALIZERS
# ============================================================================

# TODO 6: Créer les 3 serializers pour Review
# CONSIGNES :
# - ReviewCreateSerializer : product (ID), user (ID), rating, comment
#   * Validation : rating entre 1 et 5
#   * Validation : comment doit faire au moins 10 caractères
# - ReviewListSerializer : id, product_name, user_name, rating, created_at
# - ReviewDetailSerializer : tous les champs avec détails du produit

class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    ✍️ TODO : À compléter
    """
    product= serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user= serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Review
        fields = ['product','user','rating','comment']  # TODO
    
    # TODO: validate_rating (entre 1 et 5)
    def validate_rating(self,value):
        if value > 5 or value <=0:
            raise serializers.ValidationError("rating entre 1 et 5")
        return value      
        
    # TODO: validate_comment (min 10 caractères)


class ReviewListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : À compléter
    """
    # TODO: Ajouter product_name
    product_name = serializers.CharField(source='product.name',read_only=True)
    # TODO: Ajouter username
    username = serializers.CharField(source='user.username',read_only=True)
    
    class Meta:
        model = Review
        fields = ['id','product_name','username','rating','comment','created_at'] # TODO


class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : À compléter
    """
    # TODO: Inclure les détails du produit
    product = ProductDetailSerializer(read_only=True)
    # TODO: Inclure les infos de l'utilisateur
    user=serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = '__all__'
        
    def get_user(self, obj):
        """
        Retourne les infos essentielles de l'utilisateur
        """
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email
        }



# ============================================================================
# 📁 ORDER SERIALIZERS (NIVEAU AVANCÉ)
# ============================================================================

# TODO 7: Créer les 3 serializers pour Order
# CONSIGNES COMPLEXES :
# - OrderCreateSerializer :
#   * user (ID), client (ID), status
#   * NE PAS inclure products ici (on utilisera OrderItem)
# - OrderListSerializer :
#   * id, order_id, client_name, status, created_at, total_amount
#   * total_amount : calculer la somme de tous les items
# - OrderDetailSerializer :
#   * Tous les champs
#   * Liste complète des items avec détails
#   * Montant total

# serializers.py

class OrderItemCreateSerializer(serializers.ModelSerializer):
    """🎁 Serializer minimal pour créer les items en même temps que la commande"""
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['user', 'client', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order



class OrderListSerializer(serializers.ModelSerializer):
    """
    📋 Serializer léger pour lister les commandes
    """
    # order_id = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [ 'order_id', 'client_name', 'status', 'created_at', 'items_count', 'total_amount']

    # def get_order_id(self, obj):
    #     return getattr(obj, 'order_id', obj.id)

    def get_client_name(self, obj):
        client = getattr(obj, 'client', None)
        if not client:
            return None
        first = getattr(client, 'first_name', '') or ''
        last = getattr(client, 'last_name', '') or ''
        return f"{first} {last}".strip() or None

    def get_items_count(self, obj):
        if hasattr(obj, 'items'):
            return obj.items.count()
        return obj.orderitem_set.count() if hasattr(obj, 'orderitem_set') else 0

    def get_total_amount(self, obj):
        # Preferer une propriété 'total' si présente sur le modèle
        total = getattr(obj, 'total', None)
        if total is not None:
            return total
        # Sinon calculer à partir des items
        items = getattr(obj, 'items', None) or getattr(obj, 'orderitem_set', None)
        if items is None:
            return 0
        s = 0
        for it in items.all():
            unit = getattr(it, 'unit_price', None) or getattr(it.product, 'price', 0)
            qty = getattr(it, 'quantity', 0)
            try:
                s += unit * qty
            except Exception:
                # si types incompatibles (None), ignorer
                pass
        return s


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    🔍 Serializer détaillé pour une commande
    """
    # nested list of items (détails)
    items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    client_details = ClientListSerializer(source='client', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_items(self, obj):
        items_qs = getattr(obj, 'items', None) or getattr(obj, 'orderitem_set', None)
        if items_qs is None:
            return []
        serializer = OrderItemListSerializer(items_qs.all(), many=True, context=self.context)
        return serializer.data

    def get_total_amount(self, obj):
        total = getattr(obj, 'total', None)
        if total is not None:
            return total
        items_qs = getattr(obj, 'items', None) or getattr(obj, 'orderitem_set', None)
        if items_qs is None:
            return 0
        s = 0
        for it in items_qs.all():
            unit = getattr(it, 'unit_price', None) or getattr(it.product, 'price', 0)
            qty = getattr(it, 'quantity', 0)
            try:
                s += unit * qty
            except Exception:
                pass
        return s


# ============================================================================
# 📁 ORDERITEM SERIALIZERS
# ============================================================================

# TODO 8: Créer les serializers pour OrderItem
# CONSIGNES :
# - OrderItemCreateSerializer : order (ID), product (ID), quantity
#   * Validation : quantity > 0
#   * Validation : vérifier que le stock est suffisant
# - OrderItemListSerializer : id, product_name, quantity, subtotal
# - OrderItemDetailSerializer : tous les champs avec détails


class OrderItemListSerializer(serializers.ModelSerializer):
    """
    📋 Serializer pour lister les lignes d'une commande
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    unit_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'unit_price', 'subtotal']

    def get_unit_price(self, obj):
        return getattr(obj, 'unit_price', None) or getattr(obj.product, 'price', None)

    def get_subtotal(self, obj):
        # Preferer une propriété 'subtotal' si présente sur le modèle
        subtotal = getattr(obj, 'subtotal', None)
        if subtotal is not None:
            return subtotal
        unit = self.get_unit_price(obj) or 0
        qty = getattr(obj, 'quantity', 0) or 0
        try:
            return unit * qty
        except Exception:
            return 0


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """
    🔍 Serializer détaillé pour une ligne de commande
    """
    product = ProductListSerializer(read_only=True)
    order = OrderListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
