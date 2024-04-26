from behave import given, when, then
from django.test import Client
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.db import transaction


@given('the user is not authenticated')
def step_impl(context):
    context.client = Client()


@given('the user is authenticated')
def step_impl(context):
    context.client = Client()
    context.user = context.create_user()
    context.login(context.user)


@given('the cart is empty')
def step_impl(context):
    context.carts = []


@given('the cart is not empty')
def step_impl(context):
    context.carts = [context.create_cart()]


@when('the user attempts to confirm checkout')
def step_impl(context):
    context.response = context.client.post(reverse('confirm_checkout'), data={'total_price': 100})


@when('the user confirms checkout')
def step_impl(context):
    with transaction.atomic():
        context.carts = Cart.objects.filter(user=context.user, is_valid=True)
        if not context.carts.exists():
            context.fail("Cart is empty")
        total_price = sum([cart.merchandise.price * cart.quantity for cart in context.carts])
        context.response = context.client.post(reverse('confirm_checkout'), data={'total_price': total_price})


@then('they should be redirected to the login page')
def step_impl(context):
    assert context.response.status_code == 302
    assert context.response['location'] == reverse('login')


@then('they should see an error message')
def step_impl(context):
    assert 'There are no items in your cart.' in context.response.content.decode()


@then('they should be redirected to the cart page')
def step_impl(context):
    assert context.response.status_code == 302
    assert context.response['location'] == reverse('cart')


@then('their order should be placed successfully')
def step_impl(context):
    assert 'Your order has been placed successfully.' in context.response.content.decode()


@then('they should be redirected to the success page')
def step_impl(context):
    assert context.response.status_code == 302
    assert context.response['location'] == reverse('success')


@when("the checkout process encounters an error")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the checkout process encounters an error')