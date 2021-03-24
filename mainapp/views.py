from django.shortcuts import render, reverse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .models import Category, Product, SubCategory, Review, ReturnLetter, ReturnItem, SpecificationValue
from .mixins import LeftSideBarMixin
from .forms import ProductForm, SearchForm, populate_form_choice_fields, ReturnLetterForm, ReturnItemFormset

from cart.views import get_cart
from cart.models import CartItem

SORT_CHOICES = [
        ('-ratting', 'По умолчанию'),
        ('title', 'Наименование (А -> Я)'),
        ('-title', 'Наименование (Я -> А)'),
        ('-ratting', 'Рейтинг (по убыванию)'),
        ('ratting', 'Рейтинг (по возростанию)'),
        ('-price', 'Цена (по убыванию)'),
        ('price', 'Цена (по возрастанию)')
    ]

class HomePageView(LeftSideBarMixin, View):

    def get(self, request):
        context = self.get_context_data()

        high_ratting_products_for_main_slider = []
        for category in Category.objects.all():
            products = category.get_all_products()[:2]
            high_ratting_products_for_main_slider.append(tuple(products))

        side_products = Product.objects.all().order_by('-ratting').exclude(in_stock=False)[:5]
        most_popular_products = Product.objects.all().order_by('-ratting').exclude(in_stock=False)[:10]
        recent_products = Product.objects.filter(category__category__title='Новинки').order_by('-ratting').exclude(in_stock=False)[:10]
        cart = get_cart(request)

        context['high_ratting_products_for_main_slider'] = high_ratting_products_for_main_slider
        context['side_products'] = side_products
        context['most_popular_products'] = most_popular_products
        context['recent_products'] = recent_products
        context['cart'] = cart

        return render(request, 'home.html', context)

class CategoryProductsListView(LeftSideBarMixin, View):

    def get(self, request, slug):
        context = self.get_context_data()
        cart = get_cart(request)

        current_category = Category.objects.get(slug=slug)
        products = current_category.get_all_products()

        form = SearchForm(request.GET)
        form.fields['sort'].choices = SORT_CHOICES
        if form.is_valid():
            if form.cleaned_data['title']:
                products = products.filter(title__icontains=form.cleaned_data['title']).filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price']).order_by(form.cleaned_data['sort'])
            else:
                if form.cleaned_data['sort']:
                    products = products.filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price']).order_by(form.cleaned_data['sort'])
                else:
                    products = products.filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price'])
        paginator = Paginator(products, 15)
        page_number = int(request.GET.get('page', 1))

        try:
            page_products = paginator.page(page_number)
        except EmptyPage:
            page_products = paginator.page(1)

        if page_number - 6 >= 0:
            page_range = list(paginator.page_range)[page_number - 6:page_number + 5]
            if len(page_range) < 11:
                index = 11 - len(page_range)
                page_range = list(paginator.page_range)[page_number - 6 - index:page_number + 5]
        else:
            page_range = list(paginator.page_range)[:page_number + 9]


        context['slug'] = slug
        context['current_category'] = current_category
        context['products'] = page_products
        context['page_range'] = page_range
        context['cart'] = cart
        context['form'] = form

        return render(request, 'category_products.html', context)

