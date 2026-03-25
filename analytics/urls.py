from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from .views import (
    CentreCoutViewSet, ChargeViewSet, CleRepartitionViewSet, ActiviteViewSet, ProduitViewSet,
    CalculViewSet, ExerciceViewSet, CompteChargeViewSet, FonctionViewSet, CentreResponsabiliteViewSet,
    HopitalViewSet, UserViewSet, HopitalRoleViewSet
)


router = DefaultRouter()

# ========== ENREGISTREMENT DES VIEWSETS API ==========

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


# ========== VUES PRINCIPALES ==========

@login_required
def accueil_view(request):
    """Vue d'accueil principale du CASH"""
    return render(request, 'analytics/accueil.html')

@login_required
def configuration_view(request):
    """Vue de configuration annuelle"""
    return render(request, 'analytics/configuration.html')

@login_required
def utilisateurs_view(request):
    """Vue de gestion des utilisateurs - Contrôleur uniquement"""
    return render(request, 'analytics/utilisateurs.html')

@login_required
def roles_permissions_view(request):
    """Vue dédiée à la gestion des rôles et permissions."""
    return render(request, 'analytics/roles_permissions.html')

@login_required
def exercices_view(request):
    """Vue de gestion des exercices comptables"""
    return render(request, 'analytics/exercices.html')


@login_required
def saisie_view(request):
    """Vue de saisie des données"""
    return render(request, 'analytics/saisie.html')

@login_required
def resultats_view(request):
    """Vue des résultats analytiques"""
    return render(request, 'analytics/resultats.html')

# ========== AUTHENTIFICATION ==========

def login_simple(request):
    """Vue de connexion simple"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/accueil/')
        else:
            return render(request, 'analytics/login.html', {'error': 'Identifiants incorrects'})
    return render(request, 'analytics/login.html')


# ========== ROUTES ==========

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', login_simple, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('accueil/', accueil_view, name='accueil'),
    path('configuration/', configuration_view, name='configuration'),
        path('exercices/', exercices_view, name='exercices'),
    path('saisie/', saisie_view, name='saisie'),
    path('resultats/', resultats_view, name='resultats'),
    path('utilisateurs/', utilisateurs_view, name='utilisateurs'),
    path('roles-permissions/', roles_permissions_view, name='roles_permissions'),
    path('', login_simple),
]
