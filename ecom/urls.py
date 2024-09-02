from django.urls import path
from ecom import views

urlpatterns = [
      path("", views.home, name="home"),
      path("product/", views.product, name="product"),
      path('category/<int:id>/', views.product_category, name='product_category'),
      path('product/<int:id>/', views.product_detail, name='product_detail'),
      path("service/", views.service, name="service"),
      path("blog/", views.blog, name="blog"),
      path("product/<slug:slug>/", views.product_detail, name="product_detail"),
      path("about/", views.about, name="about"),
      path("contact/", views.contact, name="contact"),
      path("signup/", views.signup_view, name="signup"),
      path("login/", views.login_view, name="login"),
      path("forgot_password/", views.forgot_password, name="forgot"),
      path('wishlist/', views.wishlist, name='wishlist'),
      path("cart/", views.cart, name="cart"),
      path("update_cart/", views.update_cart, name="update_cart"),
      path("remove_cart/", views.remove_from_cart, name="remove_cart"),
      path("checkout/", views.checkout, name="checkout"),
      path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
]
