from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import json


@extend_schema(
    summary='User Login',
    description='Authenticate user with username and password. Returns authentication token on successful login.',
    tags=['Authentication'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'admin'},
                'password': {'type': 'string', 'example': 'admin123'}
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'description': 'Login successful',
            'example': {
                'message': 'Login successful',
                'token': 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0',
                'user': {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@example.com',
                    'first_name': '',
                    'last_name': '',
                    'is_staff': True,
                    'is_superuser': True
                }
            }
        },
        400: {
            'description': 'Bad request',
            'example': {'error': 'Username and password are required'}
        },
        401: {
            'description': 'Authentication failed',
            'example': {'error': 'Invalid username or password'}
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def api_login(request):
    """
    Token-based login endpoint that accepts JSON data and returns authentication token.
    """
    try:
        # Parse JSON data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Get or create token for the user
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'message': 'Login successful',
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'User account is disabled'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary='User Logout',
    description='Logout the current user and delete their authentication token.',
    tags=['Authentication'],
    responses={
        200: {
            'description': 'Logout successful',
            'example': {'message': 'Logout successful'}
        },
        401: {
            'description': 'User not authenticated',
            'example': {'error': 'Authentication credentials were not provided'}
        }
    }
)
@api_view(['POST'])
def api_logout(request):
    """
    Token-based logout endpoint that deletes the user's authentication token.
    """
    try:
        # Delete the user's token
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary='Get current user info',
    description='Retrieve information about the currently authenticated user using token authentication.',
    tags=['Authentication'],
    responses={
        200: {
            'description': 'User information',
            'example': {
                'user': {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@example.com',
                    'first_name': '',
                    'last_name': '',
                    'is_staff': True,
                    'is_superuser': True
                }
            }
        },
        401: {
            'description': 'User not authenticated',
            'example': {'error': 'Authentication credentials were not provided'}
        }
    }
)
@api_view(['GET'])
def api_user_info(request):
    """
    Get current user information for token-authenticated user.
    """
    if request.user.is_authenticated:
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Authentication credentials were not provided'
        }, status=status.HTTP_401_UNAUTHORIZED)