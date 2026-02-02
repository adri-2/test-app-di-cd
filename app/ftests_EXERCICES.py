# 🧪 TESTS - EXERCICES PRATIQUES

"""
CONSIGNES :
-----------
Créer des tests unitaires pour valider le bon fonctionnement de votre API.

RÈGLES OBLIGATOIRES :
--------------------
✅ Tester CHAQUE endpoint
✅ Tester les validations
✅ Tester les relations entre modèles
✅ Tester les permissions
✅ Utiliser APITestCase de Django REST Framework

TYPES DE TESTS :
---------------
1. Tests de création (POST)
2. Tests de lecture (GET)
3. Tests de mise à jour (PUT/PATCH)
4. Tests de suppression (DELETE)
5. Tests de validation
6. Tests de permissions
7. Tests des actions personnalisées
"""

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal

from app.models import Category, Product, Order, OrderItem, Review, Client, Supplier


# ============================================================================
# 📁 TESTS CATEGORY (EXEMPLE COMPLET)
# ============================================================================

class CategoryAPITestCase(APITestCase):
    """
    Tests complets pour l'API des catégories
    """
    
    def setUp(self):
        """
        Méthode appelée avant chaque test
        Créer des données de test
        """
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Créer des catégories de test
        self.category1 = Category.objects.create(
            name="Électronique",
            description="Produits électroniques"
        )
        self.category2 = Category.objects.create(
            name="Vêtements",
            description="Vêtements et accessoires"
        )
        
        # URL de base
        self.list_url = '/api/categories/'
        self.detail_url = f'/api/categories/{self.category1.id}/'
    
    def test_list_categories(self):
        """
        ✅ TEST : Lister toutes les catégories
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Électronique")
    
    def test_create_category(self):
        """
        ✅ TEST : Créer une nouvelle catégorie
        """
        data = {
            'name': 'Livres',
            'description': 'Livres et magazines'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(response.data['name'], 'Livres')
    
    def test_create_category_validation_error(self):
        """
        ✅ TEST : Créer une catégorie avec un nom trop court (validation)
        """
        data = {
            'name': 'AB',  # Trop court (< 3 caractères)
            'description': 'Test'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
    
    def test_retrieve_category(self):
        """
        ✅ TEST : Obtenir les détails d'une catégorie
        """
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Électronique")
    
    def test_update_category(self):
        """
        ✅ TEST : Modifier une catégorie (PUT)
        """
        data = {
            'name': 'High-Tech',
            'description': 'Produits high-tech'
        }
        
        response = self.client.put(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'High-Tech')
    
    def test_partial_update_category(self):
        """
        ✅ TEST : Modifier partiellement une catégorie (PATCH)
        """
        data = {'description': 'Nouvelle description'}
        
        response = self.client.patch(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.description, 'Nouvelle description')
        self.assertEqual(self.category1.name, "Électronique")  # Nom inchangé
    
    def test_delete_category(self):
        """
        ✅ TEST : Supprimer une catégorie
        """
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)
    
    def test_search_categories(self):
        """
        ✅ TEST : Rechercher des catégories
        """
        response = self.client.get(f'{self.list_url}?search=électronique')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Électronique")


# ============================================================================
# 📁 TESTS PRODUCT
# ============================================================================

# TODO 1: Créer ProductAPITestCase
# CONSIGNES :
# - Tester la création d'un produit
# - Tester la validation du prix (doit être > 0)
# - Tester la validation du stock (doit être >= 0)
# - Tester la relation avec Category
# - Tester la relation ManyToMany avec Supplier

class ProductAPITestCase(APITestCase):
    """
    🛍️ TODO : Tests pour l'API des produits
    """
    
    def setUp(self):
        """TODO : Créer les données de test"""
        # Créer un utilisateur
        # Créer des catégories
        # Créer des fournisseurs
        # Créer des produits
        pass
    
    def test_list_products(self):
        """TODO : Tester la liste des produits"""
        pass
    
    def test_create_product(self):
        """TODO : Tester la création d'un produit"""
        # data = {
        #     'name': 'Smartphone',
        #     'price': '599.99',
        #     'description': 'Un super smartphone',
        #     'category': self.category.id,
        #     'stock': 10,
        #     'suppliers': [self.supplier1.id, self.supplier2.id]
        # }
        pass
    
    def test_create_product_negative_price(self):
        """TODO : Tester qu'un prix négatif est rejeté"""
        pass
    
    def test_create_product_negative_stock(self):
        """TODO : Tester qu'un stock négatif est rejeté"""
        pass
    
    def test_filter_products_by_category(self):
        """TODO : Tester le filtrage par catégorie"""
        pass
    
    def test_low_stock_action(self):
        """TODO : Tester l'action personnalisée low_stock"""
        # response = self.client.get('/api/products/low_stock/')
        pass


# ============================================================================
# 📁 TESTS ORDER
# ============================================================================

