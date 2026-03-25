from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from analytics.views import (
    CentreCoutViewSet, ChargeViewSet, CleRepartitionViewSet,
    CalculViewSet, ExerciceViewSet, CompteChargeViewSet,
    FonctionViewSet, CentreResponsabiliteViewSet, ProduitViewSet, ActiviteViewSet,
    HopitalViewSet, UserViewSet, HopitalRoleViewSet
)

router = DefaultRouter()

# ========== API ROUTES ==========

router.register(r'exercices', ExerciceViewSet)
router.register(r'centres-couts', CentreCoutViewSet)
router.register(r'comptes-charges', CompteChargeViewSet)
router.register(r'charges', ChargeViewSet)
router.register(r'cles-repartition', CleRepartitionViewSet)
router.register(r'calcul', CalculViewSet, basename='calcul')
router.register(r'fonctions', FonctionViewSet)
router.register(r'centres-responsabilite', CentreResponsabiliteViewSet)
router.register(r'produits', ProduitViewSet)
router.register(r'activites', ActiviteViewSet)
router.register(r'hopitaux', HopitalViewSet)
router.register(r'utilisateurs', UserViewSet)
router.register(r'hopital-roles', HopitalRoleViewSet)

# ========== VUES PROTÉGÉES ==========

@login_required
def accueil_view(request):
    """Vue d'accueil principale"""
    return render(request, 'analytics/accueil.html')

@login_required
def configuration_view(request):
    """Vue de configuration annuelle"""
    return render(request, 'analytics/configuration.html')

@login_required
def saisie_view(request):
    """Vue de saisie des données"""
    return render(request, 'analytics/saisie.html')

@login_required
def resultats_view(request):
    """Vue des résultats analytiques"""
    return render(request, 'analytics/resultats.html')

@login_required
def utilisateurs_view(request):
    """Vue de gestion des utilisateurs - Contrôleur uniquement"""
    return render(request, 'analytics/utilisateurs.html')

@login_required
def roles_permissions_view(request):
    """Vue dédiée à la gestion des rôles et permissions."""
    return render(request, 'analytics/roles_permissions.html')

@login_required
def info_session(request):
    """Retourne les infos de la session courante (utilisateur, rôle, exercice actif)"""
    from django.http import JsonResponse
    from analytics.models import Exercice
    user = request.user
    role_code = ''
    role_libelle = ''
    hopital_nom = ''
    hopital_id = None
    if hasattr(user, 'profile'):
        role_code = user.profile.role
        role_libelle = user.profile.get_role_display()
        if user.profile.hopital:
            hopital_nom = user.profile.hopital.nom
            hopital_id = user.profile.hopital.id
        elif user.profile.hopital_role and user.profile.hopital_role.hopital:
            hopital_nom = user.profile.hopital_role.hopital.nom
            hopital_id = user.profile.hopital_role.hopital.id

    exercice_queryset = Exercice.objects.filter(est_actif=True, est_clos=False)
    if hopital_id:
        exercice_queryset = exercice_queryset.filter(hopital_id=hopital_id)
    exercice = exercice_queryset.order_by('-annee').first()
    return JsonResponse({
        'user': user.get_full_name() or user.username,
        'username': user.username,
        'role': role_libelle,
        'role_code': role_code,
        'is_superuser': user.is_superuser,
        'hopital': hopital_nom,
        'hopital_id': hopital_id,
        'exercice': exercice.annee if exercice else None,
        'exercice_id': exercice.id if exercice else None,
        'exercice_actif': exercice is not None and not exercice.est_clos,
    })

urlpatterns = [
    path('api/', include(router.urls)),
    
    # ========== AUTHENTIFICATION =========
    
    path('login/', auth_views.LoginView.as_view(template_name='analytics/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    
    # ========== PAGES PROTÉGÉES =========
    
    path('accueil/', accueil_view, name='accueil'),
    path('configuration/', configuration_view, name='configuration'),
    path('saisie/', saisie_view, name='saisie'),
    path('resultats/', resultats_view, name='resultats'),
    path('utilisateurs/', utilisateurs_view, name='utilisateurs'),
    path('roles-permissions/', roles_permissions_view, name='roles_permissions'),
    path('api/info-session/', info_session, name='info_session'),
    path('', auth_views.LoginView.as_view(template_name='analytics/login.html')),
]