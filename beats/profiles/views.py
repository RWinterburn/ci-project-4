from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.
@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Optionally create a profile if it doesn't exist
        profile = Profile.objects.create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})