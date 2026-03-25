
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator, MaxValueValidator


class Role(models.TextChoices):
    """Définition des rôles utilisateur"""
    CONTROLEUR_GESTION = 'controleur', 'Contrôleur de Gestion'
    DIRECTEUR = 'directeur', 'Directeur'
    RESPONSABLE_FINANCIER = 'responsable_financier', 'Responsable Financier'
    COMPTABLE_ANALYTIQUE = 'comptable', 'Comptable Analytique'
    AGENT_SAISIE = 'agent_saisie', 'Agent de Saisie'


class RolePermission(models.TextChoices):
    """Catalogue de permissions fonctionnelles."""
    MANAGE_USERS = 'manage_users', 'Gerer les utilisateurs'
    MANAGE_CONFIGURATION = 'manage_configuration', 'Configurer le referentiel'
    ENTER_CHARGES = 'enter_charges', 'Saisir les charges'
    ENTER_PRODUCTS = 'enter_products', 'Saisir les produits'
    ENTER_ACTIVITIES = 'enter_activities', 'Saisir les activites'
    RUN_CALCULATIONS = 'run_calculations', 'Executer les calculs'
    VIEW_RESULTS = 'view_results', 'Consulter les resultats'
    EXPORT_REPORTS = 'export_reports', 'Exporter les etats'


ROLE_DEFAULT_PERMISSIONS = {
    Role.CONTROLEUR_GESTION: [
        RolePermission.MANAGE_USERS,
        RolePermission.MANAGE_CONFIGURATION,
        RolePermission.ENTER_CHARGES,
        RolePermission.ENTER_PRODUCTS,
        RolePermission.ENTER_ACTIVITIES,
        RolePermission.RUN_CALCULATIONS,
        RolePermission.VIEW_RESULTS,
        RolePermission.EXPORT_REPORTS,
    ],
    Role.DIRECTEUR: [
        RolePermission.VIEW_RESULTS,
        RolePermission.EXPORT_REPORTS,
    ],
    Role.RESPONSABLE_FINANCIER: [
        RolePermission.VIEW_RESULTS,
        RolePermission.EXPORT_REPORTS,
        RolePermission.RUN_CALCULATIONS,
    ],
    Role.COMPTABLE_ANALYTIQUE: [
        RolePermission.ENTER_CHARGES,
        RolePermission.VIEW_RESULTS,
    ],
    Role.AGENT_SAISIE: [
        RolePermission.ENTER_CHARGES,
        RolePermission.ENTER_PRODUCTS,
        RolePermission.ENTER_ACTIVITIES,
    ],
}


class HopitalRole(models.Model):
    """Role configurable par hopital avec permissions selectionnables."""
    hopital = models.ForeignKey('Hopital', on_delete=models.CASCADE, related_name='roles')
    code = models.CharField(max_length=50)
    libelle = models.CharField(max_length=100)
    permissions = models.JSONField(default=list, blank=True)
    est_actif = models.BooleanField(default=True)

    class Meta:
        unique_together = ['hopital', 'code']
        ordering = ['hopital__nom', 'libelle']
        verbose_name = 'Role hopital'
        verbose_name_plural = 'Roles hopitaux'

    def __str__(self):
        return f"{self.hopital.nom} - {self.libelle}"

    def clean(self):
        from django.core.exceptions import ValidationError

        valid_codes = {choice[0] for choice in RolePermission.choices}
        invalid_codes = [code for code in (self.permissions or []) if code not in valid_codes]
        if invalid_codes:
            raise ValidationError({'permissions': f"Permissions invalides: {', '.join(invalid_codes)}"})

    @classmethod
    def permission_catalog(cls):
        return [
            {'code': code, 'libelle': libelle}
            for code, libelle in RolePermission.choices
        ]


