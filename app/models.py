from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError

# Catégorie de produits
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    

class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name
    
    def save(self,  *args, **kwargs):
        if not self.description:
            self.description =  f"Description de la catégorie : {self.name}."
        return super().save( *args, **kwargs)

# Produit vendu dans la boutique
class Product(BaseModel):
    name = models.CharField(max_length=150,db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(upload_to="products/", blank=True)
    stock = models.PositiveIntegerField(default=0)
    supplier=models.ManyToManyField('Supplier',related_name='products')
    
    class Meta:
        ordering=['name']
        verbose_name='Produit'
        verbose_name_plural='Produits'
        indexes =[models.Index(fields=['name', 'category'], name='product_name_category_idx')]
        
    # def clean(self):
    #     self.name = " ".join(self.name.split()).strip()
    #     if Product.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
    #         raise ValidationError({'name': f"Un produit nommé '{self.name}' existe déjà."})

        
        
    # def save(self, *args, **kwargs):
      
    #     self.full_clean()
    #     return super().save( *args, **kwargs)
    
    @property
    def in_stock(self):
        return self.stock > 0


    def __str__(self):
        return self.name

# Commande passée par un utilisateur
class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        CANCELLED = 'Cancelled', 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client =models.ForeignKey('Client',on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    products = models.ManyToManyField(Product, through="OrderItem", related_name="orders")
    
    class Meta:
        ordering=['-created_at']
        
    @property
    def total_price(self):
        """
        Calcule la somme des sous-totaux de tous les articles de la commande.
        """
        return sum(item.item_subtotal for item in self.items.all())
    
     
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

# Détail d'un produit dans une commande
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()    

    @property
    def item_subtotal(self):
        """
        Calcule le sous-total de cet article (prix * quantité).
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.order_id}"

# Avis laissé par un utilisateur sur un produit
class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']



# Client de la boutique
class Client(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def save(self, *args,**kwargs):
        if Client.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
            raise ValidationError(f"L'Email '{self.email}' existe déjà.")
        self.email = self.email
        
        return super().save(*args,**kwargs)
    
    @property
    def orders_subtotal(self):
        """
        Retourne le total des sous-totaux de toutes les commandes du client.
        """
        total = 0
        for order in self.orders.all():  # 'orders' vient du related_name dans Order
            total += order.total_price
        return total

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Fournisseur de produits
class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    

    def __str__(self):
        return self.name
