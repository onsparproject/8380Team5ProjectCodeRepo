from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Category, Product, Review
from cart.forms import CartAddProductForm
from shop.forms import ReviewForm
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from googletrans import Translator

class translatedReview:

    def __init__(self, Reviews, targetLanguage):

        self.reviews = Reviews
        self.target_language = targetLanguage


    def getTranslated(self):
        translator = Translator()
        for review in self.reviews:
            review.text = translator.translate(review.text, dest=self.target_language).text
            review.title = translator.translate(review.title,dest=self.target_language).text
        return self.reviews


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    for product in products:
        print(product.name)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                        'shop/product/list.html',
                        {'category': category,
                            'categories': categories,
                                'products': products})



def french(request, id):
    target_product = get_object_or_404(Product,
                                    id=id,
                                    available=True)
    cart_product_form = CartAddProductForm()
    reviews = Review.objects.all().filter(product=target_product)
    translatedObject =  translatedReview(reviews, 'fr').getTranslated()
    reviews = translatedObject
    return render(request,
                  'shop/product/detail.html',
                  {'product': target_product,
                   'cart_product_form': cart_product_form,
                    'reviews':reviews})


def spanish(request, id):
    target_product = get_object_or_404(Product,
                                    id=id,
                                    available=True)
    cart_product_form = CartAddProductForm()
    reviews = Review.objects.all().filter(product=target_product)
    translatedObject =  translatedReview(reviews, 'es').getTranslated()
    reviews = translatedObject
    return render(request,
                  'shop/product/detail.html',
                  {'product': target_product,
                   'cart_product_form': cart_product_form,
                    'reviews':reviews})


def hindi(request, id):
    target_product = get_object_or_404(Product,
                                    id=id,
                                    available=True)
    cart_product_form = CartAddProductForm()
    reviews = Review.objects.all().filter(product=target_product)
    translatedObject =  translatedReview(reviews, 'hi').getTranslated()
    reviews = translatedObject
    return render(request,
                  'shop/product/detail.html',
                  {'product': target_product,
                   'cart_product_form': cart_product_form,
                    'reviews':reviews})


def product_detail(request, id, slug):
    target_product = get_object_or_404(Product,
                                    id=id,
                                    slug=slug,
                                    available=True)
    cart_product_form = CartAddProductForm()
    reviews = Review.objects.all().filter(product=target_product)
    return render(request,
                  'shop/product/detail.html',
                  {'product': target_product,
                   'cart_product_form': cart_product_form,
                    'reviews':reviews})

@login_required
def add_review(request, id):
    cart_product_form = CartAddProductForm()
    target_product = get_object_or_404(Product,
                                    id=id,
                                    available=True)
    reviews = Review.objects.all().filter(product=target_product)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = target_product
            review.author = request.user
            review.published_date = timezone.now()
            review.save()
            return render(request,
                          'shop/product/detail.html',
                          {'product': target_product,
                           'cart_product_form': cart_product_form,
                            'reviews':reviews})
    else:
        form = ReviewForm()
    return render(request, 'shop/product/add_review.html', {'form': form})
