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
from .models import Item, OrderItem, Order,  UserProfile, CATEGORY_CHOICES

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
                return redirect("product_catalog_app:products")
            else:
                pass
        

    return render(request,'account/login.html')


def index(request):
    """The home page for product_catalog_app"""
    return render(request, 'index.html')

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


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
    data = Item.objects.all()
    if category_slug:
        category = get_object_or_404(CATEGORY_CHOICES,slug=category_slug)
        data = Item.objects.filter(category=category)
    if 'q' in request.GET:
        q = request.GET['q']
        if category != None :
            data = Item.objects.filter(title__icontains=q,category=category)
        else:
            data = Item.objects.filter(title__icontains=q)
 

    return render(request, 'home.html', {'categories':categories,
                                              'category':category,
                                              'products':data,
                                              })




class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order.ordered_date = timezone.now()
            order.items.add(order_item)
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The Movie have been addded to your Watchlist ")
            return redirect("product_catalog_app:products")
        else:
            order.ordered_date = timezone.now()
            order.items.add(order_item)
            order.save()
            messages.info(request, "The Movie have been addded to your Watchlist")
            return redirect("product_catalog_app:products")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "The Movie have been addded to your Watchlist ")
        return redirect("product_catalog_app:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
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
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
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