# TODO 2: Créer OrderAPITestCase
# CONSIGNES :
# - Tester la création d'une commande
# - Tester l'action confirm
# - Tester l'action cancel
# - Tester que seul l'utilisateur connecté voit ses commandes

class OrderAPITestCase(APITestCase):
    """
    🛒 TODO : Tests pour l'API des commandes
    """
    
    def setUp(self):
        """TODO : Créer les données de test"""
        pass
    
    def test_create_order(self):
        """TODO : Tester la création d'une commande"""
        pass
    
    def test_confirm_order(self):
        """TODO : Tester la confirmation d'une commande"""
        # response = self.client.post(f'/api/orders/{order.order_id}/confirm/')
        pass
    
    def test_cancel_order(self):
        """TODO : Tester l'annulation d'une commande"""
        pass
    
    def test_my_orders_action(self):
        """TODO : Tester que l'utilisateur voit seulement ses commandes"""
        pass


# ============================================================================
# 📁 TESTS ORDERITEM
# ============================================================================

# TODO 3: Créer OrderItemAPITestCase
# CONSIGNES :
# - Tester la création d'un OrderItem
# - Tester qu'on ne peut pas commander plus que le stock disponible
# - Tester le calcul du subtotal

class OrderItemAPITestCase(APITestCase):
    """
    📦 TODO : Tests pour l'API des articles de commande
    """
    
    def setUp(self):
        """TODO : Créer les données de test"""
        pass
    
    def test_create_order_item(self):
        """TODO : Tester la création d'un article"""
        pass
    
    def test_create_order_item_insufficient_stock(self):
        """TODO : Tester qu'on ne peut pas commander si stock insuffisant"""
        # Product avec stock = 5
        # Essayer de commander quantity = 10
        # Doit retourner une erreur
        pass
    
    def test_item_subtotal(self):
        """TODO : Tester le calcul du subtotal"""
        # Créer un item avec quantity=3 et price=10
        # Vérifier que subtotal = 30
        pass


# ============================================================================
# 📁 TESTS REVIEW
# ============================================================================

# TODO 4: Créer ReviewAPITestCase
# CONSIGNES :
# - Tester la création d'un avis
# - Tester que le rating doit être entre 1 et 5
# - Tester que le comment doit faire au moins 10 caractères
# - Tester qu'un utilisateur ne peut pas laisser 2 avis sur le même produit

class ReviewAPITestCase(APITestCase):
    """
    ⭐ TODO : Tests pour l'API des avis
    """
    
    def setUp(self):
        """TODO : Créer les données de test"""
        pass
    
    def test_create_review(self):
        """TODO : Tester la création d'un avis"""
        pass
    
    def test_review_rating_validation(self):
        """TODO : Tester que rating doit être entre 1 et 5"""
        # Essayer avec rating = 0 -> erreur
        # Essayer avec rating = 6 -> erreur
        pass
    
    def test_review_comment_min_length(self):
        """TODO : Tester que comment doit faire au moins 10 caractères"""
        pass
    
    def test_unique_review_per_user_product(self):
        """TODO : Tester qu'on ne peut pas laisser 2 avis sur le même produit"""
        # Créer un premier avis
        # Essayer d'en créer un deuxième -> erreur
        pass


# ============================================================================
# 📁 TESTS CLIENT
# ============================================================================

# TODO 5: Créer ClientAPITestCase

class ClientAPITestCase(APITestCase):
    """
    👤 TODO : Tests pour l'API des clients
    """
    pass


# ============================================================================
# 📁 TESTS SUPPLIER
# ============================================================================

# TODO 6: Créer SupplierAPITestCase

class SupplierAPITestCase(APITestCase):
    """
    📦 TODO : Tests pour l'API des fournisseurs
    """
    pass


# ============================================================================
# 📊 RÉSUMÉ DES TÂCHES
# ============================================================================
"""
✅ FAIT :
- CategoryAPITestCase (8 tests complets)

❌ À FAIRE :
- [ ] ProductAPITestCase (6+ tests)
- [ ] OrderAPITestCase (4+ tests)
- [ ] OrderItemAPITestCase (3+ tests)
- [ ] ReviewAPITestCase (4+ tests)
- [ ] ClientAPITestCase (tests basiques)
- [ ] SupplierAPITestCase (tests basiques)

TOTAL : 25+ tests à créer

⏱️ TEMPS ESTIMÉ : 3-4 heures
🎯 DIFFICULTÉ : Moyenne

💡 COMMANDES POUR LANCER LES TESTS :

# Tous les tests
python manage.py test

# Tests d'une seule classe
python manage.py test app.tests.CategoryAPITestCase

# Un seul test
python manage.py test app.tests.CategoryAPITestCase.test_create_category

# Avec verbosité
python manage.py test --verbosity=2

# Avec coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Génère un rapport HTML
"""
