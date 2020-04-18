from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes((AllowAny,))
def login(req):
    username = req.data.get("username")
    password = req.data.get("password")
    if username is None or password is None:
        return Response({'msg': 'Please provide both username and password'})
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'msg': 'Invalid Credentials'})
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'username': user.username,
        'email': user.email,
        'name': user.first_name + ' ' + user.last_name,
        'token': token.key
    })

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(req):

    username = req.data.get("username")
    password = req.data.get("password")
    email = req.data.get("email")
    first_name = req.data.get("first_name")
    last_name = req.data.get("last_name")

    if(username is None or password is None or email is None or first_name is None
        or username == "" or password == "" or email == "" or first_name == ""):
        return Response({'msg' : 'Please provide all the credentials'})

    if(User.objects.filter(username=username)):
        return Response({'msg' : 'Username already taken'})

    user = User.objects.create_user(
        username,
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
        is_superuser = False,
        is_staff = False
    )
    user.save()
    return Response({'msg': 'Account created successfully'})