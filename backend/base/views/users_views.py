from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from rest_framework import status




from base.serializers import  UserSerializer , UserSerializerWithToken
# Create your views here.

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k , v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# view for getting users  profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user , many = False)
    return Response(serializer.data)


# view for  updating users  profile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user , many = False)

    data = request.data 
    user.first_name = data['name']
    user.email = data['email']
    user.username = data['email']

    if data['password']  != '':
        user.password = make_password(data['password'])


    return Response(serializer.data)

# view for seeing all users
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users= User.objects.all()

    serializer = UserSerializer(users , many = True)
    return Response(serializer.data)

#view for deleting users frio admin panel
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request , pk):
    user= User.objects.get(id = pk)
    user.delete()
    return Response("user deleted!!!")

# view for registering new users 

@api_view(['POST'])
def RegisterUser(request):
     data = request.data
     
     try :
        user = User.objects.create(
            first_name =data['name'],
            username =data['email'],
            email =data['email'],
            password = make_password(data['password']),
            )
     

        serializer = UserSerializerWithToken(user , many = False)
        return Response(serializer.data)

     except:
         message = {'detail' : 'user with this information already exists.'}
         return Response(message , status= status.HTTP_400_BAD_REQUEST)
