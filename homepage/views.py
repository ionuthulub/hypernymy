from django.shortcuts import render


def homepage(request):
    context = {}
    return render(request, 'homepage/homepage.html', context)
