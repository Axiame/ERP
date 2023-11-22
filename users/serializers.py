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
class SignupSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Ici, vous pouvez ajouter d'autres validations personnalisées

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        return user