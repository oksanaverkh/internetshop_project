from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # URL-маршруты для работы с пользователями
    path('registration/', views.registration, name='registration'),
    path('login_user/', views.login_user, name='login_user'),
    path('welcome/<int:user_id>', views.welcome, name='welcome'),
    path('user_card/<int:user_id>', views.show_user_card, name='user_card'),
    path('change_password/<int:user_id>',
         views.change_password, name='change_password'),
    path('password_updated/<int:user_id>',
         views.password_updated, name='password_updated'),
    path('logout/<int:user_id>', views.logout, name='logout'),

    # URL-маршруты для работы с товарами
    path('catalogue/<int:user_id>', views.catalogue, name='catalogue'),
    path('all_products/<int:user_id>/<category>', views.all_products, name='all_products'),
    path('search/<int:user_id>', views.search, name='search'),
    path('product_card/<int:user_id>/<int:product_id>',
         views.show_product_card, name='product_card'),

     # Раскомментировать при необходимости добавления или редактирования товаров 
     # без использования административной панели

     # path('add_product/', views.add_product, name='add_product'), 
#     path('edit_product/<int:product_id>',
#          views.edit_product, name='edit_product'),
#     path('upload_image/<int:product_id>',
#          views.upload_image, name='upload_image'),

    # URL-маршруты для работы с заказами
    path('cart/<int:user_id>/<int:cart_id>', views.cart, name='cart'),
    path('cart_add/<int:user_id>/<int:product_id>',
         views.add_to_cart, name='cart_add'),
    path('cart_remove/<int:user_id>/<int:cart_id>/<int:product_id>',
         views.cart_remove, name='cart_remove'),
    path('cart_clear/<int:user_id>/<int:cart_id>', views.cart_clear, name='cart_clear'),
    path('cart_empty/<int:user_id>', views.cart_empty, name='cart_empty'),
    path('checkout/<int:user_id>/<int:cart_id>',
         views.checkout, name='checkout'),
    path('payment/<int:user_id>/<int:order_id>/<int:cart_id>', views.payment, name='payment'),
    path('order_complete/<int:user_id>/<int:order_id>',
         views.order_complete, name='order_complete'),
    path('get_user_orders/<int:user_id>',
         views.get_user_orders, name='get_user_orders'),
    path('show_order_card/<int:user_id>/<int:order_id>', views.show_order_card, name='show_order_card'),
    path('get_order_products/<int:user_id>/<int:order_id>', views.get_order_products, name='get_order_products'),

]
