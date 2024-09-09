from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'show_logo', 'show_cover')

    def show_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="auto" />', obj.logo.url)
        return ''

    def show_cover(self, obj):
        if obj.cover:
            return format_html('<img src="{}" width="100" height="auto" />', obj.cover.url)
        return ''

    show_logo.short_description = 'Logo Preview'
    show_cover.short_description = 'Cover Preview'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'phone', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_filter = ['created_at']

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'text', 'show_image')

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return ''

    show_image.short_description = 'Image Preview'

@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at', 'show_image')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return ''

    show_image.short_description = 'Image Preview'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at', 'show_image')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return ''

    show_image.short_description = 'Image Preview'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username')

@admin.register(Bestselling)
class BestsellingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'show_image')
    
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return ''

    show_image.short_description = 'Image Preview'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('checkout', 'product', 'quantity', 'price')
    list_filter = ('checkout__created_at',)
    search_fields = ('checkout__user__username', 'product__name')

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'first_name', 'last_name', 'town_city', 'state_county', 'country', 'postcode', 'phone', 'email', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'town_city', 'state_county', 'country')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'checkout', 'payment_method', 'amount', 'transaction_id', 'status', 'created_at', 'updated_at')
    list_filter = ('payment_method', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'checkout__id', 'transaction_id')
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('username', 'description', 'show_image')
    
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return ''

    show_image.short_description = 'Image Preview'

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'product__name')
    
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question','answer')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at', 'show_image')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('title', 'author__username', 'content', 'tags', 'category')
    readonly_fields = ('created_at', 'updated_at')

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return ''

    show_image.short_description = 'Image Preview'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'author__username', 'content')
    readonly_fields = ('created_at',)
