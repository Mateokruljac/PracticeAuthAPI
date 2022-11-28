from rest_framework import serializers 
from accounts.models import User
from django.db.models import Q
#Create your serializers in here

class RegisterUserSerializer(serializers.ModelSerializer):
    #we are writting password2 because we need confirm password filed in Registration Request
    password2 = serializers.CharField(max_length = 200,style = {"input_type" :"password"}, write_only = True)
    class Meta:
        model = User
        fields = ["id","first_name","last_name","email","username","password","password2"]
        extra_kwargs = {
            "password" : {
                "write_only" : True,
            }
        }
        
    def validate(self, attrs):
        """
        Validate password and confirm password and check user`s email and username
        
        Args:
            attrs (_type_): ["id","first_name","last_name","username", "email",
            "password","password2"]

        Raises:
            serializers.ValidationError: if password and confirm password not matching
            serializers.ValidationError:  If user already exists in database

        Returns:
            data
        """
        #get email,username,password and confirm_password value
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")
        password2 = attrs.get("password2")
        
        if password != password2: 
            raise serializers.ValidationError("Password and confirm password not matching")
        
        if User.objects.filter(Q(email = email)|Q(username = username)).exists():
            raise serializers.ValidationError("User with that username or email already exists!")
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 200)
    class Meta:
        model = User
        fields = ["email","password"]
        extra_kwargs = {
            "password" : {
                "write_only" : True
            }
        }
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ["first_name","last_name","username","email"]