class SubcategoryProductsListView(LeftSideBarMixin, View):

    def get(self, request, category_slug, subcategory_slug):
        context = self.get_context_data()
        cart = get_cart(request)

        current_category = Category.objects.get(slug=category_slug)
        current_subcategory = SubCategory.objects.get(category=current_category, slug=subcategory_slug)
        products = current_subcategory.get_all_products()

        form = SearchForm(request.GET)
        form.fields['sort'].choices = SORT_CHOICES
        if form.is_valid():
            if form.cleaned_data['title']:
                products = products.filter(title__icontains=form.cleaned_data['title']).filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price']).order_by(form.cleaned_data['sort'])
            else:
                if form.cleaned_data['sort']:
                    products = products.filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price']).order_by(form.cleaned_data['sort'])
                else:
                    products = products.filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price'])
        paginator = Paginator(products, 15)
        page_number = int(request.GET.get('page', 1))

        try:
            page_products = paginator.page(page_number)
        except EmptyPage:
            page_products = paginator.page(1)

        if len(list(paginator.page_range)) <= 10:
            page_range = paginator.page_range
        elif page_number - 6 >= 0:
            page_range = list(paginator.page_range)[page_number - 6:page_number + 5]
            if len(page_range) < 11:
                index = 11 - len(page_range)
                page_range = list(paginator.page_range)[page_number - 6 - index:page_number + 5]
        else:
            page_range = list(paginator.page_range)[:page_number + 9]

        context['slug'] = category_slug
        context['subcategory_slug'] = subcategory_slug
        context['current_category'] = current_category
        context['current_subcategory'] = current_subcategory
        context['products'] = page_products
        context['page_range'] = page_range
        context['cart'] = cart
        context['form'] = form

        return render(request, 'subcategory_products.html', context)

class SearchView(LeftSideBarMixin, View):

    def get(self, request):
        context = self.get_context_data()
        cart = get_cart(request)
        search_query = request.GET['search_query']

        products = Product.objects.filter(title__icontains=search_query).exclude(in_stock=False)

        form = SearchForm(request.GET)
        form.fields['sort'].choices = SORT_CHOICES
        if form.is_valid():
            if form.cleaned_data['title']:
                products = products.filter(title__icontains=form.cleaned_data['title']).filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price']).order_by(form.cleaned_data['sort'])
            else:
                if form.cleaned_data['sort']:
                    products = products.filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price']).order_by(form.cleaned_data['sort'])
                else:
                    products = products.filter(price__gte=form.cleaned_data['from_price'], price__lte=form.cleaned_data['to_price'])
        paginator = Paginator(products, 15)
        page_number = int(request.GET.get('page', 1))

        try:
            page_products = paginator.page(page_number)
        except EmptyPage:
            page_products = paginator.page(1)

        if len(list(paginator.page_range)) <= 10:
            page_range = paginator.page_range
        elif page_number - 6 >= 0:
            page_range = list(paginator.page_range)[page_number - 6:page_number + 5]
            if len(page_range) < 11:
                index = 11 - len(page_range)
                page_range = list(paginator.page_range)[page_number - 6 - index:page_number + 5]
        else:
            page_range = list(paginator.page_range)[:page_number + 9]

        context['products'] = page_products
        context['page_range'] = page_range
        context['cart'] = cart
        context['form'] = form
        context['search_query'] = search_query

        return render(request, 'search_products.html', context)

class ProductDetailView(View):

    def get(self, request, category_slug, subcategory_slug, id):
        context = {}
        current_category = Category.objects.get(slug=category_slug)
        current_subcategory = SubCategory.objects.get(category=current_category, slug=subcategory_slug)
        current_product = Product.objects.get(id=id)
        related_products = current_product.get_related_products()
        reviews = current_product.reviews.all()
        current_product_rating = current_product.rounded_ratting()
        cart = get_cart(request)

        form = ProductForm()
        form = populate_form_choice_fields(form, current_product)

        context['current_category'] = current_category
        context['current_subcategory'] = current_subcategory
        context['current_product'] = current_product
        context['related_products'] = related_products
        context['reviews'] = reviews
        context['current_product_rating'] = current_product_rating
        context['cart'] = cart
        context['form'] = form

        return render(request, 'product_detail.html', context)

    def post(self, request, category_slug, subcategory_slug, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('product_detail', args=[category_slug, subcategory_slug, id]))
        form = ProductForm(request.POST)

        context = {}
        current_category = Category.objects.get(slug=category_slug)
        current_subcategory = SubCategory.objects.get(category=current_category, slug=subcategory_slug)
        current_product = Product.objects.get(id=id)
        related_products = current_product.get_related_products()
        reviews = current_product.reviews.all()
        current_product_rating = current_product.rounded_ratting()
        cart = get_cart(request)

        form = populate_form_choice_fields(form, current_product)

        context['current_category'] = current_category
        context['current_subcategory'] = current_subcategory
        context['current_product'] = current_product
        context['related_products'] = related_products
        context['reviews'] = reviews
        context['current_product_rating'] = current_product_rating
        context['cart'] = cart
        context['form'] = form

        if form.is_valid():
            quantity = int(form.cleaned_data['quantity'])
            size = form.cleaned_data.get('size', '')
            color = form.cleaned_data.get('color', '')

            item, created = CartItem.objects.get_or_create(cart=cart, product=current_product, size=size, color=color)
            item.quantity = quantity
            item.save()

            messages.info(request, f'{current_product.title} X {quantity}, добавлено в корзину')
        return render(request, 'product_detail.html', context)

