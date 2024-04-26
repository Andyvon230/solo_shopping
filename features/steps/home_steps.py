from behave import given, when, then
from django.test import Client
from django.urls import reverse
from plotly.graph_objs.layout.xaxis.rangeselector._button.Button import step

from mall.models import Cart

client = Client()


@given('I am on the home page')
def step_impl(context):
    context.response = client.get('/')


@then('I should see the merchandise list')
def step_impl(context):
    assert 'merchandise' in context.response.context


@given('I enter "{input}" in the search field')
def step_impl(context, input):
    context.search_input = input


@when('I submit the search form')
def step_impl(context):
    context.response = client.get(f'/?search_input={context.search_input}')


@then('I should see the search results')
def step_impl(context):
    assert 'search_input' in context.response.context


@given('I am logged in')
def step_impl(context):
    # Log in the user
    context.client.force_login(context.user)


@when('I add {quantity} of item {item_id} to the cart')
def step_impl(context, quantity, item_id):
    # Add the item to the cart
    url = reverse('add_to_cart', args=[item_id])
    context.response = context.client.post(url, data={'quantity': quantity})


@then('I should see the item in my cart')
def step_impl(context):
    # Check that the item is in the cart
    cart = Cart.objects.get(user=context.user, merchandise_id=context.item_id)
    assert cart.quantity == int(context.quantity)


@given("the user is not logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is not logged in')


@then('the response should be "User not logged in" with status code 403')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the response should be "User not logged in" with status code 403')


@when("the cart function is called")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the cart function is called')


@given("the user is logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is logged in')


@step("the user has valid carts")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user has valid carts')


@then('the response should render the "carts/cart.html" template with the correct carts and total price')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Then the response should render the "carts/cart.html" template with the correct carts and total price')


@step("the user has invalid carts")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user has invalid carts')


@step("an exception occurs during execution")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And an exception occurs during execution')


@then("the response should be an error message with status code 500")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the response should be an error message with status code 500')