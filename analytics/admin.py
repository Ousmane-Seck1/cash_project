
"""Configuration Django Admin pour CASH - Comptabilité Analytique Hospitalière"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Hopital, Exercice, Fonction, CentreResponsabilite, CentreCout,
    CompteCharge, Charge, CleRepartition, Activite, Produit,
    ResultatCalcul, AuditLog, UserProfile, HopitalRole
)

# ========== CONFIGURATION DJANGO ADMIN =========

admin.site.site_title = "ADMINISTRATION CASH"
admin.site.site_header = "Comptabilité Analytique Hospitalitère - CASH"
admin.site.index_title = "Gestion opérationnelle"

# ========== GESTION DES UTILISATEURS =========

class UserProfileInline(admin.StackedInline):
    """Inline pour l'attribution de rôles"""
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    """Admin personnalisé pour les utilisateurs avec rôles"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        if not hasattr(obj, 'profile'):
            return '-'
        if obj.is_superuser:
            return 'Administrateur global'
        if obj.profile.hopital_role:
            return obj.profile.hopital_role.libelle
        return obj.profile.get_role_display()
    get_role.short_description = 'Rôle'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ========== CENTRES DE COÛTS ET CHARGES =========

@admin.register(CentreCout)
class CentreCoutAdmin(admin.ModelAdmin):
    """Admin pour les centres de coûts"""
    list_display = ['code', 'libelle', 'type_centre', 'ordre_cascade', 'est_actif']
    list_filter = ['type_centre', 'est_actif', 'centre_responsabilite__fonction']
    search_fields = ['code', 'libelle']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('centre_responsabilite__fonction')


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    """Admin pour les charges"""
    list_display = ['date', 'compte', 'montant', 'centre_cout', 'created_by']
    list_filter = ['exercice', 'date', 'centre_cout__type_centre']
    search_fields = ['designation', 'numero_be_bc']
    date_hierarchy = 'date'


@admin.register(CleRepartition)
class CleRepartitionAdmin(admin.ModelAdmin):
    """Admin pour les clés de répartition"""
    list_display = ['exercice', 'centre_source', 'centre_destination', 'pourcentage']
    list_filter = ['exercice']


@admin.register(ResultatCalcul)
class ResultatCalculAdmin(admin.ModelAdmin):
    """Admin pour les résultats de calcul"""
    list_display = [
        'centre_cout', 'charges_directes', 'charges_indirectes', 
        'charges_totales', 'produits', 'resultat_analytique'
    ]
    list_filter = ['exercice', 'centre_cout__type_centre']
    readonly_fields = [f.name for f in ResultatCalcul._meta.fields]


# ========== ENREGISTREMENT DES AUTRES MODÈLES =========

admin.site.register(Hopital)
admin.site.register(Exercice)
admin.site.register(Fonction)
admin.site.register(CentreResponsabilite)
admin.site.register(CompteCharge)
admin.site.register(Activite)
admin.site.register(AuditLog)


@admin.register(HopitalRole)
class HopitalRoleAdmin(admin.ModelAdmin):
    """Admin des rôles flexibles par hôpital"""
    list_display = ['hopital', 'code', 'libelle', 'est_actif']
    list_filter = ['hopital', 'est_actif']
    search_fields = ['code', 'libelle', 'hopital__nom', 'hopital__code']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    """Admin pour les produits"""
    list_display = ['centre_cout', 'periode', 'type_produit', 'montant', 'exercice']
    list_filter = ['exercice', 'type_produit', 'centre_cout__type_centre']
    search_fields = ['centre_cout__code', 'centre_cout__libelle']

