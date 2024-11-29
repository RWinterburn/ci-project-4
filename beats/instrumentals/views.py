from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Beat
from .forms import BeatForm

 # Import your Beat model


def beat_list(request):
    beats = Beat.objects.all()  # Fetch all Beat instances
    is_admin = request.user.is_authenticated and request.user.is_staff  # Check if user is an admin
    return render(request, 'instrumentals/beatlist.html', {'beats': beats, 'is_admin': is_admin})

def is_admin(user):
    return user.is_authenticated and user.is_staff

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BeatForm
from .models import Beat

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def add_beat(request):
    if request.method == 'POST':
        form = BeatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('beats')  # Redirect to the beat list after adding
    else:
        form = BeatForm()
    return render(request, 'instrumentals/add_beat.html', {'form': form})

# Admin-only view for deleting a beat
@login_required
@user_passes_test(is_admin)
def delete_beat(request, beat_id):
    beat = get_object_or_404(Beat, id=beat_id)
    if request.method == 'POST':
        # If the user confirmed the deletion (POST request), delete the beat
        beat.delete()
          # Redirect to the beat list after deletion
        return render(request, 'instrumentals/delete_beat.html', {'beat': beat})
    return redirect('beats')



@login_required
@user_passes_test(is_admin)
def edit_beat(request, beat_id):
    # Fetch the beat to edit
    beat = get_object_or_404(Beat, id=beat_id)

    if request.method == 'POST':
        # Populate the form with POST data and files
        form = BeatForm(request.POST, request.FILES, instance=beat)
        if form.is_valid():
            form.save()
            return redirect('beats')  # Redirect to the beat list after editing
    else:
        # Initialize the form with the existing beat instance
        form = BeatForm(instance=beat)

    return render(request, 'instrumentals/edit_beat.html', {'form': form, 'beat': beat})
