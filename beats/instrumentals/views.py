# instrumentals/views.py
from django.shortcuts import render
from .models import Beat  # Import the correct model

def beatlist(request):
    Beats = Beat.objects.all()  # Fetch all Beat instances
    return render(request, 'instrumentals/beatlist.html', {'beat': beat})  # Ensure correct path

