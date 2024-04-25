from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from mall.models import Merchandise


def home(request):
    mer_list = Merchandise.objects.all().select_related('main_category', 'sub_category')

    is_empty = False
    if mer_list.count() == 0:
        is_empty = True

    paginator = Paginator(mer_list, 12)  # Show 10 merchandise per page.

    page_number = request.GET.get('page')
    merchandise = paginator.get_page(page_number)

    return render(request, 'mall/home.html', {
        'merchandise': merchandise,
        'is_empty': is_empty
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.is_superuser:  # Assuming 'admin' is a superuser
                    return HttpResponseRedirect(reverse('admin_charts'))
                else:
                    return HttpResponseRedirect(reverse('mall/home.html'))
    else:
        form = AuthenticationForm()
    return render(request, 'mall/login.html', {'form': form})


def admin_charts(request):
    return render(request, 'mall/admin_charts.html')
