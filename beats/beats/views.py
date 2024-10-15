from django.shortcuts import render

def home(request):
    return render(request, 'base.html')  # This will render 'home.html', which can extend 'base.html'
