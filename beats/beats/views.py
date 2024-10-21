from django.shortcuts import render
from instrumentals.models import Beat  # Adjust this import based on your project structure



def index(request):
    return render(request, 'base.html')  # This will render 'home.html', which can extend 'base.html'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')






def beatlist(request):
    Beat = Beat.objects.all()
    return render(request, 'beatlist.html', {'beats': beats})