from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages

from mall.models import *


def home(request):
    search_input = request.GET.get('search_input')
    if search_input:
        mer_list = Merchandise.objects.filter(name__icontains=search_input).select_related('main_category',
                                                                                           'sub_category').prefetch_related(
            'discount_id', 'ratings_id')
    else:
        mer_list = Merchandise.objects.all().select_related('main_category', 'sub_category').prefetch_related(
            'discount_id', 'ratings_id')

    is_empty = False
    if mer_list.count() == 0:
        is_empty = True

    paginator = Paginator(mer_list, 12)  # Show 10 merchandise per page.

    page_number = request.GET.get('page')
    merchandise = paginator.get_page(page_number)

    return render(request, 'mall/home.html', {
        'search_input': search_input,
        'merchandise': merchandise,
        'is_empty': is_empty
    })


def add_to_cart(request, item_id):
    # Determine if the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        try:
            # Here you would add logic to add the item to the cart
            merchandise = get_object_or_404(Merchandise, id=item_id)
            quantity = request.POST.get('quantity', 1)
            cart, created = Cart.objects.get_or_create(user=request.user, merchandise=merchandise)
            if not created:
                cart.quantity += int(quantity)
                cart.save()
            messages.success(request, "Successfully added to cart!")
        except Exception as e:
            print(e)
        return redirect('home')  # Redirect back to home page


def cart(request):
    carts = Cart.objects.filter(user=request.user, is_valid=True)
    total_price = 0.00
    for cart in carts:
        merchandise = MerchandiseDiscount.objects.filter(merchandise=cart.merchandise, is_valid=True).first()
        if merchandise:
            cart.merchandise.price = merchandise.discount
            total_price += merchandise.discount * cart.quantity
        else:
            total_price += cart.merchandise.price * cart.quantity
    return render(request, 'carts/cart.html', {'carts': carts, 'total_price': total_price})


def checkout(request):
    return render(request, 'carts/checkout.html')


def confirm_checkout(request):
    return redirect('success')


def success(request):
    return render(request, 'carts/success.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Redirect based on user type
                if user.is_superuser:
                    messages.warning(request, "If you are an admin, please click `Admin Login` to login.")
                    return redirect('login')
                else:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
    else:
        form = AuthenticationForm()
    return render(request, 'mall/login.html', {'form': form})


def user_logout(request):
    # Logout the user
    logout(request)
    # Redirect to the logout page
    return render(request, 'mall/logout.html')


def admin_charts(request):
    return render(request, 'mall/admin_charts.html')
