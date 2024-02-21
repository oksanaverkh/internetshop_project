from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from . forms import LoginForm, RegistrationForm, SearchForm, ProductForm, OrderForm, ImageForm, ChangePasswordForm, CartAddProductForm
from . models import User, Order, Product, Cart, CartItem
import logging


logger = logging.getLogger(__name__)


def index(request):
    logger.info('Main page accessed')
    products = list(reversed(Product.objects.all()))[:6]
    return render(request, template_name='shop_app/main.html', context={'products': products})


'''
    Представления для работы с пользовательскими аккаунтами
'''


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']

            user = User.objects.filter(name=name).first()

            if user is None:
                return redirect('registration')
            else:

                if check_password(password, user.password):
                    message = f'Добрый день, {name}'
                    logger.info(f'Пользователь {user} вошел в систему')
                    request.session['user_id'] = user.pk
                    return redirect('welcome', user.pk)
                else:
                    message = f'Введен некорректный пароль'
                    form = LoginForm()
                    logger.info(f'Пользователь {user} ввел некорректный пароль')
                    return render(request, 'shop_app/users/login.html', {'form': form, 'message': message})
    else:
        form = LoginForm()
        message = 'Введите имя пользователя и пароль'
    return render(request, 'shop_app/users/login.html', {'form': form, 'message': message})

