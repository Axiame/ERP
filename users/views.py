from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.db.models import Q

# Create
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
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
        if search_term:
            filters['last_name__icontains'] = search_term
            filters['first_name__icontains'] = search_term
        if birthday:
            filters['birthday__in'] = birthday
        if job:
            filters['job__in'] = job
        if uid:
            filters['uid__in'] = uid
        if pk:
            filters['pk__in'] = pk

        if search_term:
            users = User.objects.filter(
                Q(last_name__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(**filters)
            )
        else:
            users = User.objects.filter(**filters)
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
@api_view(['PUT'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
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
