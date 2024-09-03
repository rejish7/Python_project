from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify




class Setting(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cover = models.ImageField(upload_to='logo/')
    logo = models.ImageField(upload_to='logo/')
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    google = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    youtube = models.CharField(max_length=100, null=True, blank=True)
    about = RichTextField()
    learn = RichTextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    phone = models.PositiveIntegerField(default=0)
    message = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.email}"
    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contact_us'

class Banner(models.Model):
    image = models.ImageField(upload_to='banner/')
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300)
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'


class CompanyService(models.Model):
    icon = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = RichTextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Company Service'
        verbose_name_plural = 'Company Services'
        

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=100)
    specifications = RichTextField()
    shipping_info = RichTextField()
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    products = models.ManyToManyField(Product, related_name='categories')
    image = models.ImageField(upload_to='category/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        

class Review(models.Model):
    
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES) # type: ignore
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
    
class Bestselling(models.Model):
    image = models.ImageField(upload_to='bestselling/',blank=True)
    title = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Cart Item: {self.product.name}"

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.user}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s address"

    class Meta:
        verbose_name = 'Checkout Address'
        verbose_name_plural = 'Checkout Addresses'

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('khalti', 'Khalti'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for Order {self.order.user}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.ForeignKey(CheckoutAddress, on_delete=models.SET_NULL, null=True)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checkout for Order {self.order}"

    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'
        
class Testimonials(models.Model):
    image = models.ImageField(upload_to='testimonials/',blank=True)
    username =models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Testimonials'
        verbose_name_plural = 'Testimonials'
    
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wishlist item for {self.user.username}: {self.product.name}"
    
    class Meta:
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'
        unique_together = ('user', 'product')


class FAQ(models.Model):
    question = RichTextField()
    answer = RichTextField()
    
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = 'faq'
        verbose_name_plural = 'faq'
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"Profile for {self.user.username}"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
