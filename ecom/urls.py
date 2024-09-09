from django.urls import path
from ecom.views import homepage
from ecom.views import productsee
from ecom.views import about1
from ecom.views import account
from ecom.views import cart
from ecom.views import contact1
from ecom.views import wishlist
from ecom.views import blog

urlpatterns = [
      # pages
      path("", homepage.home, name="home"),   
      path("blog/", homepage.blog, name="blog"), 
      path("faq/",homepage.faq,name="faq"),
      path ("payment/",homepage.payment,name="payment"),
      path("about/", about1.about, name="about"),
      path("contact/", contact1.contact, name="contact"),
      
      # wishlist
      path("add_to_wishlist/", wishlist.add_to_wishlist, name="add_to_wishlist"),
      path("add_to_cart_from_wishlist/<int:product_id>/", wishlist.add_to_cart_from_wishlist, name="add_to_cart_from_wishlist"),
      path("remove_from_wishlist/", wishlist.remove_from_wishlist, name="remove_from_wishlist"),
      path("wishlist/", wishlist.wishlist, name="wishlist"),
      
      # product
      path("product/", productsee.product, name="product"),
      path("category/<id>/", productsee.product_category, name="product_category"),
      path("product/<id>/", productsee.product_detail, name="product_detail"),
      
      # account
      path("dashboard/", account.dashboard, name="dashboard"),
      path("signup/", account.signup_view, name="signup"),
      path("login/", account.LoginView.as_view(), name="login"),
      path("logout/", account.logout_view, name="logout"),
      path("forgot_password/", account.forgot_password, name="forgot"),
      path("edit_address/", account.edit_address, name="edit_address"),
      path("update_account/", account.update_account, name="update_account"),
      path("activate/<str:uidb64>/<str:token>/", account.activate, name="activate"),
      
      # cart
      path("cart/", cart.cart, name="cart"),
      path("add_to_cart/", cart.add_to_cart, name="add_to_cart"),
      path("update_cart/", cart.update_cart, name="update_cart"),
      path("remove_cart/", cart.remove_cart, name="remove_cart"),
      path("checkout/", cart.checkout, name="checkout"),
      path("payment_process/<id>", cart.payment_process, name="payment_process"),

      
      # blog
      path("blog/", blog.blog_list, name="blog_list"),
      path("blog/<int:post_id>/", blog.blog_detail, name="blog_detail"),
      path("blog/<int:post_id>/add_comment/", blog.add_comment, name="add_comment"),
      
]