class ProductReviewView(View):

    def post(self, request):
        redirect_url = request.GET.get('redirect', reverse('home'))
        if request.user.is_authenticated:
            product_id = request.POST['product_id']
            product = Product.objects.get(id=product_id)
            edit = request.POST.get('edit', False)
            user = request.user

            ratting, review = self.validate_ratting_and_review(request)

            try:
                if edit:
                    review_edit = Review.objects.get(product=product, user=user)
                    if ratting and review:
                        review_edit.ratting = ratting
                        review_edit.review = review
                        review_edit.save()
                        messages.success(request, 'Ваш отзыв успешно отредактирован')
                else:
                    Review.objects.get(product=product, user=user)
                    messages.error(request, 'Вы уже оставили Ваш отзыв под этим продуктом ранее')
            except Review.DoesNotExist:
                Review.objects.create(product=product, user=user, ratting=ratting, review=review)
                messages.success(request, 'Ваш отзыв успешно добавлен')
        else:
            messages.success(request, 'Неавторизованые пользователи не могут оставлять комментарии')

        return HttpResponseRedirect(redirect_url)

    def validate_ratting_and_review(self, request):

        ratting = request.POST.get('ratting', None)
        review = request.POST.get('review', None)

        if ratting:
            ratting = int(request.POST['ratting'])
        else:
            messages.error(request, 'Вы забыли поставить оценку нашему продукту. Это является обязательным, если Вы оставляете отзыв')

        if review:
            review = request.POST['review']
        else:
            messages.error(request, 'Вы забыли написать текст отзыва. Это является обязательным, если Вы оставляете отзыв')

        return ratting, review

class DeleteReviewView(View):

    def post(self, request):
        redirect_url = request.GET.get('redirect', reverse('home'))
        if request.user.is_authenticated:
            review_id = int(request.POST['review_id'])
            review = Review.objects.get(id=review_id)
            if review.user == request.user:
                review.delete()
                messages.success(request, 'Ваш отзыв был успешно удалён')
            else:
                messages.error(request, 'Это не ваш отзыв. Вы не можете его удалить')
        else:
            messages.error(request, 'Вы не можете удалить отзыв, поскольку Вы неавторизированы')
        return HttpResponseRedirect(redirect_url)

class ShippingPolicyView(View):

    def get(self, request):
        context = {}
        cart = get_cart(request)
        context['cart'] = cart

        return render(request, 'information/shipping_policy.html', context)

class PaymentPolicyView(View):

    def get(self, request):
        context = {}
        cart = get_cart(request)
        context['cart'] = cart

        return render(request, 'information/payment_policy.html', context)

class ReturnPolicyView(View):

    def get(self, request):
        context = {}
        cart = get_cart(request)
        context['cart'] = cart

        return render(request, 'information/return_policy.html', context)

