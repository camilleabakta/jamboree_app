# cotisations/admin.py
from django.contrib import admin
from .models import UserProfile, Cotisation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'total_cotise', 'pourcentage_avance')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_editable = ('role',)

@admin.register(Cotisation)
class CotisationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'montant', 'date_paiement', 'methode_paiement')
    list_filter = ('methode_paiement', 'date_paiement')
    search_fields = ('participant__username',)
    autocomplete_fields = ['participant']