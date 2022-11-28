from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .serializers import RegisterUserSerializer, LoginUserSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)}
    

class  UserRegisterView(APIView):
    def post(self,request,format = None):
        serializer = RegisterUserSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
           user = serializer.save()
           token = get_tokens_for_user(user)
           return Response(data = {"msg":"Registration Successfully done","tokens" :token},status = status.HTTP_201_CREATED)
        else: 
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request,format = None):
        serializer = LoginUserSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            email = request.data.get("email")
            password = request.data.get("password")
            user = authenticate(username = email, password = password,is_active = True)
            print(user)
            if user is not None: 
                token = get_tokens_for_user(user)
                return Response(data = {"msg":"Successfully logged in!","token":token},status = status.HTTP_200_OK)
            else:
                return Response(data = {"ERRORS":{"non_field_errors":["Invalid username or password!"]}},status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format = None):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)