class UserProfile(models.Model):
    """Profil utilisateur avec attribution de rôle et hôpital"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=30, choices=Role.choices)
    hopital_role = models.ForeignKey(
        'HopitalRole',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profiles',
        help_text='Role specifique defini pour cet hopital'
    )
    hopital = models.ForeignKey(
        'Hopital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Hôpital d'appartenance (vide = accès à tous les hôpitaux)"
    )

    def get_effective_permissions(self):
        if self.user.is_superuser:
            return [code for code, _ in RolePermission.choices]

        if self.hopital_role and self.hopital_role.est_actif:
            return list(self.hopital_role.permissions or [])

        return [str(code) for code in ROLE_DEFAULT_PERMISSIONS.get(self.role, [])]
    
    def __str__(self):
        hopital_str = self.hopital.nom if self.hopital else 'Tous hôpitaux'
        role_str = self.hopital_role.libelle if self.hopital_role else self.get_role_display()
        return f"{self.user.username} - {role_str} ({hopital_str})"


class Hopital(models.Model):
    """Information de l'hôpital (mono-établissement pour l'instant)"""
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    database_alias = models.CharField(max_length=100, blank=True, default='')
    database_name = models.CharField(max_length=255, blank=True, default='')
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name_plural = "Hopitaux"


class Exercice(models.Model):
    """Année comptable/exercice"""
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    annee = models.IntegerField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    est_actif = models.BooleanField(default=True)
    est_clos = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['hopital', 'annee']
        ordering = ['-annee']
    
    def __str__(self):
        return f"{self.hopital.nom} - {self.annee}"

class Fonction(models.Model):
    """Niveau 1 : Fonctions (94.1, 94.2, 94.3, 94.4)"""
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ['hopital', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.libelle}"


class CentreResponsabilite(models.Model):
    """Niveau 2 : Centres de responsabilité (ex: 94.1.2 SAF)"""
    fonction = models.ForeignKey(Fonction, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ['fonction', 'code']
        verbose_name_plural = "Centres de responsabilité"
    
    def __str__(self):
        return f"{self.code} - {self.libelle}"


class CentreCout(models.Model):
    """Niveau 3 : Centres de coûts finaux (éléments analysables)"""
    TYPE_CHOICES = [
        ('NT_UO', 'Non tarifaire avec Unité d\'Œuvre'),
        ('NT_TF', 'Non tarifaire avec Taux de Frais'),
        ('CT_MT', 'Tarifaire Médico-technique'),
        ('CT_CL', 'Tarifaire Clinique'),
    ]
    
    centre_responsabilite = models.ForeignKey(
        CentreResponsabilite, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    type_centre = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    # Pour les centres tarifaires
    unite_oeuvre = models.CharField(max_length=50, blank=True, 
                                   help_text="Ex: Nombre de consultations, journées d'hospitalisation")
    tarif = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Ordre pour la cascade (NT_TF)
    ordre_cascade = models.IntegerField(null=True, blank=True, 
                                       help_text="Ordre de déversement pour la méthode cascade")
    
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['centre_responsabilite', 'code']
        verbose_name_plural = "Centres de coûts"
        ordering = ['code']

    def clean(self):
        from django.core.exceptions import ValidationError

        types_avec_uo = {'NT_UO', 'CT_MT', 'CT_CL'}
        unite = (self.unite_oeuvre or '').strip()
        if self.type_centre in types_avec_uo and not unite:
            raise ValidationError({
                'unite_oeuvre': "L'unité d'oeuvre est obligatoire pour les centres NT_UO et tarifaires (CT_MT/CT_CL)."
            })

        types_tarifaires = {'CT_MT', 'CT_CL'}
        if self.type_centre in types_tarifaires and self.tarif is None:
            raise ValidationError({
                'tarif': "Le tarif est obligatoire pour les centres tarifaires (CT_MT/CT_CL)."
            })
    
    def __str__(self):
        return f"{self.code} - {self.libelle} ({self.get_type_centre_display()})"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def code_complet(self):
        if self.centre_responsabilite:
            return f"{self.centre_responsabilite.code}.{self.code}"
        return self.code


class CompteCharge(models.Model):
    """Plan comptable des charges analytiques"""
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ['hopital', 'numero']
        ordering = ['numero']
        verbose_name_plural = "Comptes de charges"

    def __str__(self):
        return f"{self.numero} - {self.libelle}"


class Charge(models.Model):
    """Saisie des charges incorporables"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Référence comptable
    numero_be_bc = models.CharField(max_length=30, blank=True, verbose_name="N° BE/BC")
    numero_op = models.CharField(max_length=30, blank=True, verbose_name="N° OP")
    numero_liquidation = models.CharField(max_length=30, blank=True, verbose_name="Liq")
    
    designation = models.CharField(max_length=180, verbose_name="Désignation")
    compte = models.ForeignKey(CompteCharge, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Imputation
    centre_cout = models.ForeignKey(CentreCout, on_delete=models.CASCADE)
    
    # Métadonnées
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='charges_crees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.date} - {self.compte} - {self.montant} - {self.centre_cout}"


class CleRepartition(models.Model):
    """Clés de répartition pour les centres NT_UO"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    centre_source = models.ForeignKey(
        CentreCout, 
        on_delete=models.CASCADE,
        related_name='cles_source',
        limit_choices_to={'type_centre': 'NT_UO'}
    )
    centre_destination = models.ForeignKey(
        CentreCout,
        on_delete=models.CASCADE,
        related_name='cles_destination'
    )
    pourcentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    class Meta:
        unique_together = ['exercice', 'centre_source', 'centre_destination']
        verbose_name = "Clé de répartition"
        verbose_name_plural = "Clés de répartition"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        from django.db.models import Sum

        if self.centre_source and self.centre_source.type_centre != 'NT_UO':
            raise ValidationError('Le centre source doit être un centre NT_UO.')

        if self.centre_source and self.centre_destination and self.centre_source == self.centre_destination:
            raise ValidationError('Le centre de destination ne peut pas être le même que le centre source.')

        total_existant = CleRepartition.objects.filter(
            exercice=self.exercice,
            centre_source=self.centre_source
        ).exclude(pk=self.pk).aggregate(total=Sum('pourcentage'))['total'] or 0

        if total_existant + self.pourcentage > 100:
            raise ValidationError('La somme des pourcentages pour ce centre source dépasse 100%.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.centre_source} → {self.centre_destination} : {self.pourcentage}%"


class Activite(models.Model):
    """Unités d'œuvre pour les centres tarifaires"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    centre_cout = models.ForeignKey(
        CentreCout,
        on_delete=models.CASCADE,
        limit_choices_to={'type_centre__in': ['CT_MT', 'CT_CL']}
    )
    periode = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Mois de saisie (1-12)"
    )
    volume = models.DecimalField(max_digits=15, decimal_places=2, 
                                help_text="Nombre d'unités d'œuvre")
    
    class Meta:
        unique_together = ['exercice', 'centre_cout', 'periode']
        ordering = ['centre_cout__code', 'periode']
    
    def __str__(self):
        return f"{self.centre_cout} - P{self.periode} - {self.volume} {self.centre_cout.unite_oeuvre}"


