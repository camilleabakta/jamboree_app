# cotisations/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import UserRegistrationForm, CotisationForm
from .models import Cotisation, UserProfile, User
from .decorators import admin_required, participant_required


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            UserProfile.objects.create(user=new_user)
            messages.success(request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    if not hasattr(request.user, 'profile'):
        UserProfile.objects.create(user=request.user)

    if request.user.profile.role == 'ADMIN':
        return redirect('dashboard_admin')
    else:
        return redirect('dashboard_participant')


@login_required
@participant_required
def dashboard_participant(request):
    user = request.user
    cotisations = Cotisation.objects.filter(participant=user)

    if request.method == 'POST':
        form = CotisationForm(request.POST)
        if form.is_valid():
            cotisation = form.save(commit=False)
            cotisation.participant = user
            cotisation.save()
            messages.success(request, 'Votre cotisation a été ajoutée avec succès !')
            return redirect('dashboard_participant')
    else:
        form = CotisationForm()

    context = {
        'cotisations': cotisations,
        'profile': user.profile,
        'form': form,
    }
    return render(request, 'dashboards/participant_dashboard.html', context)


@login_required
@admin_required
def dashboard_admin(request):
    total_participants = UserProfile.objects.filter(role='PARTICIPANT').count()
    total_collecte = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
    objectif_global = total_participants * 200000
    pourcentage_global = (total_collecte / objectif_global * 100) if objectif_global > 0 else 0

    participants_profiles = UserProfile.objects.filter(role='PARTICIPANT').select_related('user').order_by(
        'user__username')

    context = {
        'total_participants': total_participants,
        'total_collecte': total_collecte,
        'objectif_global': objectif_global,
        'pourcentage_global': pourcentage_global,
        'participants_profiles': participants_profiles
    }
    return render(request, 'dashboards/admin_dashboard.html', context)