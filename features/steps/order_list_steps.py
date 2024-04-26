from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


@given('I am logged in as an admin')
def step_impl(context):
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
    context.client = Client()
    context.client.login(username='admin', password='password')
    context.admin_user = admin_user


@when('I visit the order list page')
def step_impl(context):
    context.response = context.client.get(reverse('order_list'))


@then('I should see the order list')
def step_impl(context):
    assert context.response.status_code == 200
    assert 'Order List' in context.response.content.decode()


@then('the order list should not be empty')
def step_impl(context):
    assert 'You have no orders.' not in context.response.content.decode()