class ReturnLetterView(View):

    def get(self, request):
        context = {}
        cart = get_cart(request)

        form = ReturnLetterForm()
        formset = ReturnItemFormset()

        context['cart'] = cart
        context['form'] = form
        context['formset'] = formset

        return render(request, 'information/return_letter.html', context)

    def post(self, request):
        context = {}
        cart = get_cart(request)
        form = ReturnLetterForm(request.POST)
        formset = ReturnItemFormset(request.POST)

        context['cart'] = cart
        context['form'] = form
        context['formset'] = formset
        if form.is_valid():
            return_letter, created = ReturnLetter.objects.get_or_create(
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                receive_order_date=form.cleaned_data['receive_order_date'],
                order_number=form.cleaned_data['order_number'],
                bank_card_number=form.cleaned_data['bank_card_number'],
                fml_card_owner=form.cleaned_data['fml_card_owner'],
                comment=form.cleaned_data['comment']
            )
            if formset.is_valid():
                for data in formset.cleaned_data:
                    if data:
                        item = ReturnItem(
                            return_letter=return_letter,
                            product_name=data['product_name'],
                            quantity=data['quantity'],
                            total_price=data['total_price'],
                            return_reason=data['return_reason']
                        )
                        item.save()

                messages.info(request, 'Ваше заявление на возврат товара успешно отправлено')
                message, html_message = self.get_message_and_html_message_for_mail(return_letter)
                send_mail(
                    subject=f'Заявление на возврат от {return_letter.first_name} {return_letter.last_name}',
                    message=message,
                    from_email=None,
                    recipient_list=[settings.ADMIN_EMAIL],
                    html_message=html_message,
                )
        return render(request, 'information/return_letter.html', context)

    def get_message_and_html_message_for_mail(self, return_letter):
        """Принимает return_letter и возвращает (message, html_message)"""
        r = return_letter
        message = (
            f"""
            ФИО отправителя письма: {r.last_name} {r.first_name} {r.middle_name}
            
            Электронная почта отправителя письма: {r.email}
            
            Номер телефона отправителя письма: {r.phone_number}
            
            Дата получения заказа: {r.receive_order_date}
            
            № заказа (или номер ТТН «Новой Почты»): {r.order_number}
            
            Номер банковской карты: {r.bank_card_number}
            
            ФИО владельца банковской карты: {r.fml_card_owner}
            
            Комментарий: {r.comment}
            """
        )
        html_message = (
            f"""
            <p>ФИО отправителя письма: {r.last_name} {r.middle_name} {r.last_name}</p>
            <br>
            <p>Электронная почта отправителя письма: {r.email}</p>
            <br>
            <p>Номер телефона отправителя письма: {r.phone_number}</p>
            <br>
            <p>Дата получения заказа: {r.receive_order_date}</p>
            <br>
            <p>№ заказа (или номер ТТН «Новой Почты»): {r.order_number}</p>
            <br>
            <p>Номер банковской карты: {r.bank_card_number}</p>
            <br>
            <p>ФИО владельца банковской карты: {r.fml_card_owner}</p>
            <br>
            <p>Комментарий: {r.comment}</p>
            <br>
            <table class="table">
                <caption>Список товаров</caption>
                <thead>
                    <tr>
                        <th scope="col">№</th>
                        <th scope="col">Наименование</th>
                        <th scope="col">Кол-во, шт.</th>
                        <th scope="col">Цена, грн.</th>
                        <th scope="col">Код причины возвращения</th>
                    </tr>
                </thead>
                <tbody>
            """
        )
        for index, item in enumerate(r.items.all()):
            item_number = index + 1
            message += f'\n{item.product_name} {item.quantity}шт. {item.total_price}грн. {item.return_reason}'
            html_message += (
                f"""
                <tr>
                    <td>{item_number}</td>
                    <td>{item.product_name}</td>
                    <td>{item.quantity}</td>
                    <td>{item.total_price}</td>
                    <td>{item.return_reason}</td>
                </tr>
                """
            )
        html_message += (
            f"""
                </tbody>
            </table>
            """
        )
        return message, html_message

class PrivacyPolicyView(View):

    def get(self, request):
        context = {}
        cart = get_cart(request)
        context['cart'] = cart
        context['shop_domain_name'] = settings.SHOP_DOMAIN_NAME

        return render(request, 'information/privacy_policy.html', context)

class ClothesSizeView(View):

    def get(self, request):
        context = {}
        cart = get_cart(request)
        context['cart'] = cart

        return render(request, 'information/clothes_size.html', context)
