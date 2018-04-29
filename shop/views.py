from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Category, Product, Review
from cart.forms import CartAddProductForm
from shop.forms import ReviewForm
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from googletrans import Translator
import json
from watson_developer_cloud import ToneAnalyzerV3

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


class analyzedReview:

    def __init__(self, Reviews):

        self.reviews = Reviews
        self.positive = 0
        self.negative = 0

        tone_analyzer = ToneAnalyzerV3(username='4828dab9-6dc5-4a9a-bf75-2dd195a7b49b', password='YDDAFGJuLrtg', version='2016-05-19 ')
        for review in self.reviews:
            to_analyze = review.text
            toneObj= json.dumps(tone_analyzer.tone(tone_input=to_analyze, content_type="text/plain"), indent=2)
            review.toneObj2 = json.loads(toneObj)
            review.angerScore = review.toneObj2['document_tone']['tone_categories'][0]['tones'][0]['score']
            review.disgustScore = review.toneObj2['document_tone']['tone_categories'][0]['tones'][1]['score']
            review.fearScore = review.toneObj2['document_tone']['tone_categories'][0]['tones'][2]['score']
            review.joyScore = review.toneObj2['document_tone']['tone_categories'][0]['tones'][3]['score']
            review.sadScore = review.toneObj2['document_tone']['tone_categories'][0]['tones'][4]['score']

            if (review.angerScore + review.disgustScore + review.fearScore + review.sadScore > review.joyScore ):
                self.negative = self.negative + 1
            else:
                self.positive = self.positive + 1

    def getReviews(self):
        return self.reviews

    def getPositive(self):
        return self.positive

    def getNegative(self):
        return self.negative



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
                  'shop/product/other_languages.html',
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
                  'shop/product/other_languages.html',
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
                  'shop/product/other_languages.html',
                  {'product': target_product,
                   'cart_product_form': cart_product_form,
                    'reviews':reviews})


def product_detail(request, id, slug):
    target_product = get_object_or_404(Product,
                                    id=id,
                                    slug=slug,
                                    available=True)
    cart_product_form = CartAddProductForm()
    main_reviews = Review.objects.all().filter(product=target_product)
    reviews = analyzedReview(main_reviews).getReviews()
    print("The positive are:", analyzedReview(main_reviews).getPositive() )
    return render(request,
                  'shop/product/detail.html',
                  {'product': target_product,
                   'cart_product_form': cart_product_form,
                    'reviews':reviews,
                    'positive':analyzedReview(main_reviews).getPositive(),
                    'negative':analyzedReview(main_reviews).getNegative()})

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
