# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Category
# from django.contrib.auth.models import User


# class CategoryViewsTestCase(APITestCase):
#     """Tests des vues Detail et Delete pour Category"""

#     def setUp(self):
#         """Initialisation des données pour les tests"""
#         # Crée un utilisateur pour les tests d’authentification
#         # self.user = User.objects.create_user(username="testuser", password="1234555555")

#         # Crée une catégorie existante
#         self.category = Category.objects.create(
#             name="Electronique",
#             description="Appareils et accessoires électroniques"
#         )

#         # URLs dynamiques basées sur la clé primaire
#         self.detail_url = reverse("category-detail", args=[self.category.pk])
#         self.delete_url = reverse("category-delete", args=[self.category.pk])

#     def test_retrieve_category_detail(self):
#         """✅ Teste la récupération d'une catégorie (GET)"""
#         response = self.client.get(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["name"], "Electronique")

#     def test_retrieve_category_not_found(self):
#         """❌ Teste la récupération d'une catégorie inexistante"""
#         url = reverse("category-detail", args=[999])  # ID inexistant
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_delete_category_unauthenticated(self):
#         """🚫 Tentative de suppression sans authentification"""
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_delete_category_authenticated(self):
#         """✅ Suppression d'une catégorie avec authentification"""
#         self.client.login(username="testuser", password="12345")
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())
p ="fhh".split()
n=" ".join(p)
print(p)
print(n)