from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer, SignupSerializer
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Create
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Signup
@api_view(['POST'])
def signup(request):
    """
    Crée un nouvel utilisateur.
    """
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Ici, vous pouvez ajouter des logiques supplémentaires comme l'envoi d'un email de confirmation

            return Response({"message": "User registered successfully. Please check your email to activate your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Read (Retrieve users by filter)
@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        # Récupérer les arguments GET
        search_term = request.GET.get('search_term', None)
        birthday = request.GET.getlist('birthday')
        job = request.GET.getlist('job')
        uid = request.GET.getlist('uid')
        pk = request.GET.getlist('pk')

        # Créer un dictionnaire de filtres basé sur les arguments présents
        filters = {}

        # Si un terme de recherche est fourni, vérifier s'il s'agit d'un email
        if search_term:
            filters['last_name__icontains'] = search_term
            filters['first_name__icontains'] = search_term
            filters['email__icontains'] = search_term  # Ajout de la recherche par email ici

        if birthday:
            filters['birthday__in'] = birthday
        if job:
            filters['job__in'] = job
        if uid:
            filters['uid__in'] = uid
        if pk:
            filters['pk__in'] = pk

        # Combinez les filtres pour le terme de recherche et les autres filtres
        users = User.objects.filter(
            Q(last_name__icontains=search_term) |
            Q(first_name__icontains=search_term) |
            Q(email__icontains=search_term) |  # Ajout de la recherche par email ici
            Q(**filters)
        )

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Read (Retrieve specific user by id)
@api_view(['GET'])
def retrieve_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Update
@api_view(['PATCH'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete
@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        'access_token': access_token,
        'refresh_token': str(refresh)
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')

    if refresh_token is None:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Générer un nouvel accès à partir du token de rafraîchissement
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        return Response({
            'access_token': access_token
        }, status=status.HTTP_200_OK)

    except TokenError:  # à partir de rest_framework_simplejwt.exceptions
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