class Produit(models.Model):
    """Produits/Recettes par centre tarifaire"""
    TYPE_ORDINAIRE = 'ORDINAIRE'
    TYPE_SUPPLETIF = 'SUPPLETIF'
    TYPE_AUTRE = 'AUTRE'
    TYPE_SUBVENTION_EXPLOITATION = 'SUBVENTION_EXP'
    TYPE_AUTRE_SUBVENTION = 'AUTRE_SUBVENTION'
    TYPE_PRODUIT_CHOICES = [
        (TYPE_ORDINAIRE, 'Produits ordinaires'),
        (TYPE_SUPPLETIF, 'Produits suppletifs'),
        (TYPE_AUTRE, 'Autres produits'),
        (TYPE_SUBVENTION_EXPLOITATION, "Subvention d'exploitation"),
        (TYPE_AUTRE_SUBVENTION, 'Autres subventions'),
    ]

    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    centre_cout = models.ForeignKey(
        CentreCout,
        on_delete=models.CASCADE,
        limit_choices_to={'type_centre__in': ['CT_MT', 'CT_CL']}
    )
    periode = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Mois de saisie (1-12)"
    )
    type_produit = models.CharField(
        max_length=20,
        choices=TYPE_PRODUIT_CHOICES,
        default=TYPE_ORDINAIRE,
        help_text='Nature du produit saisi'
    )
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        unique_together = ['exercice', 'centre_cout', 'periode', 'type_produit']
        ordering = ['centre_cout__code', 'periode', 'type_produit']
    
    def __str__(self):
        return f"{self.centre_cout} - P{self.periode} - {self.get_type_produit_display()} - {self.montant}"


class ResultatCalcul(models.Model):
    """Stockage des résultats de calcul pour performance"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    centre_cout = models.ForeignKey(CentreCout, on_delete=models.CASCADE)
    
    # Charges
    charges_directes = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    charges_indirectes = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    charges_totales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Pour les centres tarifaires
    produits = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    volume_activite = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cout_revient_unitaire = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    resultat_analytique = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    date_calcul = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['exercice', 'centre_cout']
        verbose_name_plural = "Résultats de calcul"
    
    def __str__(self):
        return f"{self.centre_cout} - Charges: {self.charges_totales}"


class AuditLog(models.Model):
    """Journal d'audit pour tracer les modifications"""
    ACTION_CHOICES = [
        ('CREATE', 'Création'),
        ('UPDATE', 'Modification'),
        ('DELETE', 'Suppression'),
        ('CALCULATE', 'Calcul'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"

    def __str__(self):
        return f"{self.user.username} - {self.role}"