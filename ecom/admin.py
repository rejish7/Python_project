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
    filter_horizontal = ('products',)
    
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
    list_display = ('user', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username',)
    filter_horizontal = ('items',)

@admin.register(CheckoutAddress)
class CheckoutAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country', 'zip_code', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'city', 'state', 'country')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment_method', 'amount', 'transaction_id', 'status', 'created_at', 'updated_at')
    list_filter = ('payment_method', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'order__id', 'transaction_id')

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'address', 'payment', 'is_complete', 'created_at', 'updated_at')
    list_filter = ('is_complete', 'created_at', 'updated_at')
    search_fields = ('user__username', 'order__id')

@admin.register(Testimonials)
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