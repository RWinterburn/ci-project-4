from django.shortcuts import render, redirect, get_object_or_404
from .models import Beat

 # Import your Beat model

def beat_list(request):
    beats = Beat.objects.all()  # Fetch all Beat instances
    return render(request, 'instrumentals/beatlist.html', {'beats': beats})




