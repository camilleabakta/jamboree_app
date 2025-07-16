# cotisations/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal


class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrateur'
        PARTICIPANT = 'PARTICIPANT', 'Participant'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PARTICIPANT)
    objectif_cotisation = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('200000.00'))

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def total_cotise(self):
        total = self.user.cotisations.aggregate(Sum('montant'))['montant__sum']
        return total or Decimal('0.00')

    @property
    def pourcentage_avance(self):
        if self.objectif_cotisation > 0:
            return round((self.total_cotise / self.objectif_cotisation) * 100, 2)
        return Decimal('0.00')

    @property
    def reste_a_payer(self):
        return self.objectif_cotisation - self.total_cotise


class Cotisation(models.Model):
    class MethodePaiement(models.TextChoices):
        ESPECES = 'ESPECES', 'Espèces'
        MOBILE_MONEY = 'MOBILE_MONEY', 'Mobile Money'
        VIREMENT = 'VIREMENT', 'Virement Bancaire'
        AUTRE = 'AUTRE', 'Autre'

    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cotisations')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    methode_paiement = models.CharField(max_length=20, choices=MethodePaiement.choices, default=MethodePaiement.ESPECES)
    description = models.TextField(blank=True, null=True, help_text="Optionnel : motif du paiement")

    class Meta:
        ordering = ['-date_paiement']

    def __str__(self):
        return f"{self.participant.username} - {self.montant} F CFA le {self.date_paiement.strftime('%d/%m/%Y')}"