
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Charge, CentreCout, CleRepartition, Activite, Produit,
    ResultatCalcul, Exercice, CompteCharge, Fonction, CentreResponsabilite, Hopital,
    UserProfile, Role, HopitalRole
)


class HopitalSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les hôpitaux"""
    class Meta:
        model = Hopital
        fields = '__all__'


class HopitalRoleSerializer(serializers.ModelSerializer):
    """Sérialiseur des rôles configurables par hôpital."""
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)

    class Meta:
        model = HopitalRole
        fields = ['id', 'hopital', 'hopital_nom', 'code', 'libelle', 'permissions', 'est_actif']

    def validate_permissions(self, value):
        valid_codes = {item['code'] for item in HopitalRole.permission_catalog()}
        invalid = [code for code in (value or []) if code not in valid_codes]
        if invalid:
            raise serializers.ValidationError(f"Permissions invalides: {', '.join(invalid)}")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la gestion des utilisateurs"""
    role = serializers.ChoiceField(choices=Role.choices, required=False)
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email', required=False, allow_blank=True)
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    is_active = serializers.BooleanField(source='user.is_active', required=False)
    is_superuser = serializers.BooleanField(source='user.is_superuser', required=False)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    hopital_nom = serializers.CharField(source='hopital.nom', read_only=True)
    hopital_role_libelle = serializers.CharField(source='hopital_role.libelle', read_only=True)
    role_libelle = serializers.SerializerMethodField()
    permissions_effectives = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_superuser', 'password', 'role', 'role_libelle',
            'hopital_role', 'hopital_role_libelle', 'hopital', 'hopital_nom',
            'permissions_effectives'
        ]

    def get_role_libelle(self, obj):
        if obj.user.is_superuser:
            return 'Administrateur global'
        if obj.hopital_role:
            return obj.hopital_role.libelle
        return obj.get_role_display()

    def get_permissions_effectives(self, obj):
        catalog = dict(HopitalRole.permission_catalog())
        return [
            {'code': code, 'libelle': catalog.get(code, code)}
            for code in obj.get_effective_permissions()
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        is_superuser = attrs.get('is_superuser', getattr(getattr(self.instance, 'user', None), 'is_superuser', False))
        hopital_role = attrs.get('hopital_role', getattr(self.instance, 'hopital_role', None))
        hopital = attrs.get('hopital', getattr(self.instance, 'hopital', None))
        role = attrs.get('role', getattr(self.instance, 'role', None))

        if hopital_role and not hopital:
            attrs['hopital'] = hopital_role.hopital
            hopital = hopital_role.hopital

        if hopital_role and hopital and hopital_role.hopital_id != hopital.id:
            raise serializers.ValidationError({'hopital_role': "Ce rôle n'appartient pas à l'hôpital sélectionné."})

        if request and request.user and not request.user.is_superuser:
            # Check if is_superuser is in top-level attrs or nested under 'user'
            user_data = attrs.get('user', {})
            requested_is_superuser_top = attrs.get('is_superuser', None)
            requested_is_superuser_nested = user_data.get('is_superuser', None) if isinstance(user_data, dict) else None
            requested_is_superuser = requested_is_superuser_top if requested_is_superuser_top is not None else requested_is_superuser_nested
            
            if requested_is_superuser is True:
                raise serializers.ValidationError({'is_superuser': "Seul un superuser peut attribuer ce statut."})
            attrs['is_superuser'] = False

            managed_hopital = None
            if hasattr(request.user, 'profile'):
                managed_hopital = request.user.profile.hopital
                if not managed_hopital and request.user.profile.hopital_role:
                    managed_hopital = request.user.profile.hopital_role.hopital

            if not managed_hopital:
                raise serializers.ValidationError({'hopital': "Aucun hôpital associé à votre compte."})

            attrs['hopital'] = managed_hopital
            hopital = managed_hopital

            if hopital_role and hopital_role.hopital_id != managed_hopital.id:
                raise serializers.ValidationError({'hopital_role': "Vous ne pouvez sélectionner que des rôles de votre hôpital."})

        if is_superuser:
            attrs['hopital'] = None
            attrs['hopital_role'] = None
            if not role:
                attrs['role'] = Role.CONTROLEUR_GESTION
            return attrs

        if not role and not hopital_role:
            raise serializers.ValidationError({'role': 'Le rôle est obligatoire.'})

        if hopital_role:
            attrs['role'] = self._map_to_base_role(hopital_role.code)

        return attrs

    def _map_to_base_role(self, role_code):
        normalized = str(role_code or '').strip().lower()
        valid_roles = {choice[0] for choice in Role.choices}
        if normalized in valid_roles:
            return normalized

        if 'controleur' in normalized:
            return Role.CONTROLEUR_GESTION
        if 'directeur' in normalized:
            return Role.DIRECTEUR
        if 'responsable' in normalized and 'financier' in normalized:
            return Role.RESPONSABLE_FINANCIER
        if 'agent' in normalized and 'saisie' in normalized:
            return Role.AGENT_SAISIE
        if 'comptable' in normalized:
            return Role.COMPTABLE_ANALYTIQUE

        return Role.COMPTABLE_ANALYTIQUE

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password', None)
        validated_data.pop('is_superuser', None)  # Remove is_superuser from validated_data for UserProfile
        request = self.context.get('request')
        is_request_superuser = bool(request and request.user and request.user.is_superuser)
        requested_is_superuser = bool(user_data.get('is_superuser', False))
        
        if requested_is_superuser and not is_request_superuser:
            requested_is_superuser = False
        
        user = User.objects.create(
            username=user_data['username'],
            email=user_data.get('email', ''),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            is_superuser=requested_is_superuser,
            is_staff=requested_is_superuser,
            is_active=user_data.get('is_active', True),
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return UserProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)
        validated_data.pop('is_superuser', None)  # Remove is_superuser from validated_data for UserProfile
        request = self.context.get('request')
        is_request_superuser = bool(request and request.user and request.user.is_superuser)
        
        for attr, value in user_data.items():
            if attr == 'is_superuser' and not is_request_superuser:
                continue
            setattr(instance.user, attr, value)
        if 'is_superuser' in user_data and is_request_superuser:
            instance.user.is_staff = bool(user_data.get('is_superuser'))
        if password:
            instance.user.set_password(password)
        instance.user.save()
        # Mettre à jour UserProfile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ExerciceSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les exercices comptables avec contraintes de clôture"""
    est_clos = serializers.BooleanField(required=False, default=False)
    
    class Meta:
        model = Exercice
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        """Valider les contraintes d'exercice"""
        # Si on modifie un exercice existant, vérifier qu'il n'est pas clôturé
        if self.instance and self.instance.est_clos:
            raise serializers.ValidationError(
                "Cet exercice est clôturé et ne peut pas être modifié."
            )
        
        # Validation des dates
        date_debut = attrs.get('date_debut', self.instance.date_debut if self.instance else None)
        date_fin = attrs.get('date_fin', self.instance.date_fin if self.instance else None)
        
        if date_debut and date_fin:
            if date_debut >= date_fin:
                raise serializers.ValidationError({
                    'date_fin': "La date de fin doit être postérieure à la date de début."
                })
        
        # Si est_actif=True, s'assurer que est_clos=False
        if attrs.get('est_actif', getattr(self.instance, 'est_actif', False)):
            attrs['est_clos'] = False
        
        return attrs


class CompteChargeSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les comptes de charges"""
    
    class Meta:
        model = CompteCharge
        fields = ['id', 'numero', 'libelle', 'hopital']
    
    def create(self, validated_data):
        request = self.context.get('request')
        # Si hopital fourni explicitement (superuser staging), l'utiliser
        if validated_data.get('hopital'):
            return super().create(validated_data)

        user_hopital_id = None
        if request and request.user and hasattr(request.user, 'profile'):
            user_hopital_id = request.user.profile.hopital_id

        if user_hopital_id:
            validated_data['hopital_id'] = user_hopital_id
        else:
            default_hopital = Hopital.objects.order_by('id').first()
            if default_hopital:
                validated_data['hopital'] = default_hopital

        return super().create(validated_data)


class CentreCoutSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les centres de coûts"""
    centre_responsabilite_code = serializers.CharField(
        source='centre_responsabilite.code',
        read_only=True
    )
    centre_responsabilite_libelle = serializers.CharField(
        source='centre_responsabilite.libelle',
        read_only=True
    )
    
    class Meta:
        model = CentreCout
        fields = '__all__'


class ChargeSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les charges"""
    created_by_username = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    compte_numero = serializers.CharField(
        source='compte.numero',
        read_only=True
    )
    compte_libelle = serializers.CharField(
        source='compte.libelle',
        read_only=True
    )
    centre_cout_code = serializers.CharField(
        source='centre_cout.code',
        read_only=True
    )
    centre_cout_libelle = serializers.CharField(
        source='centre_cout.libelle',
        read_only=True
    )
    centre_responsabilite_id = serializers.IntegerField(
        source='centre_cout.centre_responsabilite.id',
        read_only=True
    )
    centre_responsabilite_code = serializers.CharField(
        source='centre_cout.centre_responsabilite.code',
        read_only=True
    )
    centre_responsabilite_libelle = serializers.CharField(
        source='centre_cout.centre_responsabilite.libelle',
        read_only=True
    )
    
    class Meta:
        model = Charge
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']


from decimal import Decimal

class CleRepartitionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les clés de répartition"""
    centre_source_code = serializers.CharField(
        source='centre_source.code',
        read_only=True
    )
    centre_source_libelle = serializers.CharField(
        source='centre_source.libelle',
        read_only=True
    )
    centre_destination_code = serializers.CharField(
        source='centre_destination.code',
        read_only=True
    )
    centre_destination_libelle = serializers.CharField(
        source='centre_destination.libelle',
        read_only=True
    )

    class Meta:
        model = CleRepartition
        fields = '__all__'

    def validate(self, attrs):
        centre_source = attrs.get('centre_source', getattr(self.instance, 'centre_source', None))
        centre_destination = attrs.get('centre_destination', getattr(self.instance, 'centre_destination', None))
        exercice = attrs.get('exercice', getattr(self.instance, 'exercice', None))
        pourcentage = attrs.get('pourcentage', getattr(self.instance, 'pourcentage', None))

        if centre_source and centre_source.type_centre != 'NT_UO':
            raise serializers.ValidationError('Le centre source doit être un NT_UO.')

        if centre_source and centre_destination and centre_source == centre_destination:
            raise serializers.ValidationError('Le centre destination ne peut pas être identique au centre source.')

        if exercice and centre_source and pourcentage is not None:
            existing_total = CleRepartition.objects.filter(
                exercice=exercice,
                centre_source=centre_source
            ).exclude(pk=getattr(self.instance, 'pk', None)).aggregate(total=Sum('pourcentage'))['total'] or Decimal('0')

            if existing_total + pourcentage > 100:
                raise serializers.ValidationError('Total des pourcentages > 100 pour ce centre source.')

        return attrs


class ResultatCalculSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les résultats de calcul"""
    centre_cout_code = serializers.CharField(
        source='centre_cout.code',
        read_only=True
    )
    centre_cout_libelle = serializers.CharField(
        source='centre_cout.libelle',
        read_only=True
    )
    centre_cout_type_centre = serializers.CharField(
        source='centre_cout.type_centre',
        read_only=True
    )
    centre_cout_unite_oeuvre = serializers.CharField(
        source='centre_cout.unite_oeuvre',
        read_only=True
    )
    centre_cout_tarif = serializers.DecimalField(
        source='centre_cout.tarif',
        max_digits=15,
        decimal_places=2,
        read_only=True,
        allow_null=True
    )
    centre_responsabilite_id = serializers.IntegerField(
        source='centre_cout.centre_responsabilite.id',
        read_only=True
    )
    centre_responsabilite_code = serializers.CharField(
        source='centre_cout.centre_responsabilite.code',
        read_only=True
    )
    centre_responsabilite_libelle = serializers.CharField(
        source='centre_cout.centre_responsabilite.libelle',
        read_only=True
    )
    
    class Meta:
        model = ResultatCalcul
        fields = '__all__'


class FonctionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les fonctions"""
    class Meta:
        model = Fonction
        fields = '__all__'


class CentreResponsabiliteSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les centres de responsabilité"""
    fonction_code = serializers.CharField(source='fonction.code', read_only=True)
    fonction_libelle = serializers.CharField(source='fonction.libelle', read_only=True)
    
    class Meta:
        model = CentreResponsabilite
        fields = ['id', 'code', 'libelle', 'fonction', 'fonction_code', 'fonction_libelle']


class ProduitSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les produits (recettes)"""
    centre_cout_code = serializers.CharField(source='centre_cout.code', read_only=True)
    centre_cout_libelle = serializers.CharField(source='centre_cout.libelle', read_only=True)
    type_produit_display = serializers.CharField(source='get_type_produit_display', read_only=True)
    
    class Meta:
        model = Produit
        fields = [
            'id', 'exercice', 'centre_cout', 'centre_cout_code', 
            'centre_cout_libelle', 'periode', 'type_produit', 'type_produit_display', 'montant'
        ]
        read_only_fields = []


class ActiviteSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les activités (volumes d'œuvre)"""
    centre_cout_code = serializers.CharField(source='centre_cout.code', read_only=True)
    centre_cout_libelle = serializers.CharField(source='centre_cout.libelle', read_only=True)
    centre_cout_unite_oeuvre = serializers.CharField(source='centre_cout.unite_oeuvre', read_only=True)
    
    class Meta:
        model = Activite
        fields = [
            'id', 'exercice', 'centre_cout', 'centre_cout_code',
            'centre_cout_libelle', 'centre_cout_unite_oeuvre', 'periode', 'volume'
        ]
        read_only_fields = []