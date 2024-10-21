from django.shortcuts import render
from .models import Beat  # Import your Beat model

def beat_list(request):
    beats = Beat.objects.all()  # Fetch all Beat instances
    return render(request, 'instrumentals/beatlist.html', {'beats': beats})

