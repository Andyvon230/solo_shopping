from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import plotly.graph_objs as go
from django.db.models import Sum

from mall.models import *


def home(request):
    search_input = request.GET.get('search_input')
    mer_list = Merchandise.objects.all().select_related(
        'main_category', 'sub_category'
    ).prefetch_related('discount_id', 'ratings_id')
    if search_input:
        mer_list = mer_list.filter(name__icontains=search_input)

    is_empty = False
    if mer_list.count() == 0:
        is_empty = True

    paginator = Paginator(mer_list, 12)  # Show 10 merchandise per page.
    page_number = request.GET.get('page')
    try:
        merchandise = paginator.page(page_number)
    except PageNotAnInteger:
        merchandise = paginator.page(1)
    except EmptyPage:
        merchandise = paginator.page(paginator.num_pages)

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
    if not request.user.is_authenticated:
        return HttpResponse("User not logged in", status=403)

    try:
        carts = Cart.objects.filter(user=request.user, is_valid=True)
        total_price = 0.00
        for mer in carts:
            mer_discount = MerchandiseDiscount.objects.filter(merchandise=mer.merchandise, is_valid=True).first()
            if mer_discount:
                mer_discount.merchandise.price = mer.discount
                total_price += mer.discount * mer.quantity
            else:
                total_price += mer.merchandise.price * mer.quantity
        return render(request, 'carts/cart.html', {'carts': carts, 'total_price': total_price})
    except AttributeError as e:
        return HttpResponse("AttributeError occurred: " + str(e), status=500)
    except Exception as e:
        return HttpResponse("An error occurred: " + str(e), status=500)


def confirm_checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    with transaction.atomic():
        try:
            carts = Cart.objects.filter(user=request.user, is_valid=True)
            if not carts.exists():
                messages.error(request, "There are no items in your cart.")
                return redirect('cart')

            # Create order
            total_price = request.POST.get('total_price')
            order = Order.objects.create(total_price=total_price, create_user=request.user)

            # Create order items
            for mer in carts:
                mer_discount = MerchandiseDiscount.objects.filter(merchandise=mer.merchandise, is_valid=True).first()
                OrderItem.objects.create(
                    order=order,
                    merchandise=mer.merchandise,
                    price=mer.merchandise.price if not mer_discount else mer_discount.merchandise.price,
                    quantity=mer.quantity
                )

                # Optionally, remove items from cart or mark as invalid
                mer.is_valid = False
                mer.save()

            messages.success(request, "Your order has been placed successfully.")
            return redirect('success')

        except Exception as e:
            # Handle exceptions and possibly roll back the transaction
            messages.error(request, f"Error completing your order: {str(e)}")
            return redirect('cart')


def success(request):
    return render(request, 'carts/success.html')


@login_required
def order_list(request):
    if not request.user.is_staff:  # Checks if the user is not an admin
        return redirect('home')

    # Fetch all orders (admin sees all orders)
    orders = Order.objects.all().order_by('-created_at')

    is_empty = False
    if orders.count() == 0:
        is_empty = True

    paginator = Paginator(orders, 20)  # Show 10 merchandise per page.

    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    # Pass the orders to the template
    return render(request, 'admn/order_list.html', {'orders': orders, 'is_empty': is_empty})


@login_required
def order_detail(request, order_id):
    if not request.user.is_staff:  # Ensure only admin can access
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)

    return render(request, 'admn/order_detail.html', {'order': order})


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
                    login(request, user)
                    return HttpResponseRedirect(reverse('admin_home'))
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


def admin_home(request):
    return render(request, 'admn/admin_home.html')


def generate_pie_chart():
    # Fetch sales data
    data = OrderItem.objects.values('merchandise__name').filter(order__created_at__range=(datetime.now() - timedelta(days=30), datetime.now())).annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

    # Prepare data for the pie chart
    names = [item['merchandise__name'] for item in data]
    values = [item['total_quantity'] for item in data]

    # Create the pie chart
    fig = go.Figure(data=go.Pie(labels=names, values=values))

    return fig.to_html(full_html=False)


def admin_charts(request):
    div = generate_pie_chart()
    return render(request, 'admn/admin_charts.html', {'pie_div': div})
