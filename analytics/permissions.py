"""
Permissions pour le contrôle d'accès à l'API analytique.

Définit les classes de permissions personnalisées pour les différents rôles :
- Contrôleur de gestion : accès complet
- Comptable analytique : accès limité
- Lecture seule : accès en consultation
"""
from rest_framework import permissions


def _has_configured_permission(user, permission_code, legacy_roles=None):
    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if not hasattr(user, 'profile'):
        return False

    profile = user.profile
    effective_permissions = set(profile.get_effective_permissions())
    if permission_code in effective_permissions:
        return True

    return profile.role in (legacy_roles or [])


# ========== PERMISSIONS PAR RÔLE ==========

class IsControleurGestion(permissions.BasePermission):
    """
    Permission pour le contrôleur de gestion.
    Le superuser passe toujours.
    """
    def has_permission(self, request, view):
        return _has_configured_permission(request.user, 'manage_configuration', legacy_roles=['controleur'])

class IsComptableAnalytique(permissions.BasePermission):
    """
    Permission pour le comptable analytique.
    """
    def has_permission(self, request, view):
        return _has_configured_permission(request.user, 'enter_charges', legacy_roles=['comptable'])


class CanManageUsers(permissions.BasePermission):
    """Permission pour la gestion des utilisateurs et rôles."""

    def has_permission(self, request, view):
        return _has_configured_permission(request.user, 'manage_users', legacy_roles=['controleur'])

class ReadOnly(permissions.BasePermission):
    """
    Permission lecture seule.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsGlobalAdmin(permissions.BasePermission):
    """Autorise uniquement le super administrateur global."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)


class CanRunSensitiveOperations(permissions.BasePermission):
    """Autorise les operations critiques pour superuser ou controleur configure."""

    def has_permission(self, request, view):
        return _has_configured_permission(
            request.user,
            'manage_configuration',
            legacy_roles=['controleur'],
        )