from django.urls import path
from ecom.views import homepage
from ecom.views import productsee
from ecom.views import about1
from ecom.views import account
from ecom.views import cart
from ecom.views import contact1
from ecom.views import wishlist

urlpatterns = [
      path("", homepage.home, name="home"),   
      path("blog/", homepage.blog, name="blog"), 
      path("faq/",homepage.faq,name="faq"),
      path ("payment/",homepage.payment,name="payment"),
      path("about/", about1.about, name="about"),
      path("contact/", contact1.contact, name="contact"),
      path('wishlist/', wishlist.wishlist, name='wishlist'),
      
      path("product/", productsee.product, name="product"),
      path('category/<id>/', productsee.product_category, name='product_category'),
      path('product/<id>/', productsee.product_detail, name='product_detail'),
      path("product/<slug:slug>/", productsee.product_detail, name="product_detail"),
      
      
      path("dashboard/", account.dashboard, name="dashboard"),
      path("signup/", account.signup_view, name="signup"),
      path("login/", account.login_view, name="login"),
      path("logout/", account.logout_view, name="logout"),
      path("forgot_password/", account.forgot_password, name="forgot"),
      path("edit_address/", account.edit_address, name="edit_address"),
      path("update_account/", account.update_account, name="update_account"),

      path("activate/<str:uidb64>/<str:token>/", account.activate, name="activate"),
      
      
      path("cart/", cart.cart, name="cart"),
      path("update_cart/", cart.update_cart, name="update_cart"),
      path("remove_cart/", cart.remove_cart, name="remove_cart"),
      path("checkout/", cart.checkout, name="checkout"),
      
      
]
