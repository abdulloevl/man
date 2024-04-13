from ninja import NinjaAPI
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from .models import User, AccessToken,Article, Comment
from rest_framework import viewsets, permissions
from .serializers import ArticleSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


api = NinjaAPI()

@api.post('/login')
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if user:
        # Генерация JWT токена
        token = jwt.encode({'username': user.username, 'exp': datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY, algorithm='HS256')
        AccessToken.objects.create(user=user, token=token)
        return {'token': token}
    else:
        return {'error': 'Неверные учетные данные'}, 401

@api.get('/protected')
def protected(request, Authorization: str):
    try:
        token = Authorization.split()[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        username = payload['username']
        user = User.objects.get(username=username)
        AccessToken.objects.get(user=user, token=token)
        return {'message': f'Доступ разрешен для пользователя {username}'}
    except jwt.ExpiredSignatureError:
        return {'error': 'Истек срок действия токена'}, 401
    except jwt.InvalidTokenError:
        return {'error': 'Недействительный токен'}, 401
    except User.DoesNotExist:
        return {'error': 'Пользователь не найден'}, 404
    except AccessToken.DoesNotExist:
        return {'error': 'Токен доступа не найден'}, 401
