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
from .models import Category, Product, Order, OrderItem, Review, Client, Supplier


# ============================================================================
# 📁 CATEGORY SERIALIZERS (EXEMPLE COMPLET - ÉTUDIEZ-LE)
# ============================================================================

class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    ✍️ Serializer pour CRÉER une catégorie
    - Accepte seulement les champs nécessaires à la création
    - Validation personnalisée sur le nom
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
    
    def validate_name(self, value):
        """VALIDATION : Le nom doit faire au moins 3 caractères"""
        if len(value) < 3:
            raise serializers.ValidationError("Le nom doit contenir au moins 3 caractères.")
        return value.strip().title()  # Nettoyer et capitaliser


class CategoryListSerializer(serializers.ModelSerializer):
    """
    📋 Serializer pour LISTER les catégories
    - Léger, seulement les infos essentielles
    - Ajoute le nombre de produits
    """
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count', 'created_at']
    
    def get_products_count(self, obj):
        """Compte le nombre de produits dans cette catégorie"""
        return obj.products.count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    🔍 Serializer pour afficher les DÉTAILS d'une catégorie
    - Toutes les infos
    - Liste des noms de produits
    """
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products', 'created_at', 'updated_at']
    
    def get_products(self, obj):
        """Retourne la liste des produits avec nom et prix"""
        return [
            {'id': p.id, 'name': p.name, 'price': str(p.price)}
            for p in obj.products.all()[:10]  # Limiter à 10 pour la performance
        ]


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
        fields = '__all__'  # ⚠️ REMPLACER par la liste explicite des champs
    
    # TODO: Ajouter une validation sur 'name'
    pass


# TODO 2: Créer SupplierListSerializer
# CONSIGNES :
# - Champs : id, name, email, products_count
# - products_count : utiliser SerializerMethodField pour compter les produits

class SupplierListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : Serializer pour lister les fournisseurs
    """
    # TODO: Ajouter products_count avec SerializerMethodField
    
    class Meta:
        model = Supplier
        fields = ['id', 'name']  # TODO: Compléter
    
    # TODO: Implémenter get_products_count
    pass


# TODO 3: Créer SupplierDetailSerializer
# CONSIGNES :
# - Tous les champs du modèle
# - Ajouter la liste des produits fournis (nom et prix seulement)

class SupplierDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : Serializer pour les détails complets d'un fournisseur
    """
    # TODO: Ajouter un champ 'products' avec SerializerMethodField
    
    class Meta:
        model = Supplier
        fields = '__all__'  # TODO: Être plus explicite
    
    # TODO: Implémenter get_products


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
        fields = []  # TODO
    
    # TODO: Validation sur email (vérifier qu'il est unique)
    # TODO: Validation sur first_name et last_name (min 2 caractères)


class ClientListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : À compléter
    """
    # TODO: Ajouter orders_count
    # TODO: Ajouter full_name (combinaison de first_name et last_name)
    
    class Meta:
        model = Client
        fields = []  # TODO


class ClientDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : À compléter
    """
    # TODO: Ajouter la liste des commandes
    # TODO: Ajouter le montant total dépensé
    
    class Meta:
        model = Client
        fields = '__all__'


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
    # TODO: Définir suppliers correctement
    
    class Meta:
        model = Product
        fields = []  # TODO
    
    # TODO: validate_price
    # TODO: validate_stock
    # TODO: validate_name


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
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category_name']  # TODO: Compléter


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
    # TODO: average_rating
    # TODO: reviews_count
    
    class Meta:
        model = Product
        fields = '__all__'


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
    class Meta:
        model = Review
        fields = []  # TODO
    
    # TODO: validate_rating (entre 1 et 5)
    # TODO: validate_comment (min 10 caractères)


class ReviewListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : À compléter
    """
    # TODO: Ajouter product_name
    # TODO: Ajouter username
    
    class Meta:
        model = Review
        fields = []  # TODO


class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : À compléter
    """
    # TODO: Inclure les détails du produit
    # TODO: Inclure les infos de l'utilisateur
    
    class Meta:
        model = Review
        fields = '__all__'


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

class OrderCreateSerializer(serializers.ModelSerializer):
    """
    ✍️ TODO : À compléter
    
    NOTE : La gestion des produits se fera via OrderItem
    """
    class Meta:
        model = Order
        fields = []  # TODO
    
    # TODO: validate_status (doit être dans les choix)


class OrderListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : À compléter
    """
    # TODO: client_name
    # TODO: items_count (nombre de lignes)
    # TODO: total_amount (somme des subtotals)
    
    class Meta:
        model = Order
        fields = []  # TODO


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : À compléter
    """
    # TODO: items (liste des OrderItems avec détails)
    # TODO: total_amount
    # TODO: client_details
    
    class Meta:
        model = Order
        fields = '__all__'


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

class OrderItemCreateSerializer(serializers.ModelSerializer):
    """
    ✍️ TODO : À compléter
    """
    class Meta:
        model = OrderItem
        fields = []  # TODO
    
    # TODO: validate_quantity
    # TODO: validate (vérifier le stock disponible)


class OrderItemListSerializer(serializers.ModelSerializer):
    """
    📋 TODO : À compléter
    """
    # TODO: product_name
    # TODO: unit_price
    # TODO: subtotal (utilisez la propriété du modèle)
    
    class Meta:
        model = OrderItem
        fields = []  # TODO


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """
    🔍 TODO : À compléter
    """
    # TODO: Détails complets du produit
    # TODO: Détails de la commande
    
    class Meta:
        model = OrderItem
        fields = '__all__'


# ============================================================================
# 📊 RÉSUMÉ DES TÂCHES
# ============================================================================
"""
✅ FAIT :
- Category (3 serializers complets comme exemple)

❌ À FAIRE :
- [x] Supplier (3 serializers)
- [x] Client (3 serializers)
- [ ] Product (3 serializers)
- [ ] Review (3 serializers)
- [ ] Order (3 serializers)
- [ ] OrderItem (3 serializers)

TOTAL : 18 serializers à créer (3 déjà faits = 21 au total)

⏱️ TEMPS ESTIMÉ : 3-4 heures
🎯 DIFFICULTÉ : Moyenne à Avancée
"""