def catalogue(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    product_man = Product.objects.filter(pk=1).first()
    img_data_man = product_man.image.url
    product_woman = Product.objects.filter(pk=2).first()
    img_data_woman = product_woman.image.url

    return render(request, 'shop_app/prods/catalogue.html', {'user': user, 'img_data_man': img_data_man, 'img_data_woman':img_data_woman})

def welcome(request, user_id):
    message = 'Добро пожаловать!'
    user = User.objects.filter(pk=user_id).first()
    return render(request, 'shop_app/welcome.html', {'message': message, 'user': user})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            telephone = form.cleaned_data['telephone']
            address = form.cleaned_data['address']
            if User.objects.filter(name__iexact=name):
                message = 'Пользователь c таким именем уже зарегистрирован'
                return render(request, 'shop_app/users/registration.html', {'form': form, 'message': message})

            user = User(name=name, email=email, password=password,
                        telephone=telephone, address=address)
            user.save()
            user.set_password(password)
            user.save()
            message = 'Пользователь успешно сохранён'

            logger.info(f'Пользователь {user} сохранен')
            return redirect('login_user')
    else:
        form = RegistrationForm()
        message = 'Заполните форму регистрации'
    return render(request, 'shop_app/users/registration.html', {'form': form, 'message': message})


def logout(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    logger.info(f'Пользователь {user.name} вышел из системы')
    return redirect('index')


def show_user_card(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    return render(request, 'shop_app/users/user.html', context={'user': user})


def change_password(request, user_id):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            user = User.objects.filter(pk=user_id).first()
            old_password = form.cleaned_data['old_password']
            if not check_password(old_password, user.password):
                message = 'Введен некорректный пароль'
                form = ChangePasswordForm()
                logger.info(f'Пользователь {user} ввел некорректный пароль')
                return render(request, 'shop_app/users/change_password.html', {'form': form, 'message': message})
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 != new_password2:
                message = 'Пароли не совпадают'
                form = ChangePasswordForm()
                logger.info(f'Пользователь {user} ввел не совпадающие пароли')
                return render(request, 'shop_app/users/change_password.html', {'form': form, 'message': message})
            user.set_password(new_password1)
            user.save()
            return redirect('password_updated', user_id)

    else:
        form = ChangePasswordForm()
        message = 'Изменение пароля'
    return render(request, 'shop_app/users/change_password.html', {'form': form, 'message': message})


def password_updated(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    return render(request, 'shop_app/users/password_updated.html', context={'user': user})


'''
    Прдеставления для работы с товаром
'''


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            color = form.cleaned_data['color']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']

            product = Product(name=name, category=category, color=color,
                              description=description, price=price, size=size, quantity=quantity)
            product.save()
            logger.info(f'Товар {product} сохранен')
            return redirect('upload_image', product.pk)

    else:
        form = ProductForm()
        message = 'Заполните форму'
    return render(request, 'shop_app/prods/product.html', {'form': form, 'message': message})


def upload_image(request, product_id):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        message = 'Ошибка данных'
        if form.is_valid():
            product = Product.objects.filter(pk=product_id).first()
            image = form.cleaned_data['image']
            fs = FileSystemStorage()

            product.image = fs.save(image.name, image)
            product.save()
            logger.info(f'Изображение товара {product} сохранено')
            return redirect('all_products')
    else:
        form = ImageForm()
        message = 'Загрузите изображение'
    return render(request, 'shop_app/prods/upload_image.html', {'form': form, 'message': message})


def all_products(request, user_id, category):
    user = User.objects.filter(pk=user_id).first()
    if category=='M':
        products = Product.objects.filter(category='Мужские футболки').all()
    else:
        products = Product.objects.filter(category='Женские футболки').all()
    return render(request, 'shop_app/prods/product_list.html', context={'products': products, 'user': user})


def search(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        message = 'Некорректный ввод'
        if form.is_valid():
            size = form.cleaned_data['size']


            products = Product.objects.filter(size=size)

            logger.info(f'Список товаров отображен пользователю')
            message = 'По заданным критериям товары не найдены'
            return render(request, 'shop_app/prods/product_list.html', context={'products': products, 'user': user, 'message': message})

    else:
        form = SearchForm()
        message = 'Выберите размер'
    return render(request, 'shop_app/prods/search.html', {'form': form, 'message': message, 'user': user})


def show_product_card(request, user_id, product_id):
    user = User.objects.filter(pk=user_id).first()
    product = Product.objects.filter(pk=product_id).first()
    img_data = product.image.url

    return render(request, 'shop_app/prods/product_card.html', context={'user': user, 'product': product, 'img_data': img_data, })


def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form_instance = form.save(commit=False)
        form_instance.id = product.id
        form_instance.save()
        return redirect('product_card', product.pk)
    return render(request, 'shop_app/prods/edit_product.html', {'form': form})


'''
    Представления для работы с корзиной
'''


def add_to_cart(request, user_id, product_id):
    product = Product.objects.filter(pk=product_id).first()
    img_data = product.image.url
    user = User.objects.filter(pk=user_id).first()

    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if product.quantity < quantity:
                message = f'Недостаточное количество товара на складе, осталось {
                    product.quantity} штук'
                form = CartAddProductForm()
                return render(request, 'shop_app/orders/cart_add.html', {'form': form, 'message': message, 'product': product, 'img_data': img_data, 'user': user})

            cart_item = CartItem(
                product=product, quantity=quantity, cart_item_price=product.price*quantity)
            cart_item.save()
            print(cart_item)

            cart = Cart.objects.filter(user=user).first()

            if cart is None:
                products = set()
                products.add(cart_item)
                cart = Cart(user=user)
                cart.save()
                print(cart)
                cart.products.set(products)
                print(cart.products)
            else:
                cart.add_item(product, quantity)

            cart.save()
            print(cart)
            logger.info(f'Корзина {cart} пользователя {user} сохранена')
            return redirect('cart', user_id, cart.pk)

    else:
        message = 'Выберите количество товара'
        form = CartAddProductForm()
    return render(request, 'shop_app/orders/cart_add.html', {'form': form, 'message': message, 'product': product, 'user': user})


def cart(request, user_id, cart_id):
    cart = Cart.objects.filter(pk=cart_id).first()
    user = User.objects.get(pk=user_id)
    items = cart.products.all()

    return render(request, 'shop_app/orders/cart.html', {'cart': cart, 'user': user, 'items': items})


def cart_remove(request, user_id, cart_id, product_id):
    cart = Cart.objects.filter(pk=cart_id).first()
    product = Product.objects.get(pk=product_id)

    cart.remove_item(product)
    cart.save()
    return redirect('cart', user_id, cart_id)


def cart_clear(request, user_id, cart_id):
    cart = Cart.objects.filter(pk=cart_id).first()

    if cart is None:
        user = User.objects.get(pk=user_id)
        return render(request, template_name='shop_app/main.html', context={'user': user})
    else:
        cart.clear()
        return redirect('cart_empty', user_id)


def cart_empty(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, template_name='shop_app/orders/cart_empty.html', context={'user': user})


'''
    Представления для работы с заказами
'''


def checkout(request, user_id, cart_id):
    user = User.objects.filter(pk=user_id).first()
    cart = Cart.objects.filter(pk=cart_id).first()
    products_in_cart = cart.products.all()
    print(products_in_cart)
    products = set()

    for item in products_in_cart:
        products.add(item.product)
        product = Product.objects.filter(pk=item.product.id).first()
        product.quantity -= item.quantity
        product.save()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(user=user, total_price=cart.get_total_price(), delivery_address=user.address, payment_option='P', status='Создан')
            order.save()
            order.products.set(products)
            print(order.products)
            order.save()
            delivery_address = form.cleaned_data['delivery_address']
            if delivery_address:
                order.delivery_address = delivery_address
            order.payment_option = form.cleaned_data['payment_option']
            order.status = 'Ожидает оплаты'
            order.save()

            return redirect('payment', user_id, order.pk, cart_id)
    else:
        form = OrderForm()

    return render(request, 'shop_app/orders/checkout.html', {'form': form, 'user': user, 'products': products_in_cart, 'cart': cart})


def payment(request, user_id, order_id, cart_id):
    order = Order.objects.filter(pk=order_id).first()
    user = User.objects.filter(pk=user_id).first()

    cart = Cart.objects.filter(pk=cart_id).first()

    order.status = 'оплачен'
    order.save()
    cart.clear()
    return render(request, 'shop_app/orders/payment.html', {'order': order, 'user': user})


def order_complete(request, user_id, order_id):
    user = User.objects.filter(pk=user_id).first()
    order = Order.objects.filter(pk=order_id).first()
    order.status = 'передан в доставку'
    order.save()
    return render(request, 'shop_app/orders/order_complete.html', {'order': order, 'user': user})


def get_user_orders(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    orders = Order.objects.filter(user=user).all()

    logger.info(f'Заказы пользователя {user} загружены')
    return render(request, template_name='shop_app/orders/order_list.html', context={'orders': orders, 'user': user, })


def show_order_card(request, user_id, order_id):
    order = Order.objects.filter(pk=order_id).first()
    user = User.objects.filter(pk=user_id).first()
    print(order)

    logger.info(f'Информация о заказе: {order}')
    return render(request, template_name='shop_app/orders/order_card.html', context={'order': order, 'user': user})


def get_order_products(request, user_id, order_id):
    order = Order.objects.filter(pk=order_id).first()
    user = User.objects.filter(pk=user_id).first()
    products = order.products.all()

    logger.info(f'Информация отоварах в заказе заказе: {order}')
    return render(request, template_name='shop_app/prods/product_list.html', context={'order': order, 'products': products, 'user': user})
