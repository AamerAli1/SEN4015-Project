from datetime import datetime
from http.client import HTTPResponse
import random
import string

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError

from .forms import ContactForm
from .models import Movie, list, MovieList,  UserProfile, CATEGORY_CHOICES

stripe.api_key = settings.STRIPE_SECRET_KEY


def login_form(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("product_catalog_app:movies")
            else:
                pass
        

    return render(request,'account/login.html')


def index(request):
    """The home page for product_catalog_app"""
    return render(request, 'index.html')

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def movies(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request, "movies.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid





@login_required
def HomeView(request,category_slug=None):
    
    category = None
    categories = CATEGORY_CHOICES.objects.all()
    data = Movie.objects.all()
    if category_slug:
        category = get_object_or_404(CATEGORY_CHOICES,slug=category_slug)
        data = Movie.objects.filter(category=category)
    if 'q' in request.GET:
        q = request.GET['q']
        if category != None :
            data = Movie.objects.filter(title__icontains=q,category=category)
        else:
            data = Movie.objects.filter(title__icontains=q)
 

    return render(request, 'home.html', {'categories':categories,
                                              'category':category,
                                              'movies':data,
                                              })




class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            movieList = MovieList.objects.get(user=self.request.user, added=False)
            context = {
                'object': movieList
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Movie
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    order_item, created = list.objects.get_or_create(
        movie=movie,
        user=request.user,
        added=False,
    )
    order_qs = MovieList.objects.filter(user=request.user, added=False)

    if order_qs.exists():
        movieList = order_qs[0]
        # check if the order item is in the order
        if movieList.movies.filter(movie__slug=movie.slug).exists():
            movieList.date_added = timezone.now()
            movieList.movies.add(order_item)
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The Movie have been addded to your Watchlist ")
            return redirect("product_catalog_app:movies")
        else:
            movieList.date_added = timezone.now()
            movieList.movies.add(order_item)
            movieList.save()
            messages.info(request, "The Movie have been addded to your Watchlist")
            return redirect("product_catalog_app:movies")
    else:
        date_added = timezone.now()
        movieList = MovieList.objects.create(
            user=request.user, date_added=date_added)
        movieList.movies.add(order_item)
        messages.info(request, "The Movie have been addded to your Watchlist ")
        return redirect("product_catalog_app:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Movie, slug=slug)
    order_qs = MovieList.objects.filter(
        user=request.user,
        added=False
    )
    if order_qs.exists():
        movieList = order_qs[0]
        # check if the order item is in the order
        if movieList.movies.filter(movie__slug=item.slug).exists():
            order_item = list.objects.filter(
                movie=item,
                user=request.user,
                added=False
            )[0]
            movieList.movies.remove(order_item)
            order_item.delete()
            messages.info(request, "The movie have been removed from your watchlist")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This movie was not in your watchlist")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "Your Watchlist is empty")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Movie, slug=slug)
    order_qs = MovieList.objects.filter(
        user=request.user,
        added=False
    )
    if order_qs.exists():
        movieList = order_qs[0]
        # check if the order item is in the order
        if movieList.movies.filter(item__slug=item.slug).exists():
            order_item = list.objects.filter(
                item=item,
                user=request.user,
                added=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                movieList.movies.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)




def waitingPage(request):
    return render(request,"waitingPage.html")


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'name': form.cleaned_data['name'], 
			'email_address': form.cleaned_data['email_address'], 
            'topic': form.cleaned_data['topic'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, from_email, ['admin@example.com'])
			except BadHeaderError:
				return HTTPResponse('Invalid header found.')
			return redirect ("product_catalog_app/index.html")
      
	form = ContactForm()
	return render(request, "product_catalog_app/index.html", {'form':form})
