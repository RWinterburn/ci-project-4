from django.shortcuts import render
from instrumentals.models import Beat
from django.db.models import Q  # Adjust this import based on your project structure

from profiles.models import Profile

def index(request):
    return render(request, 'base.html')  # This will render 'home.html', which can extend 'base.html'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# views.py





# beats/views.py


def search(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    beats = Beat.objects.filter(
        Q(title__icontains=query) |
        Q(producer__icontains=query) |
        Q(description__icontains=query) |
        Q(price__icontains=query)
    ) if query else Beat.objects.all()  # Filter beats by multiple fields
    return render(request, 'search.html', {'beats': beats, 'query': query})


def beatlist(request):
    Beat = Beat.objects.all()
    return render(request, 'beatlist.html', {'beats': beats})