from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def handler404(request, exception):
    return render(request, 'handler404.html', status=404)


def login(request):
    errors = False

    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        user = auth.authenticate(username=login, password=password)
        if not (user is None):
            auth.login(request, user)
            return redirect('note_create')

        user = auth.authenticate(email=login, password=password)
        if not (user is None):
            auth.login(request, user)
            return redirect('note_create')

        errors = True

    context = {
        'errors': errors
    }

    return render(request, 'notes/notes_list.html', context)


def logout(request):
    auth.logout(request)
    return redirect('login')


def sign_up(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).count():
            context['error_username'] = True
        else:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            auth.login(request, user)

            return redirect('note_create')

    return render(request, 'notes/notes_list.html', context)