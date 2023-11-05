from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # Récupérez le mot de passe du dictionnaire des données validées
        password = validated_data.pop('password', None)
        # Créez une instance de l'objet User sans sauvegarder en base
        instance = self.Meta.model(**validated_data)
        # S'il y a un mot de passe, utilisez set_password pour le hacher
        if password:
            instance.set_password(password)
        # Enfin, sauvegardez l'instance en base
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'
