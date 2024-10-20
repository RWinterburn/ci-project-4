from django.shortcuts import render

def index(request):
    return render(request, 'base.html')  # This will render 'home.html', which can extend 'base.html'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def beats(request):
    return render(request, 'beatlist.html')
