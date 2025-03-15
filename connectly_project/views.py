from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
def add_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fetch_users(request):
    all_users = User.objects.all()
    serialized_users = UserSerializer(all_users, many=True)
    return Response(serialized_users.data)

@api_view(['PUT'])
def modify_user(request, user_id):
    try:
        existing_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    updated_serializer = UserSerializer(existing_user, data=request.data, partial=True)
    if updated_serializer.is_valid():
        updated_serializer.save()
        return Response(updated_serializer.data)
    return Response(updated_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_user(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
        target_user.delete()
        return Response({'message': 'User successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
