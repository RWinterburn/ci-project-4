from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Beat, Producer
from .forms import BeatForm


def beat_list(request):
    beats = Beat.objects.all()  
    is_admin = request.user.is_authenticated and request.user.is_staff  
    return render(request, 'instrumentals/beatlist.html', {'beats': beats, 'is_admin': is_admin})

def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin)
def add_beat(request):
    if request.method == 'POST':
        form = BeatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('beats')  
    else:
        form = BeatForm()
    return render(request, 'instrumentals/add_beat.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def delete_beat(request, beat_id):
    beat = get_object_or_404(Beat, id=beat_id)
    if request.method == 'POST':
        beat.delete()
        return redirect('beats')  # Redirect to the beat list page after deletion
    return render(request, 'instrumentals/delete_beat.html', {'beat': beat})


@login_required
@user_passes_test(is_admin)
def edit_beat(request, beat_id):

    beat = get_object_or_404(Beat, id=beat_id)

    if request.method == 'POST':

        form = BeatForm(request.POST, request.FILES, instance=beat)
        if form.is_valid():
            form.save()
            return redirect('beats')  
    else:

        form = BeatForm(instance=beat)

    return render(request, 'instrumentals/edit_beat.html', {'form': form, 'beat': beat})
