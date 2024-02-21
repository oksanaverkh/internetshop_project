from django import forms
from . models import Product, Order

PAYMENT_CHOICES = [
    ('C', 'Cash'),
    ('P', 'PayPal')
]

COLOR_CHOICES = [
    ('White', 'Белый'),
    ('Black', 'Черный'),
    ('Red', 'Красный'),
    ('Blue', 'Синий'),
    ('Green', 'Зеленый'),
    ('Yellow', 'Желтый'),
    ('Purple', 'Пурпурный'),
    ('Brown', 'Коричневый'),
    ('Gray', 'Серый'),
    ('Pink', 'Розовый'),
    ('Orange', 'Оранжевый'),
    ('Beige', 'Бежевый'),
]

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class LoginForm(forms.Form):
    name = forms.CharField(label='Имя пользователя', max_length=100)
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput, min_length=6)


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Имя пользователя', max_length=100)
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    telephone = forms.CharField(label='Телефон', max_length=12)
    address = forms.CharField(label='Адрес доставки', max_length=100)


class SearchForm(forms.Form):
    size = forms.ChoiceField(label='Размер', choices=[(
        38, 38), (40, 40), (42, 42), (44, 44), (46, 46), (48, 48), (50, 50), (52, 52)])


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'color',
                  'description', 'price', 'size', 'quantity']
    category = forms.ChoiceField(label='Категория', choices=[(
        'M', 'Мужские футболки'), ('F', 'Женские футболки')])
    color = forms.ChoiceField(label='Цвет', choices=COLOR_CHOICES)
    size = forms.ChoiceField(label='Размер', choices=[(
        38, 38), (40, 40), (42, 42), (44, 44), (46, 46), (48, 48), (50, 50), (52, 52)])


class OrderForm(forms.Form):
    delivery_address = forms.CharField(
        label='Введите адрес доставки, если он отличается от адреса в личном кабинете', required=False)
    payment_option = forms.ChoiceField(label='Выберите способ оплаты',
                                       widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class ImageForm(forms.Form):
    image = forms.ImageField(label='Загрузите изображение', required=False)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='Введите старый пароль', widget=forms.PasswordInput, min_length=6)
    new_password1 = forms.CharField(
        label='Введите новый пароль', widget=forms.PasswordInput, min_length=6)
    new_password2 = forms.CharField(
        label='Повторите новый пароль', widget=forms.PasswordInput, min_length=6)


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        label='Количество', choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
