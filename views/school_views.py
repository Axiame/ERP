from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from school.models import School
from school.serializers import SchoolSerializer

@api_view(['GET'])
def list_schools(request):
    schools = School.objects.all()
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_school(request, pk):
    try:
        school = School.objects.get(pk=pk)
    except School.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    serializer = SchoolSerializer(school)
    return Response(serializer.data)

@api_view(['POST'])
def create_school(request):
    serializer = SchoolSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
def update_school(request, pk):
    try:
        school = School.objects.get(pk=pk)
        except School.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def delete_school(request, pk):
    try:
        school = School.objects.get(pk=pk)
    except School.DoesNotExist:
        return Response(status.status.HTTP_404_NOT_FOUND)
    school.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)